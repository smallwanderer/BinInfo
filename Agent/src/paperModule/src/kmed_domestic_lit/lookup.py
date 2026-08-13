"""Single-paper lookups used by the MCP `get_paper` / `get_fulltext` tools."""
from __future__ import annotations

from .models import Paper
from .sources.kci import KCIAdapter

# OASISAdapter exists (sources/oasis.py) but isn't wired in yet: no
# confirmed official API, see spec section 5.3.
_ADAPTERS = {"kci": KCIAdapter}


async def get_paper(uid: str) -> Paper | None:
    source, _, source_id = uid.partition(":")
    adapter_cls = _ADAPTERS.get(source)
    if not adapter_cls:
        return None
    papers = await adapter_cls().fetch([source_id])
    return papers[0] if papers else None


async def get_fulltext(uid: str) -> str | None:
    """V1 has no self-hosted PDF parser (spec section 18/26): returns the
    source-provided full-text URL/abstract fallback, not extracted text."""
    paper = await get_paper(uid)
    if paper is None:
        return None
    return paper.fulltext_url or paper.abstract
