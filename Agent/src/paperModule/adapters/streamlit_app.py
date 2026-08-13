"""Human Web UI.

cmd
streamlit run src/paperModule/adapters/streamlit_app.py --server.port 8501

powershell
cloudflared tunnel --url http://localhost:8501
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import hmac
import io
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

from agent.usage_log import (
    complete_search,
    database_path,
    fail_search,
    get_search,
    list_searches,
    start_search,
)
from kmed_domestic_lit.fast.search import fast_search

_DEFAULT_TOP_K = 10


def _user_id() -> str | None:
    """Use the OIDC identity when authentication is configured."""
    user = getattr(st, "user", None)
    if user is None or not getattr(user, "is_logged_in", False):
        return None
    return getattr(user, "email", None) or getattr(user, "name", None)


def _elapsed_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _as_csv(records: list[dict]) -> str:
    if not records:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue()


def _configured_password_hash() -> str | None:
    from_environment = os.getenv("BIOINFO_APP_PASSWORD_HASH")
    if from_environment:
        return from_environment
    try:
        return st.secrets.get("app_password_hash")
    except FileNotFoundError:
        return None


def _require_password() -> None:
    if st.session_state.get("password_authenticated", False):
        return

    st.title("국내외 한의학 논문 탐색")
    st.caption("계속하려면 비밀번호를 입력하세요.")

    with st.form("password_form", clear_on_submit=False):
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("접속", type="primary")

    if submitted:
        expected_hash = _configured_password_hash()
        if expected_hash is None:
            st.error("앱 비밀번호가 설정되지 않았습니다.")
        else:
            entered_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if hmac.compare_digest(entered_hash, expected_hash):
                st.session_state.password_authenticated = True
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")

    st.stop()


st.set_page_config(page_title="국내 한의학 논문 탐색", layout="wide")
_require_password()

if st.sidebar.button("로그아웃"):
    st.session_state.password_authenticated = False
    st.rerun()

st.title("국내외 한의학 논문 탐색")

fast_tab, deep_tab, history_tab = st.tabs(
    ["논문 검색", "Deep Research (현재 미사용)", "사용 기록"]
)

with fast_tab:
    st.caption("현재 활성 source: KCI (OASIS는 공식 Open API 확보 전까지 비활성)")
    query = st.text_area(
        "한의학 질문",
        placeholder="예: 뇌졸중 후유증에 대한 침 치료의 효과를 알려줘",
        key="fast_query",
    )
    st.caption("찾고 싶은 내용을 자연어 한 문장으로 입력하세요.")

    if st.button("검색", key="fast_search_btn") and query:
        started_at = time.perf_counter()
        request_id = start_search(
            user_id=_user_id(),
            search_mode="fast",
            query=query,
            parameters={
                "sources": ["KCI"],
                "top_k": _DEFAULT_TOP_K,
            },
        )
        try:
            with st.spinner("KCI 검색 중..."):
                cards = asyncio.run(
                    fast_search(
                        query,
                        k=_DEFAULT_TOP_K,
                    )
                )
            serialized_cards = [card.model_dump(mode="json") for card in cards]
            complete_search(
                request_id,
                result_count=len(cards),
                elapsed_ms=_elapsed_ms(started_at),
                result={"papers": serialized_cards},
            )
        except Exception as error:
            fail_search(request_id, elapsed_ms=_elapsed_ms(started_at), error=error)
            st.error("검색 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")
        else:
            st.caption(f"{len(cards)}건")
            for c in cards:
                with st.expander(f"[{c.score:.3f}] {c.title} ({c.year or '-'})"):
                    st.write(f"**저자**: {c.authors_short} · **학술지**: {c.journal or '-'}")
                    st.write(f"**출처**: {', '.join(c.sources)} · **source rank**: {c.source_ranks}")
                    st.write(f"**피인용**: {c.citation_count if c.citation_count is not None else '-'}")
                    if c.abstract:
                        st.write(c.abstract)
                    links = []
                    if c.doi:
                        links.append(f"DOI: {c.doi}")
                    if c.fulltext_url:
                        links.append(f"[원문]({c.fulltext_url})")
                    if links:
                        st.write(" · ".join(links))

with deep_tab:
    st.info("Deep Research 기능은 현재 사용하지 않습니다.")
    st.caption("현재는 빠른 논문 검색 결과만 제공합니다.")

with history_tab:
    st.caption(f"SQLite: {database_path()}")

    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
    status_value = col1.selectbox(
        "상태",
        ["전체", "completed", "failed", "running"],
        key="history_status",
    )
    mode_value = col2.selectbox(
        "검색 유형",
        ["전체", "fast", "deep"],
        key="history_mode",
    )
    query_value = col3.text_input(
        "질문 검색",
        placeholder="질문에 포함된 단어",
        key="history_query",
    )
    limit_value = col4.number_input(
        "최대 행 수",
        min_value=10,
        max_value=5000,
        value=200,
        step=10,
        key="history_limit",
    )

    records = list_searches(
        limit=int(limit_value),
        status=None if status_value == "전체" else status_value,
        search_mode=None if mode_value == "전체" else mode_value,
        query_contains=query_value.strip() or None,
    )

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("조회된 요청", len(records))
    metric2.metric("성공", sum(row["status"] == "completed" for row in records))
    metric3.metric("실패", sum(row["status"] == "failed" for row in records))

    if not records:
        st.info("조건에 맞는 사용 기록이 없습니다.")
    else:
        st.dataframe(records, use_container_width=True, hide_index=True)
        st.download_button(
            "목록 CSV 다운로드",
            data=_as_csv(records).encode("utf-8-sig"),
            file_name="search_usage.csv",
            mime="text/csv",
        )

        labels = {
            row["request_id"]: (
                f"{row['created_at']} · {row['search_mode']} · "
                f"{row['status']} · {row['query'][:60]}"
            )
            for row in records
        }
        selected_id = st.selectbox(
            "상세 기록",
            options=list(labels),
            format_func=labels.__getitem__,
            key="history_selected_id",
        )
        selected = get_search(selected_id)
        if selected:
            summary = {
                key: value
                for key, value in selected.items()
                if key not in {"parameters", "result"}
            }
            st.json(summary)

            st.subheader("검색 조건")
            st.json(selected.get("parameters") or {})

            st.subheader("저장된 결과")
            st.json(selected.get("result") or {})
