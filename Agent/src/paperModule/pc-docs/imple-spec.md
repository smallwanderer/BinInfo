# 한의학 문헌 탐색 에이전트 데모 — 구현 계획서

## 1. 목표

한의학. 환자, 한약과 처방 그리고 성분 관련 자연어 질의를 입력받아 관련 학술 논문을 검색하고, 중복 제거·통합·랭킹한 결과를 다음 두 방식으로 제공하는 데모 시스템을 구현한다.

1. **Agent용 인터페이스**
   - MCP Tool 형태로 상위 신약개발 Agent가 호출
   - 구조화된 `PaperCard[]` 반환

2. **Human용 인터페이스**
   - 연구자가 직접 검색 결과를 확인할 수 있는 Web UI
   - 질의 확장 과정, 논문 목록, 검색 근거, 원문 링크 등을 표시

데모의 핵심은 **문헌 검색 Core를 하나 구현하고, MCP와 Web UI는 동일 Core를 사용하는 얇은 인터페이스로 구성하는 것**이다.

---

## 2. 핵심 설계 원칙

### 2.1 검색 Core와 인터페이스 분리

```text
                    ┌──────────────────────┐
                    │ Literature Search    │
                    │        Core          │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
          [1안] MCP Server            [2안] Web UI
                  │                         │
                  ▼                         ▼
        Drug Discovery Agent            Researcher
```

- MCP와 Web UI가 별도의 검색 로직을 가지지 않는다.
- 검색·정규화·중복 제거·랭킹은 모두 Core에서 수행한다.
- 인터페이스 교체가 검색 시스템 구현에 영향을 주지 않도록 한다.

### 2.2 기존 오픈소스와 무료 API 적극 활용

직접 개발할 가치가 낮은 범용 기능은 재구현하지 않는다.

- 학술 데이터베이스 → KCI, PubMed
- HTTP 통신 → `httpx`
- 데이터 모델 → `Pydantic`
- MCP → 공식 MCP Python SDK
- Human UI → `Streamlit`
- 논문 내부 근거 검색·종합 → 필요 시 `PaperQA2`

직접 개발은 한의학 특화 기능과 검색 orchestration에 집중한다.

---

## 3. 전체 아키텍처

```text
                  User / Drug Discovery Agent
                              │
                              ▼
                          Query Layer
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Domain Normalizer          Query Planner
                 │                         │
                 └────────────┬────────────┘
                              ▼
                  Literature Search Core
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
                KCI                     PubMed
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    Deduplication / Merge
                              │
                              ▼
                          RRF Fusion
                              │
                              ▼
                          Reranking
                              │
                              ▼
                         PaperCard[]
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
          MCP Tool          Web UI         PaperQA2
              │               │             (optional)
              ▼               ▼                │
            Agent         Researcher      Evidence RAG
```

---

## 4. 기존 시스템 및 오픈소스 활용 전략

## 4.1 PaperQA2

### 활용 방향

PaperQA2 전체를 fork하여 검색 시스템으로 개조하지 않는다.

대신 다음 기능이 필요해질 때 **Python dependency 또는 내부 evidence engine**으로 활용한다.

- PDF / full-text 처리
- 문서 chunking
- embedding
- 문서 내부 evidence retrieval
- LLM reranking
- contextual summarization
- citation-grounded synthesis

### 시스템 내 위치

```text
  Core
   │
   ├─ 한의학 용어 정규화
   ├─ Query expansion
   ├─ Europe PMC / OpenAlex / S2 검색
   ├─ 중복 제거
   └─ Top-K 선별
            │
            ▼
         PaperQA2
            │
            ├─ evidence retrieval
            ├─ summarization
            └─ citation-grounded answer
```

### 원칙

- **V1 데모에서는 PaperQA2를 필수 의존성으로 두지 않는다.**
- 검색 품질 검증 후 V1.5에서 연결한다.
- PaperQA2 upstream 변경과 독립적으로 검색 Core를 유지한다.

---

## 4.2 TCM-Agent

TCM-Agent는 한의학/중의학 기반 multi-agent, network pharmacology, target discovery, knowledge graph 등의 상위 구조를 설계할 때 참고한다.

현재 데모의 목표는 TCM-Agent 전체 기능이 아니라 **Literature Retrieval 모듈**이므로 전체 아키텍처를 fork 대상으로 삼지 않는다.

활용 범위:

- 한약·성분·타깃 중심 multi-agent 설계 참고
- 향후 network pharmacology Agent와의 연결 방식 참고
- 상위 Drug Discovery Agent workflow 참고

