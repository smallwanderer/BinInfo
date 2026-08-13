"""Deep Research orchestrator. spec section 15.2, 16."""
from __future__ import annotations

from ..config import deep_research_config
from ..fast.search import fast_search
from ..models import PaperCard, ResearchReport
from ..sources.base import SourceAdapter
from .paperqa_adapter import run_paperqa
from .planner import is_evidence_sufficient, reformulate_queries


async def research_literature(
    question: str,
    seed_uids: list[str] | None = None,
    sources: list[SourceAdapter] | None = None,
) -> ResearchReport:
    cfg = deep_research_config()
    queries_used = [question]

    seed_cards = await fast_search(question, k=cfg["seed_k"], sources=sources)
    pool: dict[str, PaperCard] = {c.uid: c for c in seed_cards}

    iterations = 0
    while (
        not is_evidence_sufficient(len(pool), cfg["min_evidence_papers"])
        and iterations < cfg["max_iterations"]
    ):
        iterations += 1
        new_queries = await reformulate_queries(
            question, [c.title for c in pool.values()], cfg["llm_model"]
        )
        if not new_queries:
            break
        for q in new_queries:
            queries_used.append(q)
            for card in await fast_search(q, k=cfg["seed_k"], sources=sources):
                pool.setdefault(card.uid, card)

    key_papers = sorted(pool.values(), key=lambda c: c.score, reverse=True)[: cfg["seed_k"]]
    summary, evidence = await run_paperqa(
        question,
        [_card_to_paper(c) for c in key_papers],
    )

    return ResearchReport(
        question=question,
        summary=summary,
        key_papers=key_papers,
        evidence=evidence,
        queries_used=queries_used,
        search_iterations=iterations,
        evidence_uids=[e.uid for e in evidence],
    )


def _card_to_paper(card: PaperCard):
    from ..models import Paper

    return Paper(
        uid=card.uid,
        doi=card.doi,
        kci_id=card.kci_id,
        title=card.title,
        journal=card.journal,
        year=card.year,
        abstract=card.abstract,
        citation_count=card.citation_count,
        fulltext_url=card.fulltext_url,
        sources=card.sources,
        source_ranks=card.source_ranks,
    )
