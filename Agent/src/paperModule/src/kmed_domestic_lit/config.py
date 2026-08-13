"""YAML config loading with ${ENV_VAR} substitution. spec section 23."""
from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"
_ENV_PATTERN = re.compile(r"\$\{(\w+)\}")


def _resolve_env(value):
    if isinstance(value, str):
        m = _ENV_PATTERN.fullmatch(value.strip())
        return os.environ.get(m.group(1), "") if m else value
    if isinstance(value, dict):
        return {k: _resolve_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env(v) for v in value]
    return value


@lru_cache
def load_yaml(name: str) -> dict:
    path = CONFIG_DIR / name
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return _resolve_env(raw)


def sources_config() -> dict:
    return load_yaml("sources.yaml")


def fast_ranking_config() -> dict:
    return load_yaml("fast_ranking.yaml")


def deep_research_config() -> dict:
    return load_yaml("deep_research.yaml")
