"""Fast Search orchestrator. spec section 7."""
from __future__ import annotations

import asyncio
import unicodedata

from ..config import fast_ranking_config
from ..models import Paper, PaperCard, paper_to_card
from ..sources.base import SourceAdapter
from ..sources.kci import KCIAdapter
from ..sources.pubmed import PubMedAdapter
from .dedup import merge_source_results
from .rerank import score_papers


def normalize_query(query: str) -> str:
    """Minimal preprocessing only (spec section 6.2): no NLP expansion."""
    q = unicodedata.normalize("NFKC", query)
    return " ".join(q.strip().split())


def default_sources() -> list[SourceAdapter]:
    return [KCIAdapter(), PubMedAdapter()]


async def fast_search(
    query: str,
    k: int = 10,
    year_from: int | None = None,
    year_to: int | None = None,
    journal: str | None = None,
    sources: list[SourceAdapter] | None = None,
    limit_per_source: int = 50,
) -> list[PaperCard]:
    q = normalize_query(query)
    adapters = sources or default_sources()

    filters = {"year_from": year_from, "year_to": year_to, "journal": journal}
    results = await asyncio.gather(
        *(adapter.search(q, limit=limit_per_source, **filters) for adapter in adapters)
    )
    by_source: dict[str, list[Paper]] = {
        adapter.name: papers for adapter, papers in zip(adapters, results)
    }

    merged = merge_source_results(by_source)
    scores = score_papers(merged, fast_ranking_config())
    ranked = sorted(merged, key=lambda p: scores.get(p.uid, 0), reverse=True)

    return [paper_to_card(p, scores.get(p.uid, 0.0), matched_query=q) for p in ranked[:k]]
