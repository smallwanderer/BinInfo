"""SourceAdapter protocol. spec section 9."""
from __future__ import annotations

from typing import Protocol

from ..models import Paper


class SourceAdapter(Protocol):
    name: str

    async def search(self, query: str, limit: int = 50, **filters) -> list[Paper]: ...

    async def fetch(self, ids: list[str]) -> list[Paper]: ...

    async def references(self, uid: str, limit: int = 50) -> list[Paper]: ...

    async def citations(self, uid: str, limit: int = 50) -> list[Paper]: ...
