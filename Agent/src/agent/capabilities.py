"""Deterministic registry of query constraints this system's tools cannot
fulfill. Checked by code, not by LLM prompt compliance.

Why: classifying "can this constraint be met" was originally the Entry
Agent's job via prompt instructions, but that broke across prompt rewordings
(the IF/Impact Factor constraint silently stopped being flagged once the
explicit instruction was trimmed). This is a fact about the system's current
tools, not something that needs judgment, so it belongs in code that every
caller shares -- see graph.py's `ask()` for the other place this used to be
duplicated as its own regex.
"""
from __future__ import annotations

import re

UNSUPPORTED_CONSTRAINTS: dict[str, re.Pattern] = {
    "Impact Factor(IF)": re.compile(r"\bIF\b|impact factor|임팩트\s*팩터", re.IGNORECASE),
}


def classify_constraints(constraints: list[str]) -> tuple[list[str], list[str]]:
    """Split constraints into (fillable, unfillable) via the registry above."""
    fillable, unfillable = [], []
    for c in constraints:
        if any(p.search(c) for p in UNSUPPORTED_CONSTRAINTS.values()):
            unfillable.append(c)
        else:
            fillable.append(c)
    return fillable, unfillable


def mentions_unsupported_constraint(text: str) -> bool:
    """True if `text` (e.g. a raw user question) mentions any registered
    unsupported constraint, regardless of whether it was explicitly parsed
    out as a constraint. Used as a last-resort disclaimer trigger."""
    return any(p.search(text) for p in UNSUPPORTED_CONSTRAINTS.values())
