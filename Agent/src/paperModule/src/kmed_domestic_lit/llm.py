"""Thin OpenAI wrapper used only for Deep Research query reformulation.
Returns None (caller falls back to a no-op) when no API key is configured.
"""
from __future__ import annotations

import os

_client = None


def _get_client():
    global _client
    if _client is None and os.environ.get("OPENAI_API_KEY"):
        from openai import AsyncOpenAI

        _client = AsyncOpenAI()
    return _client


async def complete(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 512) -> str | None:
    client = _get_client()
    if client is None:
        return None
    resp = await client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content

