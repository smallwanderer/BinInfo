"""OASIS (한국한의학연구원 전통의학정보포털) adapter. spec section 5.3.

Structure-only placeholder: as of this writing there is no confirmed
official Open API for OASIS paper search (the public-data-portal
datasets under KIOM's name only cover 연구과제/약재 정보, not article
bibliographic search), and the spec explicitly rules out unofficial
web scraping as the default implementation (spec section 5.3, 26).

This adapter is wired into the Fast Search pipeline like `KCIAdapter`
so that enabling OASIS later is a config change, not a pipeline change.
Until one of the spec section 5.3 후속 조건 is met (official Open API,
institutional data-sharing agreement, approved export, or ToS-permitted
mechanical access), every method is a no-op returning empty results.
"""
from __future__ import annotations

from ..config import sources_config
from ..models import Paper


class OASISAdapter:
    name = "oasis"

    def __init__(self):
        cfg = sources_config()["sources"].get("oasis", {})
        self.enabled = cfg.get("enabled", False)
        self.base_url = cfg.get("base_url")
        self.api_key = cfg.get("api_key")

    async def search(self, query: str, limit: int = 50, **filters) -> list[Paper]:
        return []

    async def fetch(self, ids: list[str]) -> list[Paper]:
        return []

    async def references(self, uid: str, limit: int = 50) -> list[Paper]:
        return []

    async def citations(self, uid: str, limit: int = 50) -> list[Paper]:
        return []
