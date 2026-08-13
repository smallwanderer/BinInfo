"""PubMed (NCBI E-utilities) source adapter. spec section 5.2.

Provides full PubMed integration for paperModule, creating `Paper` objects
with `uid=pubmed:{pmid}` and `sources=["pubmed"]`.
"""
from __future__ import annotations

import os

import httpx
import xmltodict

from ..cache import cache_key, get as cache_get, set as cache_set
from ..config import sources_config
from ..models import Paper
from ..retry import with_backoff

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
S2_BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper"
S2_RELATED_FIELDS = "title,abstract,year,authors,venue,externalIds,citationCount"


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


def _parse_article(article: dict) -> Paper | None:
    medline = article.get("MedlineCitation")
    if not medline:
        return None
    pmid = _text(medline.get("PMID")) or str(medline.get("PMID"))
    if not pmid:
        return None

    art = medline.get("Article") or {}
    title = _text(art.get("ArticleTitle"))

    abstract_node = (art.get("Abstract") or {}).get("AbstractText")
    abstract_parts = [_text(a) for a in _as_list(abstract_node)]
    abstract = " ".join(p for p in abstract_parts if p) or None

    journal = (art.get("Journal") or {}).get("Title")

    pub_date = ((art.get("Journal") or {}).get("JournalIssue") or {}).get("PubDate") or {}
    year_str = pub_date.get("Year") if isinstance(pub_date, dict) else None
    year = int(year_str) if year_str and year_str.isdigit() else None

    authors = []
    for a in _as_list((art.get("AuthorList") or {}).get("Author")):
        if not isinstance(a, dict):
            continue
        name = f"{a.get('LastName', '')} {a.get('ForeName', '')}".strip()
        if name:
            authors.append(name)

    doi = None
    for e in _as_list(art.get("ELocationID")):
        if isinstance(e, dict) and e.get("@EIdType") == "doi":
            doi = _text(e)

    return Paper(
        uid=f"pubmed:{pmid}",
        pmid=pmid,
        doi=doi,
        title=title,
        authors=authors,
        journal=journal,
        year=year,
        abstract=abstract,
        fulltext_url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        sources=["pubmed"],
    )


