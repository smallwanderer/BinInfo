"""PaperQA2 evidence engine adapter. spec section 17.

Ingestion / chunking / retrieval / citation-grounded synthesis are all
delegated to `paper-qa`; we only feed it abstracts (spec section 18
fallback) since automated full-text scraping is out of scope for V1.

`PaperQASession` keeps one `Docs` instance alive across a whole Deep
Research session so papers found in later rounds get added incrementally
(no duplicate re-ingestion of already-added papers) and can be queried
per-aspect/topic rather than with one compound question. See
agent-docs/planner-v2.md §3 "PaperQA2 — 공유 ingest + aspect별 query".
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from ..models import Evidence, Paper


def _paperqa_usage(answer) -> dict:
    """paper-qa's PQASession exposes its own cost/token_counts (per
    model-name key: [input, output]) -- surface it in our usual shape so
    callers can fold PaperQA2's cost (the most expensive part of a Deep
    round) into a pipeline-wide total instead of it silently going
    untracked."""
    counts = getattr(answer, "token_counts", None) or {}
    input_tokens = sum(v[0] for v in counts.values())
    output_tokens = sum(v[1] for v in counts.values())
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cost": getattr(answer, "cost", 0.0),
    }


class PaperQASession:
    def __init__(self, model: str = "gpt-4o-mini", evidence_k: int = 10):
        try:
            from paperqa import Docs
            from paperqa.settings import Settings
        except ImportError as exc:
            raise RuntimeError("paper-qa가 설치되어 있지 않습니다: pip install paper-qa") from exc

        self.docs = Docs()
        self._settings = Settings(
            # paper-qa defaults both to full gpt-4o -- ~15x the per-token
            # cost of gpt-4o-mini, and it's what dominates a Deep Research
            # round's cost/latency (measured: ~9k tokens, ~$0.036, ~10s per
            # topic query). llm = final answer synthesis, summary_llm = the
            # per-chunk RCS summarization (the bulk of the token volume).
            llm=model,
            summary_llm=model,
            # Default is True: paper-qa calls out to Semantic Scholar/Crossref
            # per-document during aadd() to "enrich" metadata. We already pass
            # a full citation string ourselves, so this is redundant -- and it
            # was observed to trip the same S2 rate limit our own citation
            # lookups use, on top of them (see pubmed.py's S2 calls).
            parsing={"use_doc_details": False},
            # How many top-ranked passages get retrieved+summarized per
            # query (paper-qa's own passage-level relevance judgment, a
            # different/finer granularity than our paper-level Relevance
            # Screen). Default 10.
            answer={"evidence_k": evidence_k},
        )
        self._ingested_uids: set[str] = set()
        self._tmp_dir = tempfile.TemporaryDirectory()

    async def ingest(self, papers: list[Paper]) -> int:
        """Add papers not already in this session (by uid). Returns count
        newly added; papers without an abstract are skipped (nothing to
        ingest)."""
        added = 0
        for paper in papers:
            if paper.uid in self._ingested_uids or not paper.abstract:
                continue
            path = Path(self._tmp_dir.name) / f"{paper.uid.replace(':', '_')}.txt"
            path.write_text(f"{paper.title}\n\n{paper.abstract}", encoding="utf-8")
            citation = (
                f"{', '.join(paper.authors[:3]) or '저자 미상'} "
                f"({paper.year or 'n.d.'}). {paper.title}. {paper.journal or ''}"
            )
            await self.docs.aadd(path, citation=citation, docname=paper.uid, settings=self._settings)
            self._ingested_uids.add(paper.uid)
            added += 1
        return added

    async def ask(self, question: str) -> tuple[str, list[Evidence], dict]:
        empty_usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "cost": 0.0}
        if not self._ingested_uids:
            return "근거로 사용할 초록/원문을 확보하지 못했습니다.", [], empty_usage

        answer = await self.docs.aquery(question, settings=self._settings)
        evidence = [
            Evidence(uid=getattr(getattr(ctx.text, "doc", None), "docname", "unknown"), quote=ctx.context)
            for ctx in getattr(answer, "contexts", [])
        ]
        return answer.formatted_answer, evidence, _paperqa_usage(answer)

    def close(self) -> None:
        self._tmp_dir.cleanup()

    async def __aenter__(self) -> "PaperQASession":
        return self

    async def __aexit__(self, *exc_info) -> None:
        self.close()


async def run_paperqa(question: str, papers: list[Paper]) -> tuple[str, list[Evidence]]:
    """One-shot convenience wrapper (ingest once, ask once) for callers that
    don't need a multi-round session -- e.g. deep/research.py's current
    single-question use. Drops the usage info ask() now returns, to keep
    this function's original 2-tuple contract."""
    async with PaperQASession() as session:
        await session.ingest(papers)
        answer, evidence, _usage = await session.ask(question)
        return answer, evidence
