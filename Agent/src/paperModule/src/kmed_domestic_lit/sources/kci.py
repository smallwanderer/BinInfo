"""KCI (한국학술지인용색인) Open API adapter. spec section 5.1.

Response is XML under `MetaData.outputData.record[*]`. This shape (and the
`articleSearch` field names below) was confirmed against a live response
with a real API key on 2026-08-13 -- see `Agent/kci_raw_response.xml` for
a captured sample. `articleDetail`/`articleReference`/`articleCitation`
(used by fetch/references/citations) are still unverified guesses.
"""
from __future__ import annotations

import hashlib

import httpx
import xmltodict

from ..cache import cache_key, get as cache_get, set as cache_set
from ..config import sources_config
from ..models import Paper
from ..retry import with_backoff

_DOI_PREFIXES = ("https://doi.org/", "http://doi.org/", "http://dx.doi.org/", "https://dx.doi.org/")


def _uid(kci_id: str | None, title: str) -> str:
    return "kci:" + (kci_id or hashlib.md5(title.encode()).hexdigest()[:12])


def _as_list(x) -> list:
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def _text(node) -> str:
    if isinstance(node, dict):
        return (node.get("#text") or "").strip()
    if isinstance(node, str):
        return node.strip()
    return ""


def _pick_title(title_group: dict | None) -> str:
    by_lang: dict[str, str] = {}
    for t in _as_list((title_group or {}).get("article-title")):
        lang = t.get("@lang") if isinstance(t, dict) else None
        by_lang[lang or "original"] = _text(t)
    return by_lang.get("original") or by_lang.get("foreign") or by_lang.get("english") or ""


def _pick_abstract(abstract_group: dict | None) -> str | None:
    by_lang: dict[str, str] = {}
    for a in _as_list((abstract_group or {}).get("abstract")):
        lang = a.get("@lang") if isinstance(a, dict) else None
        by_lang[lang or "original"] = _text(a)
    return by_lang.get("original") or by_lang.get("english") or None


def _authors(author_group: dict | None) -> list[str]:
    names = []
    for a in _as_list((author_group or {}).get("author")):
        raw = a if isinstance(a, str) else _text(a)
        name = raw.split("(")[0].strip()  # strip trailing "(소속기관)"
        if name:
            names.append(name)
    return names


def _clean_doi(raw: str | None) -> str | None:
    if not raw:
        return None
    text = raw.strip()
    lowered = text.lower()
    for prefix in _DOI_PREFIXES:
        if lowered.startswith(prefix):
            return text[len(prefix):]
    return text or None


def _to_paper(record: dict) -> Paper:
    journal_info = record.get("journalInfo") or {}
    article = record.get("articleInfo") or {}

    kci_id = article.get("@article-id")
    title = _pick_title(article.get("title-group"))

    year_str = journal_info.get("pub-year")
    year = int(year_str) if str(year_str or "").isdigit() else None

    fpage, lpage = article.get("fpage"), article.get("lpage")
    pages = f"{fpage}-{lpage}" if fpage and lpage else (fpage or None)

    category = article.get("article-categories")
    citation_count = int(cc) if str(cc := article.get("citation-count")).isdigit() else None

    return Paper(
        uid=_uid(kci_id, title),
        kci_id=kci_id,
        doi=_clean_doi(article.get("doi")),
        title=title,
        authors=_authors(article.get("author-group")),
        journal=journal_info.get("journal-name"),
        publisher=journal_info.get("publisher-name"),
        year=year,
        volume=journal_info.get("volume"),
        issue=journal_info.get("issue"),
        pages=pages,
        abstract=_pick_abstract(article.get("abstract-group")),
        fields_of_study=[category] if category else [],
        citation_count=citation_count,
        fulltext_url=article.get("url") or None,
        sources=["kci"],
    )


class KCIAdapter:
    name = "kci"

    def __init__(self):
        cfg = sources_config()["sources"]["kci"]
        self.enabled = cfg.get("enabled", False) and bool(cfg.get("api_key"))
        self.base_url = cfg["base_url"]
        self.api_key = cfg.get("api_key", "")

    async def _call(self, api_code: str, **params) -> list[dict]:
        if not self.enabled:
            return []
        query = {"apiCode": api_code, "key": self.api_key, **params}
        key = cache_key("kci", api_code, str(sorted(query.items())))
        cached = cache_get(key)
        if cached is not None:
            return cached

        async with httpx.AsyncClient(timeout=15) as client:

            async def _call():
                resp = await client.get(self.base_url, params=query)
                resp.raise_for_status()
                return resp.text

            text = await with_backoff(_call)
        parsed = xmltodict.parse(text)
        records = _as_list(parsed.get("MetaData", {}).get("outputData", {}).get("record"))
        cache_set(key, records, kind="search_result")
        return records

    async def search(self, query: str, limit: int = 50, **filters) -> list[Paper]:
        params = {"title": query, "displayCount": limit}
        if filters.get("year_from"):
            params["fromYear"] = filters["year_from"]
        if filters.get("year_to"):
            params["toYear"] = filters["year_to"]
        if filters.get("journal"):
            params["journalName"] = filters["journal"]
        records = await self._call("articleSearch", **params)
        return [_to_paper(r) for r in records]

    async def fetch(self, ids: list[str]) -> list[Paper]:
        papers = []
        for kci_id in ids:
            records = await self._call("articleDetail", papId=kci_id)
            papers.extend(_to_paper(r) for r in records)
        return papers

    async def references(self, uid: str, limit: int = 50) -> list[Paper]:
        records = await self._call("articleReference", papId=uid, displayCount=limit)
        return [_to_paper(r) for r in records]

    async def citations(self, uid: str, limit: int = 50) -> list[Paper]:
        records = await self._call("articleCitation", papId=uid, displayCount=limit)
        return [_to_paper(r) for r in records]
