"""Reciprocal Rank Fusion. spec section 12."""
from __future__ import annotations

from ..models import Paper


def rrf_score(source_ranks: dict[str, int], k: int, source_weight: dict[str, float]) -> float:
    return sum(
        source_weight.get(source, 1.0) / (k + rank)
        for source, rank in source_ranks.items()
    )


def apply_rrf(papers: list[Paper], cfg: dict) -> dict[str, float]:
    k = cfg["rrf"]["k"]
    weights = cfg["rrf"]["source_weight"]
    return {p.uid: rrf_score(p.source_ranks, k, weights) for p in papers}