직접 코드 재사용은 공개 코드와 라이선스 상태를 확인한 후 결정한다.

---

## 5. 직접 개발 범위와 재사용 범위

| 구분 | 기능 | 구현 방식 |
|---|---|---|
| 학술 검색 | Europe PMC | 공개 REST API |
| 학술 검색 | OpenAlex | 공개 REST API |
| 학술 검색 | Semantic Scholar | 공개 API |
| HTTP | 비동기 API 호출 | `httpx`, `asyncio` |
| 데이터 모델 | Paper / PaperCard | `Pydantic` |
| 한의학 용어 | 약재·처방·성분 사전 | **직접 구축** |
| Entity normalization | 한글·한자·영문·라틴명 | **직접 구현** |
| Query expansion | DB별 검색어 생성 | **직접 구현** |
| Deduplication | DOI / PMID / 제목 기반 | **직접 구현** |
| Metadata merge | 소스별 필드 통합 | **직접 구현** |
| 검색 결과 융합 | RRF | **직접 구현** |
| Reranking | 관련도·인용·근거·최신성 | **직접 구현** |
| LLM reranking | 선택적 사용 | 기존 LLM API |
| Agent Interface | MCP | 공식 MCP Python SDK |
| Human Interface | Web UI | Streamlit |
| Evidence RAG | 논문 내부 근거 검색 | PaperQA2, 후속 |
| Citation synthesis | 다중 문헌 근거 종합 | PaperQA2, 후속 |

---

## 6. 데모 기능 범위

### V1 필수

- 자연어 질의 입력
- 한의학 용어 정규화
- 한글 / 한자 / 영문 / 라틴명 / 성분명 확장
- Europe PMC 검색
- OpenAlex 검색
- Semantic Scholar 선택적 검색
- 검색 결과 표준 `Paper` 모델 변환
- DOI / PMID 기반 중복 제거
- metadata 병합
- RRF 기반 검색 결과 융합
- 간단한 reranking
- `PaperCard[]` 생성
- MCP 검색 Tool
- Streamlit Web UI
- 검색 과정 provenance 표시

### V1.5

- PaperQA2 연동
- Full-text 확보
- 논문 내부 evidence retrieval
- 논문 요약
- 질문에 대한 citation-grounded synthesis

### V2 이후

- Citation graph traversal
- 관련 논문 자동 확장
- 복잡한 intent profile
- Network pharmacology Agent 연동
- Target discovery Agent 연동
- Knowledge graph 연동
- 국내 한의학 논문 DB 확장
- CNKI 등 중의학 데이터 소스 연동

---

## 7. 한의학 Domain Layer

## 7.1 용어 사전

`domain/kmed_lexicon.yaml`

예시:

```yaml
- id: HERB:SCUTELLARIA_BAICALENSIS
  type: herb

  ko:
    - 황금
    - 속썩은풀

  hanja:
    - 黃芩

  latin:
    - Scutellaria baicalensis Georgi
    - Scutellariae Radix

  en:
    - Chinese skullcap
    - Baikal skullcap

  compounds:
    - baicalin
    - baicalein
    - wogonin

  mesh:
    - Scutellaria baicalensis
```

처방 예시:

```yaml
- id: FORMULA:YUKMIJIHwang
  type: formula

  ko:
    - 육미지황탕
    - 육미지황환

  hanja:
    - 六味地黃湯

  ko_roman:
    - Yukmijihwang-tang

  zh_roman:
    - Liuwei Dihuang Wan

  ja_roman:
    - Rokumijiogan
```

---

## 7.2 초기 사전 규모

데모에서는 처음부터 대규모 ontology를 구축하지 않는다.

초기 목표:

- 대표 약재: 20~30개
- 대표 처방: 10~20개
- 주요 활성 성분: 30~50개

검색 과정에서 등장한 미등록 표현은 `unmatched.log`에 기록하여 사전 확장 후보로 사용한다.

---

## 7.3 Query expansion 예시

사용자 입력:

```text
황금의 항염 효과
```

정규화:

```text
황금
→ Scutellaria baicalensis
→ Scutellariae Radix
→ baicalin
→ baicalein
→ wogonin
```

DB별 질의 예시:

```text
Europe PMC
("Scutellaria baicalensis" OR "Scutellariae Radix"
 OR baicalin OR baicalein OR wogonin)
AND (inflammation OR anti-inflammatory)

OpenAlex
Scutellaria baicalensis baicalin baicalein inflammation

Semantic Scholar
anti-inflammatory mechanism of Scutellaria baicalensis
```

