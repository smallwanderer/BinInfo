"""Token usage extraction for structured-output LLM calls made with
`with_structured_output(..., include_raw=True)`."""
from __future__ import annotations


def extract_usage(raw_message) -> dict:
    meta = getattr(raw_message, "usage_metadata", None) or {}
    return {
        "input_tokens": meta.get("input_tokens", 0),
        "output_tokens": meta.get("output_tokens", 0),
        "total_tokens": meta.get("total_tokens", 0),
    }


def sum_usage(*usages: dict) -> dict:
    return {
        "input_tokens": sum(u.get("input_tokens", 0) for u in usages),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usages),
        "total_tokens": sum(u.get("total_tokens", 0) for u in usages),
    }
