"""Deduplication + metadata merge. spec section 10-11."""
from __future__ import annotations

import re
import unicodedata

from ..models import Paper

_PAREN = re.compile(r"[\(\[].*?[\)\]]")
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")


def normalize_title(title: str) -> str:
    t = unicodedata.normalize("NFKC", title or "").lower()
    t = _PAREN.sub("", t)
    t = _PUNCT.sub("", t)
    return _WS.sub(" ", t).strip()


def _identity_keys(paper: Paper) -> list[str]:
    keys = []
    if paper.doi:
        keys.append(f"doi:{paper.doi.strip().lower()}")
    if paper.kci_id:
        keys.append(f"kci:{paper.kci_id}")
    if paper.oasis_id:
        keys.append(f"oasis:{paper.oasis_id}")
    if paper.pmid:
        keys.append(f"pmid:{paper.pmid}")
    first_author = (paper.authors[0].lower() if paper.authors else "")
    keys.append(f"ty:{normalize_title(paper.title)}|{first_author}|{paper.year}")
    return keys


def _merge_flag(a: bool | None, b: bool | None, *, prefer_true: bool) -> bool | None:
    """Combine a tri-state (True/False/unknown) flag from two sources.

    `prefer_true` picks whether an explicit True or explicit False wins when
    the sources disagree; unknown (None) only wins if both sides are None.
    """
    if a is None:
        return b
    if b is None:
        return a
    if a == b:
        return a
    # a and b disagree (one True, one False): prefer_true picks the winner
    return prefer_true


def _merge_pair(a: Paper, b: Paper) -> Paper:
    """Merge b into a following spec section 11 field-priority rules."""
    merged = a.model_copy(deep=True)

    merged.doi = a.doi or b.doi
    merged.kci_id = a.kci_id or b.kci_id
    merged.oasis_id = a.oasis_id or b.oasis_id
    merged.riss_id = a.riss_id or b.riss_id
    merged.pmid = a.pmid or b.pmid

    merged.journal = a.journal or b.journal
    merged.publisher = a.publisher or b.publisher
    merged.year = a.year or b.year
    merged.volume = a.volume or b.volume
    merged.issue = a.issue or b.issue
    merged.pages = a.pages or b.pages

    # abstract: more complete value wins
    a_abs, b_abs = a.abstract or "", b.abstract or ""
    merged.abstract = a.abstract if len(a_abs) >= len(b_abs) else b.abstract

    merged.authors = a.authors or b.authors
    merged.keywords = sorted(set(a.keywords) | set(b.keywords))
    merged.fields_of_study = sorted(set(a.fields_of_study) | set(b.fields_of_study))

    # KCI citation count is authoritative when present (spec 11)
    merged.citation_count = (
        a.citation_count if "kci" in a.sources and a.citation_count is not None
        else (b.citation_count if "kci" in b.sources and b.citation_count is not None
              else a.citation_count or b.citation_count)
    )
    merged.influential_citation_count = (
        a.influential_citation_count if a.influential_citation_count is not None
        else b.influential_citation_count
    )
    merged.citation_counts_by_year = a.citation_counts_by_year or b.citation_counts_by_year

    merged.study_type = a.study_type or b.study_type
    merged.tldr = a.tldr or b.tldr
    # is_retracted/is_open_access: an explicit flag from either source wins
    # over "unknown" (None); True (retracted) wins over False for safety.
    merged.is_retracted = _merge_flag(a.is_retracted, b.is_retracted, prefer_true=True)
    merged.is_open_access = _merge_flag(a.is_open_access, b.is_open_access, prefer_true=False)

    merged.fulltext_url = a.fulltext_url or b.fulltext_url

    merged.sources = list(dict.fromkeys(a.sources + b.sources))
    merged.source_ranks = {**b.source_ranks, **a.source_ranks}
    return merged


def merge_source_results(results: dict[str, list[Paper]]) -> list[Paper]:
    """Union-find dedup across per-source ranked result lists, then merge.

    `results` maps source name -> ranked list[Paper] (index 0 = rank 1).
    """
    tagged: list[Paper] = []
    for source, papers in results.items():
        for rank, paper in enumerate(papers, start=1):
            p = paper.model_copy(deep=True)
            p.sources = [source]
            p.source_ranks = {source: rank}
            tagged.append(p)

    parent = list(range(len(tagged)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    key_to_index: dict[str, int] = {}
    for i, paper in enumerate(tagged):
        for key in _identity_keys(paper):
            if key in key_to_index:
                union(key_to_index[key], i)
            else:
                key_to_index[key] = i

    clusters: dict[int, list[int]] = {}
    for i in range(len(tagged)):
        clusters.setdefault(find(i), []).append(i)

    merged_papers: list[Paper] = []
    for indices in clusters.values():
        acc = tagged[indices[0]]
        for i in indices[1:]:
            acc = _merge_pair(acc, tagged[i])
        merged_papers.append(acc)
    return merged_papers
