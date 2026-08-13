"""Structured outputs for the Fast planning stage. See agent-docs/planner-v2.md §3."""
from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator

# KCI's title search does a literal substring AND-match on the paper's TITLE
# text only -- space is the implicit AND, and it does not understand boolean
# operator words (writing "AND"/"OR" makes that word itself a required
# substring, matching nothing). Verified empirically 2026-08-13, see
# Agent/snippet/02_result.json.
_BOOLEAN_TOKENS = {"and", "or", "그리고", "또는"}
_MAX_KCI_KEYWORDS = 3
# Tokenize on word characters only (Python's \w is unicode-aware, matches
# Hangul) so punctuation the model adds -- parens, commas, quotes, mimicking
# the PubMed boolean-query style it writes alongside this field -- gets
# stripped instead of surviving into a naive whitespace-split truncation
# (which previously produced mangled output like "(재활치료, 뇌졸중) (침술,").
_WORD_PATTERN = re.compile(r"\w+")


class EntryAgentResult(BaseModel):
    """Extraction only -- whether a constraint is actually fillable by this
    system's current tools is a fact about the system, not something the
    LLM should judge here. See capabilities.classify_constraints(), which
    splits `constraints` deterministically after this call returns."""

    goal: str = Field(description="사용자가 궁극적으로 알고 싶어하는 것을 한 문장으로 요약")
    constraints: list[str] = Field(
        default_factory=list, description="사용자가 명시한 조건 전체 (채울 수 있는지는 이후 별도 검증)"
    )


class SubQuery(BaseModel):
    topic: str = Field(description="하위 정보요구 주제 (예: 효과, 부작용, 적용범위)")
    kci: str = Field(
        description=(
            "KCI 논문 제목 검색어. KCI는 제목 텍스트 안에서 공백으로 구분된 단어들의 "
            "리터럴 부분일치 AND 검색만 지원한다 (공백=AND, 'AND'/'OR' 같은 연산자 단어는 "
            "이해하지 못하고 그 자체가 검색 대상 텍스트로 취급된다). 1~3개의 짧고 흔한 "
            "임상 용어만 공백으로만 구분해서 쓸 것 — 괄호/쉼표/따옴표 등 구두점은 절대 넣지 "
            "말 것 (pubmed 필드의 boolean 문법을 따라하지 말 것). "
            "필수: 격식체/교과서적 동의어는 절대 쓰지 말고 실제 논문 제목에 흔히 쓰이는 "
            "표현으로 바꿀 것 — 예: 뇌혈관질환(후유증) → 뇌졸중, 통증 관리 → 진통, "
            "인지 기능 장애 → 인지장애. 애매하면 더 짧고 더 일상적인 쪽을 선택할 것."
        )
    )
    pubmed: str = Field(description="PubMed에 그대로 넣을 영어 검색어")

    @field_validator("kci")
    @classmethod
    def _enforce_kci_query_shape(cls, value: str) -> str:
        """Deterministic backstop for the description above: don't rely on
        the LLM alone to follow it (see fast_planner.py's history of the
        model conflating this rule with unrelated instructions)."""
        tokens = [t for t in _WORD_PATTERN.findall(value) if t.lower() not in _BOOLEAN_TOKENS]
        return " ".join(tokens[:_MAX_KCI_KEYWORDS])


class QueryBuilderResult(BaseModel):
    sub_queries: list[SubQuery]


class RelevanceTag(BaseModel):
    uid: str = Field(description="The candidate paper's uid, copied exactly as given")
    relevant_to: list[str] = Field(
        default_factory=list,
        description=(
            "Subset of the given topics this paper is actually relevant to "
            "(zero, one, or several). Judge each topic independently."
        ),
    )
    unmet_constraints: list[str] = Field(
        default_factory=list,
        description=(
            "Subset of the given constraints this candidate fails to satisfy, "
            "or that cannot be verified from its year/journal/abstract. Empty "
            "if it satisfies all constraints (or none were given)."
        ),
    )


class RelevanceScreenResult(BaseModel):
    tags: list[RelevanceTag]
