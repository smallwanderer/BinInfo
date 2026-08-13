"""Shared pydantic models: spec section 8, 15, 19."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Paper(BaseModel):
    uid: str

    doi: str | None = None
    kci_id: str | None = None
    oasis_id: str | None = None
    riss_id: str | None = None
    pmid: str | None = None

    title: str
    authors: list[str] = Field(default_factory=list)
    journal: str | None = None
    publisher: str | None = None

    year: int | None = None
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None

    abstract: str | None = None
    keywords: list[str] = Field(default_factory=list)
    fields_of_study: list[str] = Field(default_factory=list)

    # Evidence-quality signals. None means "unknown / not checked" — no
    # currently-wired source (KCI, PubMed) populates these, so they stay
    # unset rather than fabricated. Left in place for sources that do
    # (e.g. Semantic Scholar-style retraction/OA metadata) later.
    study_type: str | None = None  # e.g. RCT / meta-analysis / systematic-review / case-report / animal-study
    is_retracted: bool | None = None
    is_open_access: bool | None = None

    citation_count: int | None = None
    influential_citation_count: int | None = None
    citation_counts_by_year: dict[int, int] = Field(default_factory=dict)

    tldr: str | None = None

    fulltext_url: str | None = None

    sources: list[str] = Field(default_factory=list)
    source_ranks: dict[str, int] = Field(default_factory=dict)


class PaperCard(BaseModel):
    uid: str

    title: str
    authors: list[str] = Field(default_factory=list)
    authors_short: str
    journal: str | None = None
    year: int | None = None

    doi: str | None = None
    kci_id: str | None = None
    pmid: str | None = None

    score: float
    citation_count: int | None = None
    influential_citation_count: int | None = None

    study_type: str | None = None
    is_retracted: bool | None = None
    is_open_access: bool | None = None
    tldr: str | None = None

    matched_query: str
    sources: list[str]
    source_ranks: dict[str, int]

    abstract: str | None = None
    fulltext_url: str | None = None


class Evidence(BaseModel):
    uid: str
    quote: str
    source: str = "paperqa"


class ResearchReport(BaseModel):
    question: str
    summary: str

    key_papers: list[PaperCard] = Field(default_factory=list)
    key_findings: list[str] = Field(default_factory=list)
    agreements: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)

    queries_used: list[str] = Field(default_factory=list)
    search_iterations: int = 0
    evidence_uids: list[str] = Field(default_factory=list)


def paper_to_card(paper: Paper, score: float, matched_query: str) -> PaperCard:
    authors_short = paper.authors[0] + " 외" if len(paper.authors) > 1 else (
        paper.authors[0] if paper.authors else ""
    )
    return PaperCard(
        uid=paper.uid,
        title=paper.title,
        authors=paper.authors,
        authors_short=authors_short,
        journal=paper.journal,
        year=paper.year,
        doi=paper.doi,
        kci_id=paper.kci_id,
        pmid=paper.pmid,
        score=round(score, 4),
        citation_count=paper.citation_count,
        influential_citation_count=paper.influential_citation_count,
        study_type=paper.study_type,
        is_retracted=paper.is_retracted,
        is_open_access=paper.is_open_access,
        tldr=paper.tldr,
        matched_query=matched_query,
        sources=paper.sources,
        source_ranks=paper.source_ranks,
        abstract=paper.abstract,
        fulltext_url=paper.fulltext_url,
    )