---

## 8. Query normalization 전략

### 기본 순서

1. 원문 보존
2. 사전 기반 최장 일치
3. Entity type 식별
4. 한의학 동의어·학술명 확장
5. 질병·기전 키워드 분리
6. Source별 query 생성
7. 필요 시 LLM 보조

### LLM 사용 원칙

LLM은 deterministic dictionary를 대체하지 않는다.

주 사용처:

- 미등록 질의 구조화
- 질병 / 기전 / 치료효과 분리
- 영어 학술 검색어 후보 생성
- Top-N reranking

LLM 생성 synonym은 검증 없이 domain lexicon에 자동 반영하지 않는다.

---

## 9. 학술 데이터 소스

## 9.1 Europe PMC

주 역할:

- biomedical literature 검색
- PMID
- abstract
- MeSH
- publication type
- OA 여부
- biomedical evidence 관련 metadata

한의학 논문 탐색에서는 가장 우선적인 source로 사용한다.

---

## 9.2 OpenAlex

주 역할:

- 폭넓은 scholarly coverage
- citation count
- FWCI
- topic
- source / venue metadata
- citation graph 확장

---

## 9.3 Semantic Scholar

주 역할:

- 보조 semantic search
- citation graph
- influential citation 관련 신호
- TLDR 등 보조 metadata

API rate limit을 고려하여 V1에서는 선택적으로 사용한다.

---

## 10. 내부 데이터 모델

```python
from pydantic import BaseModel


class Paper(BaseModel):
    uid: str

    doi: str | None = None
    pmid: str | None = None
    openalex_id: str | None = None
    s2_id: str | None = None

    title: str
    authors: list[str] = []
    venue: str | None = None
    year: int | None = None
    abstract: str | None = None

    cited_by_count: int | None = None
    publication_types: list[str] = []
    mesh_terms: list[str] = []

    is_oa: bool | None = None
    fulltext_url: str | None = None

    sources: list[str] = []
    source_ranks: dict[str, int] = {}


class PaperCard(BaseModel):
    uid: str

    title: str
    authors_short: str
    venue: str | None
    year: int | None

    doi: str | None
    pmid: str | None

    score: float

    citation_count: int | None
    publication_type: str | None

    matched_terms: list[str]
    sources: list[str]

    abstract: str | None = None
    is_open_access: bool | None = None
    fulltext_url: str | None = None
```

---

## 11. 소스 Adapter

```python
class SourceAdapter(Protocol):

    name: str

    async def search(
        self,
        query: str,
        limit: int = 50,
        **filters,
    ) -> list[Paper]:
        ...

    async def fetch(
        self,
        ids: list[str],
    ) -> list[Paper]:
        ...
```

구현:

```text
sources/
├─ base.py
├─ europepmc.py
├─ openalex.py
└─ semantic_scholar.py
```

모든 외부 API 응답은 `Paper` 모델로 변환한다.

검색 Core가 특정 API 응답 구조에 직접 의존하지 않도록 한다.

---

## 12. Deduplication

우선순위:

```text
DOI
 ↓
PMID
 ↓
정규화 제목 + 제1저자 + 연도
```

DOI 정규화:

- lowercase
- `https://doi.org/` 제거
- `doi:` 제거
- 공백 제거

여러 DB에서 동일 논문이 검색되면 하나의 `Paper`로 병합한다.

---

## 13. Metadata merge

예시 우선순위:

- biomedical metadata → Europe PMC
- citation signal → OpenAlex
- Semantic Scholar 전용 정보 → Semantic Scholar

소스 provenance는 항상 보존한다.

```json
{
  "sources": [
    "europepmc",
    "openalex"
  ],
  "source_ranks": {
    "europepmc": 2,
    "openalex": 8
  }
}
```

---

## 14. 검색 결과 융합

### Reciprocal Rank Fusion

```python
RRF_score(paper) =
    Σ source_weight / (k + source_rank)
```

기본값:

```text
k = 60
```

초기에는 source별 복잡한 가중치를 최소화한다.

예:

```yaml
europepmc: 1.0
openalex: 1.0
semantic_scholar: 0.8
```

---

## 15. 데모용 Reranking

기존 계획의 다수 신호 기반 복잡한 scoring은 후순위로 둔다.

V1에서는 다음 네 가지 정도만 활용한다.

```text
Final Score
= relevance
+ citation signal
+ evidence/publication type
+ recency
```

