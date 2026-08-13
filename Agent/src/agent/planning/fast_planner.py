"""Fast stage planning: Entry Agent + Query Builder. See agent-docs/planner-v2.md §3.

Kept as two separate calls rather than merged into one — crowding goal/
constraint extraction together with query decomposition was observed to
drop constraints (e.g. an explicit IF condition) under a single prompt.
"""
from __future__ import annotations

from langchain_openai import ChatOpenAI

from .models import EntryAgentResult, QueryBuilderResult
from .usage import extract_usage

_ENTRY_AGENT_PROMPT = """
Analyze the user's literature-search request.

Extract:
- goal: what the user wants to find or know
- constraints: every explicit condition the user stated (year, journal,
  study type, impact factor, anything). List all of them here regardless
  of whether you think the system can apply them -- that check happens
  separately, after this step, in code.

Preserve the user's intent. Do not invent constraints the user didn't state.

User query:
{query}
"""

_QUERY_BUILDER_PROMPT = """
Expand the literature-search goal into 2–4 parallel search topics.

For each topic, produce: topic, kci, pubmed (see each field's own
description for its format -- kci and pubmed have different constraints).

Rules:
- Topics should broaden recall without changing the user's goal.
- Avoid redundant topics.

For KCI:
- Prefer 1–2 keywords per query.
- Because space-separated terms are AND-matched, avoid combining synonyms in one query.
- Put alternative disease/treatment terms into separate parallel queries.
- Use 3 keywords only when all three are likely to co-occur in real article titles.

Goal:
{goal}
Constraint:
{constraints}
"""


async def entry_agent(query: str, model: str = "gpt-4o-mini") -> tuple[EntryAgentResult, dict]:
    llm = ChatOpenAI(model=model).with_structured_output(EntryAgentResult, include_raw=True)
    raw = await llm.ainvoke(_ENTRY_AGENT_PROMPT.format(query=query))
    return raw["parsed"], extract_usage(raw["raw"])


async def query_builder(
    goal: str, constraints: list[str] | None = None, model: str = "gpt-4o-mini"
) -> tuple[QueryBuilderResult, dict]:
    llm = ChatOpenAI(model=model).with_structured_output(QueryBuilderResult, include_raw=True)
    prompt = _QUERY_BUILDER_PROMPT.format(goal=goal, constraints=constraints or [])
    raw = await llm.ainvoke(prompt)
    return raw["parsed"], extract_usage(raw["raw"])
