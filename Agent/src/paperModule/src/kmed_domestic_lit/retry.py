"""Exponential backoff retry for external API calls. spec section 24
("특정 source가 실패하더라도 전체 검색이 실패하지 않도록 한다") -- this is
the piece that keeps a transient rate limit (e.g. the 429 hit against
Semantic Scholar during testing) from taking down the whole search.
"""
from __future__ import annotations

import asyncio
import random
from typing import Awaitable, Callable, TypeVar

import httpx

RETRYABLE_STATUS = {429, 500, 502, 503, 504}

T = TypeVar("T")


async def with_backoff(
    call: Callable[[], Awaitable[T]],
    *,
    max_retries: int = 4,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> T:
    """Run an async zero-arg callable, retrying on rate limits / transient
    server errors with exponential backoff + jitter. Honors a numeric
    Retry-After header when the server sends one (common on 429s). Any
    other exception, or exhausting max_retries, propagates as-is.
    """
    attempt = 0
    while True:
        try:
            return await call()
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status not in RETRYABLE_STATUS or attempt >= max_retries:
                raise
            retry_after = exc.response.headers.get("retry-after")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else min(
                base_delay * (2**attempt), max_delay
            )
            delay += random.uniform(0, delay * 0.25)
            await asyncio.sleep(delay)
            attempt += 1
