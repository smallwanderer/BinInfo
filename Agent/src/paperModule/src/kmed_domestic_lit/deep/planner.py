"""Evidence-gap judgement + Korean query reformulation. spec section 16."""
from __future__ import annotations

from ..llm import complete

_REFORMULATE_PROMPT = """Analyze the following research question and candidate paper titles for Korean medicine literature search.

Question: {question}

Candidate Paper Titles Currently Gathered:
{titles}

The current evidence is insufficient. Generate exactly 3 additional Korean search query strings to complement the evidence.
Output one query per line. Output ONLY the query strings without any extra explanation, numbers, or bullet points."""


def is_evidence_sufficient(paper_count: int, min_evidence_papers: int) -> bool:
    return paper_count >= min_evidence_papers


async def reformulate_queries(question: str, seed_titles: list[str], model: str) -> list[str]:
    titles = "\n".join(f"- {t}" for t in seed_titles[:10]) or "(없음)"
    text = await complete(_REFORMULATE_PROMPT.format(question=question, titles=titles), model)
    if not text:
        return []
    lines = [line.lstrip("-• ").strip() for line in text.splitlines()]
    return [line for line in lines if line][:3]
