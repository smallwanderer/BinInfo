"""Final Answer (Layer 5). Combines PaperQA2's per-topic grounded answers
into one coherent answer to the user's original question.

The per-topic answers are already evidence-grounded (that verification
happened in Layer 4), so this step's job is reorganizing/translating them
for the user, not re-deriving facts -- it doesn't need to be as paranoid
about "zero new claims" as an from-scratch synthesis would. It should still
avoid inventing specific findings/numbers the sources don't support.
"""
from __future__ import annotations

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from ..capabilities import mentions_unsupported_constraint
from .usage import extract_usage

_PROMPT = """
You are writing the final research answer based on already-verified,
citation-grounded partial answers.

Original user question:
{question}

Partial answers:
{topic_answers}

Write the entire answer in the SAME LANGUAGE as the original user question.

Write a natural, coherent, and sufficiently detailed answer that directly answers
the question.

Requirements:
- Begin with the main takeaway, then explain the supporting evidence.
- Synthesize the partial answers rather than concatenating them.
- Preserve meaningful differences between outcomes, populations, study types,
  or other important aspects.
- Explain conflicting, limited, or uncertain evidence when relevant.
- Mention important limitations or unanswered parts.
- Do not invent claims, statistics, or conclusions not supported by the partial answers.
- Avoid overly terse or report-like phrasing.
- Use headings or bullets when they improve readability.

Citations:
- Cite important evidence-based claims using only sources already present in the partial answers.
- Use numbered Markdown footnotes such as [^1], [^2].
- Place citations immediately after the claims they support.
- Reuse the same footnote for the same source.
- List the corresponding footnotes at the end using the available bibliographic information.
- Never invent missing sources or bibliographic details.

Use a structure appropriate to the question.
"""


class FinalAnswerResult(BaseModel):
    answer: str = Field(description="One coherent final answer combining the given partial answers")


def _format_topic_answers(topic_answers: dict[str, str]) -> str:
    return "\n\n".join(f"[{topic}]\n{answer}" for topic, answer in topic_answers.items())


async def synthesize_final_answer(
    question: str,
    topic_answers: dict[str, str],
    unfillable_constraints: list[str] | None = None,
    model: str = "gpt-4o-mini",
) -> tuple[str, dict]:
    llm = ChatOpenAI(model=model).with_structured_output(FinalAnswerResult, include_raw=True)
    prompt = _PROMPT.format(question=question, topic_answers=_format_topic_answers(topic_answers))
    raw = await llm.ainvoke(prompt)
    answer = raw["parsed"].answer

    # Deterministic disclaimer for unfillable constraints (e.g. Impact
    # Factor) -- same registry/pattern as graph.py's ask(). Don't rely on
    # the LLM to remember to disclose data it doesn't have; it has already
    # been shown to silently drop such instructions under load.
    for label in unfillable_constraints or []:
        if mentions_unsupported_constraint(label):
            answer = (
                f"⚠️ 이 시스템은 다음 조건을 확인할 데이터가 없습니다: {label}. "
                f"아래 답변은 이 조건과 무관하게 작성되었습니다.\n\n"
            ) + answer

    return answer, extract_usage(raw["raw"])
