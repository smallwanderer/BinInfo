"""Lightweight deterministic reranking. spec section 13."""
from __future__ import annotations

import math
from datetime import date

from ..models import Paper
from .fusion import apply_rrf

_META_FIELDS = ("title", "abstract", "authors", "journal", "year", "keywords")


def _minmax(values: dict[str, float]) -> dict[str, float]:
    if not values:
        return {}
    lo, hi = min(values.values()), max(values.values())
    if hi == lo:
        return {k: 1.0 for k in values}
    return {k: (v - lo) / (hi - lo) for k, v in values.items()}


def _recency(paper: Paper, half_life: int) -> float:
    if not paper.year:
        return 0.0
    age = max(date.today().year - paper.year, 0)
    return math.exp(-age / half_life)


def _completeness(paper: Paper) -> float:
    present = 0
    for field in _META_FIELDS:
        value = getattr(paper, field)
        if value:
            present += 1
    return present / len(_META_FIELDS)


def score_papers(papers: list[Paper], cfg: dict) -> dict[str, float]:
    """Returns uid -> final weighted score."""
    if not papers:
        return {}

    rrf = apply_rrf(papers, cfg)
    relevance = _minmax(rrf)
    citation_raw = {p.uid: math.log1p(p.citation_count or 0) for p in papers}
    citation = _minmax(citation_raw)
    half_life = cfg.get("recency_half_life_years", 8)
    recency = {p.uid: _recency(p, half_life) for p in papers}
    completeness = {p.uid: _completeness(p) for p in papers}

    w = cfg["rerank_weights"]
    return {
        p.uid: (
            w["relevance"] * relevance.get(p.uid, 0)
            + w["citation"] * citation.get(p.uid, 0)
            + w["recency"] * recency.get(p.uid, 0)
            + w["metadata_completeness"] * completeness.get(p.uid, 0)
        )
        for p in papers
    }