예시 가중치:

```yaml
relevance: 0.55
citation: 0.20
evidence: 0.15
recency: 0.10
```

후보군 내 percentile을 활용하여 citation long-tail 영향을 줄인다.

---

## 16. 선택적 LLM Reranking

정형 점수만으로 관련도 판별이 부족한 경우:

```text
RRF
 ↓
Top 30
 ↓
LLM Reranker
 ↓
Top 10
```

LLM 입력:

- 사용자 질의
- 논문 제목
- abstract
- publication type
- matched terms

LLM은 논문의 사실성을 판단하는 것이 아니라 **질의와의 직접적 관련도**를 재정렬하는 용도로 제한한다.

---

## 17. Agent용 인터페이스 — MCP

MCP는 검색 시스템 자체가 아니라 **Search Core를 상위 Agent에 노출하는 interface layer**이다.

### V1 Tool

```python
async def search_literature(
    query: str,
    intent: str = "auto",
    k: int = 10,
) -> list[PaperCard]:
    ...


async def get_paper(
    uid: str,
) -> Paper:
    ...


async def get_fulltext(
    uid: str,
) -> str | None:
    ...
```

### 호출 예시

```text
Drug Discovery Agent

"황금의 NF-kB 억제 근거를 찾아야 한다."

        ↓

search_literature(
    query="황금 NF-kB 억제",
    intent="mechanism",
    k=10
)

        ↓

PaperCard[]
```

MCP wrapper에서는 검색·랭킹 로직을 구현하지 않는다.

---

## 18. Human용 인터페이스 — Streamlit

UI의 주요 목적은 검색 결과뿐 아니라 **검색 과정의 추적 가능성**을 보여주는 것이다.

### 화면 요소

```text
┌─────────────────────────────────────────────┐
│ 한의학 문헌 탐색                            │
├─────────────────────────────────────────────┤
│ 검색어                                      │
│ [ 황금의 항염증 기전                     ] │
│                                             │
│ 검색 유형                                   │
│ [ mechanism ▼ ]                             │
│                                             │
│ [검색]                                      │
├─────────────────────────────────────────────┤
│ 검색어 확장                                 │
│ 황금                                        │
│ → Scutellaria baicalensis                   │
│ → Scutellariae Radix                        │
│ → baicalin / baicalein / wogonin            │
├─────────────────────────────────────────────┤
│ #1 논문                                     │
│ 제목                                        │
│ Journal · 2024 · cited 42                   │
│                                             │
│ Matched: baicalein, inflammation            │
│ Sources: Europe PMC, OpenAlex               │
│                                             │
│ [Abstract] [DOI] [Full text]                │
└─────────────────────────────────────────────┘
```

---

## 19. 검색 결과 Provenance

각 논문에 다음 정보를 가능한 범위에서 표시한다.

- 어떤 검색어에 매칭되었는가
- 어느 DB에서 검색되었는가
- 각 source의 원래 rank
- 최종 score
- publication type
- citation count
- OA 여부

예:

```json
{
  "matched_terms": [
    "Scutellaria baicalensis",
    "baicalein",
    "NF-kB"
  ],
  "sources": [
    "europepmc",
    "openalex"
  ],
  "source_ranks": {
    "europepmc": 2,
    "openalex": 5
  }
}
```

---

## 20. PaperQA2 연동 — V1.5

V1 검색 결과에서 선별한 논문을 PaperQA2에 전달한다.

```text
PaperCard[]
     │
     ▼
Top-K Paper
     │
     ▼
Full-text / Abstract
     │
     ▼
PaperQA2
     │
     ├─ evidence retrieval
     ├─ relevant passage selection
     ├─ contextual summary
     └─ citation-grounded synthesis
```

검색 source selection과 query expansion은 우리 시스템이 담당한다.

PaperQA2는 **선별된 문서 내부에서 근거를 찾고 종합하는 역할**에 집중시킨다.

---

## 21. 저장소 구조

```text
kmed-lit/
│
├─ src/
│  └─ kmed_lit/
│
│     ├─ models.py
│     ├─ search.py
│     ├─ normalize.py
│     ├─ query_builder.py
│     ├─ merge.py
│     ├─ ranking.py
│     ├─ cache.py
│     │
│     ├─ domain/
│     │  ├─ lexicon.py
│     │  └─ kmed_lexicon.yaml
│     │
│     ├─ sources/
│     │  ├─ base.py
│     │  ├─ europepmc.py
│     │  ├─ openalex.py
│     │  └─ semantic_scholar.py
│     │
│     └─ evidence/
│        └─ paperqa_adapter.py
│
├─ adapters/
│  ├─ mcp_server.py
│  └─ streamlit_app.py
│
├─ config/
│  ├─ ranking.yaml
│  └─ source.yaml
│
├─ eval/
│  ├─ demo_queries.yaml
│  └─ run_eval.py
│
└─ tests/
```

