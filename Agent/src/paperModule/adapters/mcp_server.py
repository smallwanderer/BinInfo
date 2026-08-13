"""MCP interface. spec section 19: search_literature / research_literature /
get_paper / get_fulltext."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dotenv import load_dotenv

# Launched as a stdio subprocess (see Agent/src/agent/graph.py's MCP_SERVERS) --
# it does not automatically inherit the parent process's loaded .env vars
# (e.g. KCI_API_KEY), so load them here explicitly.
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

from mcp.server.fastmcp import FastMCP

from kmed_domestic_lit.deep.research import research_literature as _research_literature
from kmed_domestic_lit.fast.search import fast_search
from kmed_domestic_lit.lookup import get_fulltext as _get_fulltext
from kmed_domestic_lit.lookup import get_paper as _get_paper

mcp = FastMCP("kmed-domestic-lit")


@mcp.tool()
async def search_literature(
    query: str,
    k: int = 10,
    year_from: int | None = None,
    year_to: int | None = None,
    journal: str | None = None,
) -> list[dict]:
    """국내외 한의학 논문 Fast Search. KCI(+ OASIS 활성화 시) 통합 후 PaperCard 목록 반환."""
    cards = await fast_search(query, k=k, year_from=year_from, year_to=year_to, journal=journal)
    return [c.model_dump() for c in cards]


@mcp.tool()
async def research_literature(question: str, seed_uids: list[str] | None = None) -> dict:
    """하나의 연구 질문에 대한 국내외 문헌 기반 Deep Research 보고서 생성."""
    report = await _research_literature(question, seed_uids=seed_uids)
    return report.model_dump()


@mcp.tool()
async def get_paper(uid: str) -> dict | None:
    """uid(예: kci:12345)로 논문 상세정보를 조회."""
    paper = await _get_paper(uid)
    return paper.model_dump() if paper else None


@mcp.tool()
async def get_fulltext(uid: str) -> str | None:
    """원문 URL(가능 시) 또는 초록 fallback을 반환."""
    return await _get_fulltext(uid)


if __name__ == "__main__":
    mcp.run()
