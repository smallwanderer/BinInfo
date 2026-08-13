"""SQLite-backed TTL cache (spec section 23) via diskcache."""
from __future__ import annotations

from pathlib import Path

import diskcache

from .config import sources_config

_cfg = sources_config().get("cache", {})
_DIR = Path(__file__).resolve().parents[2] / _cfg.get("dir", ".cache")
_TTL = _cfg.get("ttl_seconds", {})

_cache = diskcache.Cache(str(_DIR))


def cache_key(namespace: str, *parts: str) -> str:
    return namespace + ":" + "|".join(parts)


def get(key: str):
    return _cache.get(key, default=None)


def set(key: str, value, kind: str = "search_result") -> None:
    _cache.set(key, value, expire=_TTL.get(kind, 86400))