---

## 22. Core API

```python
async def normalize_query(
    query: str,
) -> QueryPlan:
    ...


async def search_literature(
    query: str,
    intent: str = "auto",
    k: int = 10,
    year_from: int | None = None,
) -> list[PaperCard]:
    ...


async def get_paper(
    uid: str,
) -> Paper:
    ...


async def get_fulltext(
    uid: str,
) -> str | None:
    ...
```

MCP와 Streamlit은 위 API를 그대로 사용한다.

---

## 23. Cache

초기에는 SQLite + 파일 캐시 정도로 구성한다.

| 대상 | TTL |
|---|---|
| 제목 / 저자 / DOI / abstract | 장기 |
| citation count | 7일 |
| 검색 결과 | 24시간 |
| full-text | 장기 |

API quota와 latency 감소가 목적이다.

---

## 24. Rate Limit / 오류 처리

소스별 독립적인 client를 사용한다.

기본 기능:

- timeout
- retry
- exponential backoff
- concurrency limit
- API 오류 격리

특정 source가 실패하더라도 전체 검색이 실패하지 않도록 한다.

예:

```text
Europe PMC  ─ success
OpenAlex    ─ success
S2          ─ rate limit

→ Europe PMC + OpenAlex 결과만으로 계속 진행
```

---

# 25. 구현 단계

## Phase 1 — 최소 검색 Core

- [ ] 프로젝트 구조 생성
- [ ] `Paper`, `PaperCard` 정의
- [ ] `SourceAdapter` 정의
- [ ] Europe PMC adapter
- [ ] OpenAlex adapter
- [ ] API response → `Paper`
- [ ] DOI / PMID deduplication
- [ ] metadata merge
- [ ] 기본 CLI 검색

### 완료 기준

```text
query
→ Europe PMC + OpenAlex
→ dedup
→ Top 10 Paper
```

가 정상 작동한다.

---

## Phase 2 — 한의학 특화

- [ ] `kmed_lexicon.yaml`
- [ ] 약재 20~30개
- [ ] 처방 10~20개
- [ ] 주요 성분 30~50개
- [ ] 최장일치 matcher
- [ ] Entity normalization
- [ ] Query expansion
- [ ] Source별 query builder
- [ ] `matched_terms` 기록
- [ ] `unmatched.log`

### 완료 기준

예:

```text
황금 항염증
```

입력 시 다음과 같은 학술 검색어가 실제 query에 포함된다.

```text
Scutellaria baicalensis
Scutellariae Radix
baicalin
baicalein
wogonin
```

---

## Phase 3 — 검색 품질

- [ ] RRF
- [ ] citation percentile
- [ ] recency score
- [ ] publication type score
- [ ] 간단한 final score
- [ ] 필요 시 LLM reranker
- [ ] Semantic Scholar adapter

### 완료 기준

대표 질의에서 관련 핵심 논문이 Top 10에 안정적으로 등장한다.

---

## Phase 4 — Agent / Human Interface

### MCP

- [ ] MCP server
- [ ] `search_literature`
- [ ] `get_paper`
- [ ] `get_fulltext`

### Streamlit

- [ ] query 입력
- [ ] intent 선택
- [ ] expanded terms 표시
- [ ] 검색 결과 card
- [ ] DOI / Full-text 링크
- [ ] matched terms
- [ ] sources 표시

### 완료 기준

동일한 검색 Core를:

```text
MCP Agent
```

와

```text
Web Browser
```

에서 각각 사용할 수 있다.

---

## Phase 5 — PaperQA2 연동

- [ ] PaperQA2 현재 API 확인
- [ ] `paperqa_adapter.py`
- [ ] Top-K 문서 전달
- [ ] abstract fallback
- [ ] full-text 추가
- [ ] evidence retrieval
- [ ] citation-grounded answer

### 완료 기준

사용자가:

```text
황금의 항염 작용 기전은 무엇인가?
```

를 질의했을 때:

1. 관련 논문 검색
2. Top-K 선별
3. 논문 내부 evidence retrieval
4. 근거 기반 답변
5. citation 출력

