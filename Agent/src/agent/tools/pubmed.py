"""PubMed (NCBI E-utilities) search tool — the Agent-level counterpart to
paperModule's domestic-only KCI tool.

Uses paperModule's PubMedAdapter and ranking engine so results return full
PaperCard schema with `score` and `source_ranks={"pubmed": rank}`.
"""
from __future__ import annotations

import sys
from pathlib import Path

from langchain_core.tools import tool

# Ensure paperModule's src is in sys.path
_PAPER_MODULE_SRC = Path(__file__).resolve().parents[2] / "paperModule" / "src"
if str(_PAPER_MODULE_SRC) not in sys.path:
    sys.path.insert(0, str(_PAPER_MODULE_SRC))

from kmed_domestic_lit.config import fast_ranking_config
from kmed_domestic_lit.fast.dedup import merge_source_results
from kmed_domestic_lit.fast.rerank import score_papers
from kmed_domestic_lit.models import paper_to_card
from kmed_domestic_lit.sources.pubmed import PubMedAdapter


@tool
async def search_pubmed(query: str, limit: int = 10) -> list[dict]:
    """해외(PubMed) 학술논문 검색. query는 반드시 영어 키워드로 작성할 것.
    국내 문헌은 KCI 관련 도구를 사용하고, 이 도구는 해외 문헌에만 사용한다."""
    adapter = PubMedAdapter()
    papers = await adapter.search(query, limit=limit)
    if not papers:
        return []

    merged = merge_source_results({"pubmed": papers})
    scores = score_papers(merged, fast_ranking_config())
    ranked = sorted(merged, key=lambda p: scores.get(p.uid, 0), reverse=True)
    cards = [paper_to_card(p, scores.get(p.uid, 0.0), matched_query=query) for p in ranked]
    return [c.model_dump() for c in cards]
