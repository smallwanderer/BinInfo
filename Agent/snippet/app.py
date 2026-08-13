"""Interactive pipeline runner + viewer — Layers 1-5 (Entry Agent ->
Query Builder -> Fast Search -> Relevance Screen/Screened Pool -> PaperQA2
-> Final Answer).

User enters a question, the app runs the full live pipeline and shows every
layer's result. Each run is kept separately for the browser session (no DB,
no disk persistence -- st.session_state clears on restart, which is fine
per spec: "임시로만 존재해도 괜찮다").

Run: streamlit run snippet/app.py
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

_AGENT_SRC = Path(__file__).resolve().parents[1] / "src"
_PAPERMODULE_SRC = _AGENT_SRC / "paperModule" / "src"
sys.path.insert(0, str(_AGENT_SRC))
sys.path.insert(0, str(_PAPERMODULE_SRC))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from langchain_mcp_adapters.client import MultiServerMCPClient  # noqa: E402

from agent.capabilities import classify_constraints  # noqa: E402
from agent.graph import MCP_SERVERS  # noqa: E402
from agent.planning.fast_planner import entry_agent, query_builder  # noqa: E402
from agent.planning.final_answer import synthesize_final_answer  # noqa: E402
from agent.planning.relevance_screen import finalize_pool, relevance_screen  # noqa: E402
from agent.planning.usage import sum_usage  # noqa: E402
from agent.tools.pubmed import search_pubmed  # noqa: E402
from kmed_domestic_lit.deep.paperqa_adapter import PaperQASession  # noqa: E402
from kmed_domestic_lit.models import Paper  # noqa: E402

DEFAULT_QUERY = "뇌혈관질환후유증에 대한 침치료의 효과를 IF 5이상 저널 기준으로 찾아줘"


def _coerce(result):
    """FastMCP serializes a `list[dict]` tool return as one MCP text-content
    block per item rather than one block wrapping the whole array."""
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return result
    if isinstance(result, list) and result and all(
        isinstance(x, dict) and x.get("type") == "text" and "text" in x for x in result
    ):
        return [json.loads(x["text"]) for x in result]
    return result


def _flatten_pool(fast_search: list[dict]) -> dict[str, dict]:
    pool: dict[str, dict] = {}
    for item in fast_search:
        for c in item["kci"] + item["pubmed"]:
            pool.setdefault(c["uid"], c)
    return pool


async def run_pipeline(query: str) -> dict:
    t0 = time.time()
    usages = []

    # Layer 1 — Entry Agent + Query Builder
    entry, entry_usage = await entry_agent(query)
    fillable, unfillable = classify_constraints(entry.constraints)
    built, builder_usage = await query_builder(entry.goal, fillable)
    usages += [entry_usage, builder_usage]
    layer1 = {
        "entry_agent": {
            "goal": entry.goal,
            "constraints": entry.constraints,
            "fillable_constraints": fillable,
            "unfillable_constraints": unfillable,
        },
        "query_builder": built.model_dump(),
    }

    # Layer 2 — Fast Search (KCI via MCP + PubMed). KCI calls stay
    # sequential across sub-queries -- concurrent calls over the shared
    # stdio MCP session were observed to corrupt responses.
    mcp_client = MultiServerMCPClient(MCP_SERVERS)
    tools = {t.name: t for t in await mcp_client.get_tools()}
    kci_tool = tools["search_literature"]

    fast_results = []
    for sq in built.sub_queries:
        kci_result, pubmed_result = await asyncio.gather(
            kci_tool.ainvoke({"query": sq.kci, "k": 5}),
            search_pubmed.ainvoke({"query": sq.pubmed, "limit": 5}),
        )
        fast_results.append(
            {"topic": sq.topic, "kci": _coerce(kci_result), "pubmed": _coerce(pubmed_result)}
        )
    layer2 = {"fast_search": fast_results}

    # Layer 3 — Relevance Screen + Screened Pool
    topics = [sq.topic for sq in built.sub_queries]
    pool = _flatten_pool(fast_results)
    rs_result, rs_usage = await relevance_screen(topics, list(pool.values()), fillable)
    usages.append(rs_usage)
    tags_by_uid = {t.uid: t for t in rs_result.tags}
    screened = [
        {
            **pool[uid],
            "relevant_to": tags_by_uid[uid].relevant_to if uid in tags_by_uid else [],
            "unmet_constraints": tags_by_uid[uid].unmet_constraints if uid in tags_by_uid else [],
        }
        for uid in pool
    ]
    pool_out = finalize_pool(screened)
    layer3 = {
        "topics": topics,
        "constraints": fillable,
        "candidate_count": len(pool),
        "pool": pool_out,
    }

    # Layer 4 — PaperQA2 (persistent session, per-topic query)
    papers = [Paper.model_validate(c) for c in pool_out]
    answers = {}
    async with PaperQASession(model="gpt-4o-mini") as session:
        added = await session.ingest(papers)
        for topic in topics:
            answer, evidence, pqa_usage = await session.ask(topic)
            usages.append(pqa_usage)
            answers[topic] = {"answer": answer, "evidence": [e.model_dump() for e in evidence]}
    layer4 = {"pool_size": len(papers), "ingested": added, "answers": answers}

    # Layer 5 — Final Answer
    topic_answers = {t: a["answer"] for t, a in answers.items()}
    final_answer, fa_usage = await synthesize_final_answer(query, topic_answers, unfillable)
    usages.append(fa_usage)
    layer5 = {"final_answer": final_answer}

    return {
        "query": query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "layer1": layer1,
        "layer2": layer2,
        "layer3": layer3,
        "layer4": layer4,
        "layer5": layer5,
        "total_usage": sum_usage(*usages),
        "elapsed_seconds": time.time() - t0,
    }


# ---------------------------------------------------------------- UI ----

st.set_page_config(page_title="문헌 탐색 파이프라인", layout="wide")
st.title("문헌 탐색 파이프라인")

if "runs" not in st.session_state:
    st.session_state.runs = []  # each run kept only for this browser session

with st.form("query_form"):
    query_input = st.text_input("질문을 입력하세요", value="", placeholder=DEFAULT_QUERY)
    submitted = st.form_submit_button("실행")

if submitted:
    query = query_input.strip() or DEFAULT_QUERY
    with st.spinner("파이프라인 실행 중 (KCI/PubMed 검색 + LLM 호출 다수, 1~2분 소요)..."):
        result = asyncio.run(run_pipeline(query))
    st.session_state.runs.append(result)
    st.success(
        f"완료 — {result['elapsed_seconds']:.1f}초, "
        f"{result['total_usage']['total_tokens']:,} 토큰"
    )

if not st.session_state.runs:
    st.info("질문을 입력하고 실행 버튼을 누르세요.")
    st.stop()

labels = [
    f"[{i + 1}] {r['timestamp']} — {r['query'][:40]}"
    for i, r in enumerate(st.session_state.runs)
]
selected = st.selectbox(
    "결과 선택 (이번 세션에서 실행한 질의들)",
    range(len(labels)),
    format_func=lambda i: labels[i],
    index=len(labels) - 1,
)
run = st.session_state.runs[selected]

col1, col2 = st.columns(2)
col1.metric("총 토큰 소모량", f"{run['total_usage']['total_tokens']:,}")
col2.metric("총 소요 시간", f"{run['elapsed_seconds']:.1f}초")

l1, l2, l3, l4, l5 = run["layer1"], run["layer2"], run["layer3"], run["layer4"], run["layer5"]

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "1. Entry Agent / Query Builder",
        "2. Fast Search",
        "3. Relevance Screen / Screened Pool",
        "4. PaperQA2",
        "5. 최종 답변",
    ]
)

with tab1:
    st.subheader("사용자 질의")
    st.write(run["query"])

    st.subheader("Entry Agent")
    ea = l1["entry_agent"]
    st.write(f"**Goal**: {ea['goal']}")
    col1, col2 = st.columns(2)
    col1.markdown("**채울 수 있는 제약조건**")
    col1.write(ea["fillable_constraints"] or "(없음)")
    col2.markdown("**채울 수 없는 제약조건**")
    col2.write(ea["unfillable_constraints"] or "(없음)")

    st.subheader("Query Builder — sub_queries")
    for sq in l1["query_builder"]["sub_queries"]:
        st.markdown(f"- **{sq['topic']}**\n  - KCI: `{sq['kci']}`\n  - PubMed: `{sq['pubmed']}`")

with tab2:
    for item in l2["fast_search"]:
        with st.expander(
            f"{item['topic']} — KCI {len(item['kci'])}건 / PubMed {len(item['pubmed'])}건"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**KCI**")
                for p in item["kci"]:
                    st.write(f"[{p.get('score', 0):.3f}] {p['title']} ({p.get('year', '-')})")
            with col2:
                st.markdown("**PubMed**")
                for p in item["pubmed"]:
                    st.write(f"[{p.get('score', 0):.3f}] {p['title']} ({p.get('year', '-')})")

with tab3:
    st.write(f"전체 후보 {l3['candidate_count']}건 → Screened Pool {len(l3['pool'])}건")
    for c in l3["pool"]:
        with st.expander(f"[{c.get('score', 0):.3f}] {c['title']}"):
            st.write(
                f"**출처**: {', '.join(c['sources'])} · **연도**: {c.get('year', '-')} · "
                f"**저널**: {c.get('journal', '-')}"
            )
            st.write(f"**관련 토픽**: {', '.join(c['relevant_to'])}")
            if c.get("citation_count") is not None:
                st.write(f"**피인용수**: {c['citation_count']}")
            links = []
            if c.get("doi"):
                links.append(f"DOI: {c['doi']}")
            if c.get("fulltext_url"):
                links.append(f"[원문]({c['fulltext_url']})")
            if links:
                st.write(" · ".join(links))
            if c.get("abstract"):
                st.write(c["abstract"])

with tab4:
    st.write(f"Screened Pool {l4['pool_size']}건 중 {l4['ingested']}건 ingest")
    for topic, a in l4["answers"].items():
        st.subheader(topic)
        st.write(a["answer"])
        with st.expander(f"근거 {len(a['evidence'])}개"):
            for e in a["evidence"]:
                st.markdown(f"- **[{e['uid']}]** {e['quote']}")

with tab5:
    st.subheader("최종 답변")
    st.write(l5["final_answer"])