이 가능하다.

---

## 26. 데모 시나리오

### 시나리오 A — 사람이 직접 검색

```text
연구자
 ↓
"황금의 NF-kB 억제 효과"
 ↓
한의학 용어 expansion 확인
 ↓
논문 검색 결과 확인
 ↓
Top 논문 선택
 ↓
abstract / DOI / full-text 확인
```

### 시나리오 B — Agent가 검색 Tool 호출

```text
Drug Discovery Agent
 ↓
가설 검증에 문헌 근거 필요
 ↓
MCP search_literature 호출
 ↓
PaperCard[] 반환
 ↓
근거가 강한 논문 선택
 ↓
다음 reasoning 단계 수행
```

### 시나리오 C — 후속 PaperQA2

```text
질의
 ↓
문헌 검색
 ↓
Top-K
 ↓
PaperQA2
 ↓
핵심 근거 passage
 ↓
citation-grounded synthesis
```

---

## 27. 초기 평가

대규모 golden set 구축 전 데모에서는 소규모 평가를 진행한다.

### Demo Query Set

대표 질의 약 10개.

예:

- 황금의 항염 효과
- 황금 NF-kB
- 인삼의 면역 조절 기전
- 육미지황탕의 당뇨 관련 연구
- 황기의 염증성 질환 효과
- 감초의 간독성 또는 약물 상호작용
- 당귀의 혈관 관련 연구
- 마황의 안전성
- 청폐배독탕 임상 연구
- 한약 처방과 류마티스 관절염

### 평가 항목

- Top 10 관련 논문 비율
- 검색 누락 여부
- 한의학 명칭 expansion 정확성
- 중복 제거 정확성
- 검색 provenance 확인 가능 여부
- Agent MCP 호출 성공 여부
- Web UI 검색 성공 여부

정식 평가 단계에서:

- Recall@50
- Precision@10
- nDCG@10

등을 추가한다.

---

## 28. 데모에서 제외하는 항목

초기 버전에서는 다음 기능을 구현하지 않거나 최소화한다.

- 복잡한 citation graph traversal
- 대규모 knowledge graph
- 네트워크 약리학
- target prediction
- drug repurposing inference
- 복잡한 7~10개 signal ranking
- 자동 ontology 구축
- 대규모 PDF corpus ingestion
- 자체 vector database
- 자체 embedding pipeline
- 자체 PDF parser

필요 시 검증된 오픈소스를 재사용한다.

---

## 29. 기술 스택

```text
Language
- Python 3.11+

Academic APIs
- Europe PMC
- OpenAlex
- Semantic Scholar

Core
- Pydantic
- httpx
- asyncio
- PyYAML
- SQLite

Agent Interface
- Official MCP Python SDK

Human Interface
- Streamlit

LLM
- 기존 보유 LLM API

Evidence Engine
- PaperQA2 (V1.5 optional)

Reference Architecture
- TCM-Agent
```

---

## 30. 구현 우선순위

가장 먼저 완성해야 하는 것은 다음 경로이다.

```text
한의학 자연어 질의
        ↓
용어 정규화 / expansion
        ↓
Europe PMC + OpenAlex
        ↓
Paper 통합
        ↓
Dedup
        ↓
RRF / ranking
        ↓
PaperCard[]
```

이 경로가 안정화된 이후:

```text
PaperCard[]
   ├─ MCP
   ├─ Streamlit
   └─ PaperQA2
```

를 추가한다.

---

# 31. 최종 구현 전략

본 데모는 기존 논문 탐색 Agent 전체를 fork하여 개조하는 방식보다 **기존 공개 학술 API와 검증된 오픈소스 구성요소를 조합하고, 한의학 특화 retrieval layer만 자체 개발하는 구조**를 채택한다.

### 직접 개발의 핵심

- 한의학 용어 정규화
- Query expansion
- Source별 query 생성
- 다중 학술 DB orchestration
- 중복 제거 및 metadata merge
- 검색 결과 fusion / ranking
- provenance

### 재사용의 핵심

- 학술 데이터 → Europe PMC / OpenAlex / Semantic Scholar
- Agent protocol → MCP SDK
- Human UI → Streamlit
- evidence retrieval / synthesis → PaperQA2
- 상위 TCM multi-agent 구조 → TCM-Agent 참고

이를 통해 데모 구현 범위를 관리하면서도, 향후 신약개발 Agent의 Literature Retrieval Module로 그대로 확장 가능한 구조를 확보한다.
