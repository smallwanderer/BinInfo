"""Relevance Screen (Layer 3). See agent-docs/planner-v2.md §3.

One LLM call over the whole candidate pool, but judgment stays per-topic --
each candidate is tagged against every topic individually rather than a
single holistic yes/no, so a paper that only covers one topic (e.g. safety)
doesn't get dropped by a coarse "is this relevant overall" judgment.
"""
from __future__ import annotations

from langchain_openai import ChatOpenAI

from .models import RelevanceScreenResult
from .usage import extract_usage

_ABSTRACT_CHARS = 400

_PROMPT = """You are screening literature search candidates.

Topics (the user's parallel information needs):
{topics}

Constraints (conditions the results must satisfy, independent of topic):
{constraints}

For each candidate below, make TWO separate judgments -- keep them separate,
a candidate's topic relevance does not affect its constraint check or vice
versa:

1. relevant_to: which of the topics above it is actually relevant to (zero,
   one, or several -- judge each topic independently, from the title/abstract
   content, not just because it was returned by a search for that topic).

2. unmet_constraints: which of the constraints above this candidate FAILS to
   satisfy, or that you cannot verify from the fields given (year, journal,
   abstract). Empty list if it satisfies all constraints, or if there are no
   constraints. If you cannot actually check a constraint from the given
   data, list it as unmet -- never assume a constraint is satisfied without
   evidence.

Candidates:
{candidates}
"""


def _format_candidates(candidates: list[dict]) -> str:
    lines = []
    for c in candidates:
        abstract = (c.get("abstract") or "")[:_ABSTRACT_CHARS]
        lines.append(
            f"- uid: {c['uid']}\n  title: {c.get('title')}\n  year: {c.get('year')}\n"
            f"  journal: {c.get('journal')}\n  abstract: {abstract}"
        )
    return "\n".join(lines)


async def relevance_screen(
    topics: list[str],
    candidates: list[dict],
    constraints: list[str] | None = None,
    model: str = "gpt-4o-mini",
) -> tuple[RelevanceScreenResult, dict]:
    llm = ChatOpenAI(model=model).with_structured_output(RelevanceScreenResult, include_raw=True)
    prompt = _PROMPT.format(
        topics="\n".join(f"- {t}" for t in topics),
        constraints="\n".join(f"- {c}" for c in constraints) if constraints else "(none)",
        candidates=_format_candidates(candidates),
    )
    raw = await llm.ainvoke(prompt)
    return raw["parsed"], extract_usage(raw["raw"])


def finalize_pool(screened: list[dict]) -> list[dict]:
    """Screened Pool: deterministic (no LLM) post-processing shared by both
    consumers -- the Fast response returns this list as-is, and Deep uses
    the same list as its PaperQA2 ingestion seed. Doing the filtering once
    here means an irrelevant candidate can't leak into either path.

    - drop candidates the Relevance Screen didn't tag to any topic
    - drop candidates with any unmet_constraints (fillable constraints the
      candidate failed, or that couldn't be verified from its data)
    - sort by score (KCI/PubMed both already carry one from their own Fast
      Search ranking pass), breaking ties by how many topics it covers
    """
    relevant = [c for c in screened if c.get("relevant_to") and not c.get("unmet_constraints")]
    return sorted(
        relevant,
        key=lambda c: (c.get("score") or 0, len(c.get("relevant_to", []))),
        reverse=True,
    )