async def _fetch_citation_counts(
    client: httpx.AsyncClient, pmids: list[str], api_key: str | None
) -> dict[str, int]:
    """PubMed itself doesn't track citation counts -- look them up in one
    batched call to Semantic Scholar instead. A PMID absent from the
    returned dict means "unknown" (S2 has no match), never fabricated 0."""
    if not pmids:
        return {}
    headers = {"x-api-key": api_key} if api_key else {}

    async def _call():
        resp = await client.post(
            S2_BATCH_URL,
            params={"fields": "citationCount"},
            json={"ids": [f"PMID:{p}" for p in pmids]},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()

    data = await with_backoff(_call)
    return {
        pmid: item["citationCount"]
        for pmid, item in zip(pmids, data)
        if item is not None and item.get("citationCount") is not None
    }


def _s2_paper_to_paper(item: dict | None) -> Paper | None:
    if not item or not item.get("title"):
        return None
    external_ids = item.get("externalIds") or {}
    pmid = external_ids.get("PubMed")
    authors = [a.get("name", "") for a in (item.get("authors") or []) if a.get("name")]
    uid = f"pubmed:{pmid}" if pmid else f"s2:{item.get('paperId')}"
    return Paper(
        uid=uid,
        pmid=pmid,
        doi=external_ids.get("DOI"),
        title=item["title"],
        authors=authors,
        journal=item.get("venue") or None,
        year=item.get("year"),
        abstract=item.get("abstract"),
        citation_count=item.get("citationCount"),
        fulltext_url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
        sources=["pubmed"] if pmid else ["semanticscholar"],
    )


async def _fetch_related(
    client: httpx.AsyncClient, pmid: str, relation: str, limit: int, api_key: str | None
) -> list[Paper]:
    """Citation Traversal: papers citing (`relation="citations"`) or cited
    by (`relation="references"`) a PubMed paper, via Semantic Scholar's
    citation graph. Single page up to `limit` (S2 caps at 1000) -- this is
    for recall expansion on a handful of already-promising papers, not for
    computing an exact citation count (see `_fetch_citation_counts`, which
    is far cheaper per-paper and used for that instead).
    """
    headers = {"x-api-key": api_key} if api_key else {}
    key_field = "citingPaper" if relation == "citations" else "citedPaper"

    async def _call():
        resp = await client.get(
            f"{S2_PAPER_URL}/PMID:{pmid}/{relation}",
            params={"fields": S2_RELATED_FIELDS, "limit": min(limit, 1000)},
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json()

    data = await with_backoff(_call)
    papers = []
    for entry in data.get("data", []):
        p = _s2_paper_to_paper(entry.get(key_field))
        if p:
            papers.append(p)
    return papers


class PubMedAdapter:
    name = "pubmed"

    def __init__(self):
        cfg = sources_config().get("sources", {}).get("pubmed", {})
        self.enabled = cfg.get("enabled", True)
        self.api_key = cfg.get("api_key") or os.environ.get("PUBMED_API_KEY") or None
        self.s2_api_key = os.environ.get("S2_API_KEY") or None

    async def _esearch(self, client: httpx.AsyncClient, query: str, limit: int) -> list[str]:
        params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": limit, "sort": "relevance"}
        if self.api_key:
            params["api_key"] = self.api_key

        key = cache_key("pubmed", "esearch", f"{query}:{limit}")
        cached = cache_get(key)
        if cached is not None:
            return cached

        async def _call():
            resp = await client.get(ESEARCH_URL, params=params)
            resp.raise_for_status()
            return resp.json()

        ids = (await with_backoff(_call)).get("esearchresult", {}).get("idlist", [])
        cache_set(key, ids, kind="search_result")
        return ids

    async def _efetch(self, client: httpx.AsyncClient, ids: list[str]) -> list[Paper]:
        if not ids:
            return []

        key = cache_key("pubmed", "efetch", ",".join(ids))
        cached = cache_get(key)
        if cached is not None:
            papers = [Paper.model_validate(p) for p in cached]
        else:
            params = {"db": "pubmed", "id": ",".join(ids), "rettype": "abstract", "retmode": "xml"}
            if self.api_key:
                params["api_key"] = self.api_key

            async def _call():
                resp = await client.get(EFETCH_URL, params=params)
                resp.raise_for_status()
                return resp.text

            parsed = xmltodict.parse(await with_backoff(_call))
            articles = _as_list(parsed.get("PubmedArticleSet", {}).get("PubmedArticle"))
            papers = []
            for a in articles:
                p = _parse_article(a)
                if p:
                    papers.append(p)

            cache_set(key, [p.model_dump() for p in papers], kind="metadata")

        # Citation counts get their own short-TTL cache (spec: 7 days) so
        # they refresh independently of the long-lived bibliographic cache
        # above -- otherwise they'd freeze at whatever they were on first
        # fetch, same problem this fix is meant to solve.
        await self._attach_citation_counts(client, papers)
        return papers

    async def _attach_citation_counts(self, client: httpx.AsyncClient, papers: list[Paper]) -> None:
        pmids = [p.pmid for p in papers if p.pmid]
        if not pmids:
            return
        key = cache_key("pubmed", "citations", ",".join(pmids))
        counts = cache_get(key)
        if counts is None:
            try:
                counts = await _fetch_citation_counts(client, pmids, self.s2_api_key)
            except httpx.HTTPError:
                counts = {}
            cache_set(key, counts, kind="citation_count")
        for p in papers:
            if p.pmid in counts:
                p.citation_count = counts[p.pmid]

    async def search(self, query: str, limit: int = 50, **filters) -> list[Paper]:
        if not self.enabled:
            return []
        async with httpx.AsyncClient(timeout=15) as client:
            ids = await self._esearch(client, query, limit)
            return await self._efetch(client, ids)

    async def fetch(self, ids: list[str]) -> list[Paper]:
        if not self.enabled or not ids:
            return []
        clean_ids = [i.replace("pubmed:", "") for i in ids]
        async with httpx.AsyncClient(timeout=15) as client:
            return await self._efetch(client, clean_ids)

    async def references(self, uid: str, limit: int = 50) -> list[Paper]:
        return await self._related(uid, "references", limit)

    async def citations(self, uid: str, limit: int = 50) -> list[Paper]:
        return await self._related(uid, "citations", limit)

    async def _related(self, uid: str, relation: str, limit: int) -> list[Paper]:
        if not self.enabled:
            return []
        pmid = uid.replace("pubmed:", "")
        key = cache_key("pubmed", relation, f"{pmid}:{limit}")
        cached = cache_get(key)
        if cached is not None:
            return [Paper.model_validate(p) for p in cached]

        async with httpx.AsyncClient(timeout=15) as client:
            try:
                papers = await _fetch_related(client, pmid, relation, limit, self.s2_api_key)
            except httpx.HTTPError:
                papers = []
        cache_set(key, [p.model_dump() for p in papers], kind="citation_count")
        return papers
