"""Layer 2: Fast Search — run Layer 1's (Entry Agent + Query Builder) sub_queries
against KCI (via paperModule's MCP tool) and PubMed. No LLM call in this layer
itself — see agent-docs/planner-v2.md §3 "Fast Search".

Reuses snippet/01_result.json when it matches the query (avoids re-paying for
Entry Agent/Query Builder); otherwise computes Layer 1 fresh.

Usage: python 02_fast_search.py ["질문"]
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from langchain_mcp_adapters.client import MultiServerMCPClient  # noqa: E402

from agent.capabilities import classify_constraints  # noqa: E402
from agent.graph import MCP_SERVERS  # noqa: E402
from agent.planning.fast_planner import entry_agent, query_builder  # noqa: E402
from agent.planning.usage import sum_usage  # noqa: E402
from agent.tools.pubmed import search_pubmed  # noqa: E402

RESULT_1_PATH = Path(__file__).resolve().parent / "01_result.json"
DEFAULT_QUERY = "뇌혈관질환후유증에 대한 침치료의 효과를 IF 5이상 저널 기준으로 찾아줘"


def _coerce(result):
    """FastMCP serializes a `list[dict]` tool return as one MCP text-content
    block PER ITEM (each block's "text" is that one item's JSON), rather than
    a single block wrapping the whole array -- reconstruct the real list.
    Also handles the plain-JSON-string case for other transports/versions.
    """
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


async def load_layer1(query: str) -> dict:
    if RESULT_1_PATH.exists():
        cached = json.loads(RESULT_1_PATH.read_text(encoding="utf-8"))
        if cached.get("query") == query:
            return cached
    entry, entry_usage = await entry_agent(query)
    fillable, unfillable = classify_constraints(entry.constraints)
    built, builder_usage = await query_builder(entry.goal, fillable)
    return {
        "query": query,
        "entry_agent": {
            "goal": entry.goal,
            "constraints": entry.constraints,
            "fillable_constraints": fillable,
            "unfillable_constraints": unfillable,
        },
        "query_builder": built.model_dump(),
        "usage": {
            "entry_agent": entry_usage,
            "query_builder": builder_usage,
            "total": sum_usage(entry_usage, builder_usage),
        },
    }


async def search_one(kci_tool, sub_query: dict) -> dict:
    # KCI goes through one shared stdio MCP session; firing multiple KCI
    # calls concurrently (via gather across sub-queries) was observed to
    # corrupt responses (JSONDecodeError / _MCPToolExecutionError). PubMed
    # is a plain HTTP call with no shared session, so it stays concurrent
    # with the KCI call for this one sub-query.
    kci_result, pubmed_result = await asyncio.gather(
        kci_tool.ainvoke({"query": sub_query["kci"], "k": 5}),
        search_pubmed.ainvoke({"query": sub_query["pubmed"], "limit": 5}),
    )
    return {"topic": sub_query["topic"], "kci": _coerce(kci_result), "pubmed": _coerce(pubmed_result)}


async def run(query: str) -> dict:
    layer1 = await load_layer1(query)
    sub_queries = layer1["query_builder"]["sub_queries"]

    mcp_client = MultiServerMCPClient(MCP_SERVERS)
    tools = {t.name: t for t in await mcp_client.get_tools()}
    kci_tool = tools["search_literature"]

    # Sub-queries processed sequentially (not gathered) -- see search_one()'s
    # comment on why concurrent KCI calls over the shared stdio session broke.
    fast_results = [await search_one(kci_tool, sq) for sq in sub_queries]
    return {**layer1, "fast_search": fast_results}


async def main() -> None:
    query = " ".join(sys.argv[1:]) or DEFAULT_QUERY
    result = await run(query)

    out_path = Path(__file__).resolve().parent / "02_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # Windows console codepage (cp949) can't render every unicode char PubMed
    # returns (e.g. narrow no-break space) — save first, print best-effort.
    sys.stdout.reconfigure(errors="replace")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if "usage" in result:
        print(f"\ntoken usage (Layer 1, reused or fresh): {result['usage']['total']}")
    print(f"saved to {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
