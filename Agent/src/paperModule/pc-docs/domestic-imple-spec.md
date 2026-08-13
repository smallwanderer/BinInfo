# 국내 한의학 논문 탐색 에이전트 — Fast / Deep Search 구현 계획서

> **[Deprecated]** 국내 문헌 전용으로 범위를 제한하는 이 문서의 전제는 폐기되었습니다.
> 현재는 KCI(국내, `paperModule`을 MCP tool로 노출) + PubMed(해외, `Agent/src/agent/tools/pubmed.py`)를
> 상위 LangGraph 에이전트(`Agent/`)가 함께 tool-call하는 구조로 진행합니다. `paperModule`의 KCI
> 어댑터·Fast/Deep Search 구현 자체는 계속 유효하며, 이 문서는 "국내 전용" 설계 배경 참고용으로만 남깁니다.

## 1. 목표

국내 한의학·한약·처방·성분·임상 관련 질의를 대상으로 **국내 학술논문만 탐색하는 문헌 검색 에이전트**를 구현한다.

기존의 해외 문헌 검색 구조에서 필요했던 한글→영문 정규화, 다언어 한의학 용어 매핑, MeSH 기반 확장 등은 제거한다.  
사용자 질의는 기본적으로 **한국어 원문 그대로 국내 학술 DB에 검색**하며, 검색 결과 통합·랭킹·근거 분석에 집중한다.

시스템은 두 가지 탐색 경로를 제공한다.

- **Fast Search**
  - 관련 국내 논문 후보를 빠르게 탐색
  - KCI + ScienceON 중심
  - 결과를 중복 제거·통합·랭킹하여 `PaperCard[]` 반환
  - 상위 신약개발 Agent가 반복적으로 호출하기 적합

- **Deep Research**
  - 하나의 연구 질문을 국내 문헌을 기반으로 심층 조사
  - Fast Search 결과를 seed로 사용
  - 필요 시 추가 검색·질의 재작성·관련문헌 탐색
  - 논문 초록/원문에서 근거를 수집하고 citation-grounded synthesis 수행
  - 결과는 `ResearchReport` 형태로 반환

---

# 2. 설계 방향

## 2.1 유지하는 참고 아키텍처

### Fast Search — OriGene식 Tool Agent 관점

OriGene의 biomedical database Tool Agent 구조에서 다음 원칙을 참고한다.

- 학술 DB를 독립된 Tool/Adapter로 취급
- 검색 결과를 공통 내부 모델로 변환
- 검색 Tool이 상위 Agent에서 반복적으로 호출될 수 있도록 단순한 인터페이스 유지
- 특정 Agent framework에 검색 로직을 종속시키지 않음

본 시스템에서는 PubMed 등의 해외 DB 대신 **국내 학술 DB**를 연결한다.

---

### Deep Research — Robin / PaperQA2 관점

Robin의 Crow/Falcon 및 PaperQA2 계열의 문헌 조사 구조에서 다음 원칙을 참고한다.

- 한 번의 검색으로 종료하지 않음
- 초기 후보 문헌을 읽고 근거 부족 여부를 판단
- 필요하면 검색어를 재작성하여 추가 검색
- 관련문헌·참고문헌·인용문헌을 따라 추가 근거 확보
- 최종적으로 근거가 포함된 synthesis 생성

Deep Research는 자체 scientific RAG를 새로 만드는 대신 **PaperQA2를 evidence engine으로 재사용하는 방향**을 우선한다.

---

# 3. 전체 아키텍처

```text
                    User / Drug Discovery Agent
                               │
                               ▼
                        Korean Query
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
             FAST SEARCH                DEEP RESEARCH
                 │                           │
         ┌───────┴────────┐                  │
         ▼                ▼                  │
        KCI           ScienceON              │
         │                │                  │
         └───────┬────────┘                  │
                 ▼                           │
           Dedup / Merge                     │
                 │                           │
              RRF Fusion                     │
                 │                           │
         Lightweight Rerank                  │
                 │                           │
                 ▼                           │
            PaperCard[]                      │
                 │                           │
                 ├───────────────────────────┤
                 │                           ▼
                 │                   Evidence Planning
                 │                   Additional Search
                 │                   Related/Cited Works
                 │                   Abstract / Full-text
                 │                   PaperQA2
                 │                           │
                 │                           ▼
                 │                    ResearchReport
                 │
          ┌──────┴───────────────────────────┐
          ▼                                  ▼
       MCP Tools                         Human Web UI
```

---

# 5. 데이터 소스

## 5.1 KCI — V1 필수

**한국학술지인용색인(KCI)** 을 국내 학술논문의 기본 검색 source로 사용한다.

### 역할

- 국내 학술지 논문 검색
- 논문 기본정보
- 논문 상세정보
- 참고문헌 정보
- 인용정보
- DOI 및 KCI Control Number
- 제목 / 저자 / 학술지 / 키워드 / 초록 / 발행연도 기반 검색

### 구현 이유

KCI는 국내 학술지 중심의 검색·인용 메타데이터를 제공하므로 국내 문헌 탐색의 기본 source로 적합하다.

### 사용 API

- 논문 기본 정보 검색
- 논문 상세 정보
- 참고문헌 정보
- 인용정보

API 응답은 XML 기준으로 처리하며, 인증키는 configuration으로 관리한다.

---

# 5.2 ScienceON — V1 필수

**ScienceON 논문검색 API**를 KCI 보완 source로 사용한다.

### 역할

- 국내 과학기술·의학 관련 논문 coverage 보완
- 저널 및 프로시딩 논문 검색
- 논문 상세 서지정보
- 관련문헌
- 참고문헌
- 인용문헌

### 구현 이유

KCI와 수집 범위 및 검색 체계가 다르므로 동일 질의에서 후보 논문 recall을 보완할 수 있다.

ScienceON은 국내외 문헌을 모두 포함하므로 본 프로젝트에서는 **국내 문헌 조건을 적용할 수 있는 필드/분류를 API 신청 후 실제 스펙에서 확인하여 국내 논문만 반환하도록 제한**한다.

---

# 5.3 OASIS — 후속 한의학 특화 source

**OASIS 전통의학정보포털**은 국내 한의학 논문에 특화된 source이므로 도메인 관점에서는 중요하다.

OASIS는 한의학 학술지 논문, 참고문헌, 연구보고서 등을 별도로 구축하고 있으며 한의학 학술논문의 서지·초록 검색 및 원문 열람 기능을 제공한다.

다만 현재 계획 작성 시점에는 **공식 공개 Open API를 확인하지 못했으므로 V1 자동 검색 source로 포함하지 않는다.**

### 후속 조건

다음 중 하나가 확보되면 `OASISAdapter`를 추가한다.

- 공식 Open API
- 기관 간 데이터 연계 방식
- 허가된 데이터 export
- 이용약관상 허용된 기계적 접근 방식

비공식 웹 스크래핑을 기본 구현 방식으로 사용하지 않는다.

---

# 5.4 RISS — 선택적 확장

RISS는 국내 학술지 논문과 학위논문을 함께 탐색할 필요가 있을 때 후속 source로 고려한다.

### 사용 조건

- RISS Open API 사용 권한 확보
- 기관/대학도서관 기반 API 이용 조건 확인

### 추가 가치

- 학위논문
- KCI 외 국내 학술자료 보완

초기 데모에서는 KCI + ScienceON 두 source로 먼저 검색 품질을 검증한다.

---

# 6. 질의 처리

## 6.1 별도 자연어 질의 해석 모듈을 두지 않음

Fast Search에서는 사용자 질의를 의미적으로 재해석하지 않는다.

예:

```text
사용자 질의:
황금의 항염 효과
```

이를 다음처럼 바로 각 DB 검색에 전달한다.

```text
KCI:
title / keyword / abstract = "황금 항염"

ScienceON:
query = "황금 항염"
```

실제 source별 query parameter 형식은 adapter 내부에서 변환한다.

---

## 6.2 최소 전처리만 수행

검색 일관성을 위해 다음 정도만 처리한다.

- 앞뒤 공백 제거
- 중복 공백 정리
- Unicode 정규화
- 따옴표/괄호 등의 안전한 encoding
- 연도/저자/학술지 filter가 명시된 경우 별도 parameter로 분리

별도의 형태소 분석, Entity Linking, 사전 기반 확장은 V1에 포함하지 않는다.

---

# 7. Fast Search

## 7.1 목적

관련 국내 논문 후보를 짧은 시간 안에 확보한다.

Fast Search의 출력은 최종 답변이 아니라 **상위 Agent 또는 연구자가 후속 판단에 사용할 후보 문헌 목록**이다.

---

## 7.2 처리 흐름

```text
Korean Query
     │
     ▼
Source Query Mapping
     │
     ├───────────────┐
     ▼               ▼
    KCI          ScienceON
     │               │
     ▼               ▼
 Source Paper     Source Paper
     │               │
     └───────┬───────┘
             ▼
       Normalize Paper
             │
             ▼
       Deduplication
             │
             ▼
        Metadata Merge
             │
             ▼
           RRF
             │
             ▼
    Lightweight Rerank
             │
             ▼
        PaperCard[]
```

---

# 8. 공통 Paper 모델

```python
from pydantic import BaseModel


class Paper(BaseModel):
    uid: str

    doi: str | None = None
    kci_id: str | None = None
    scienceon_id: str | None = None
    riss_id: str | None = None

    title: str
    authors: list[str] = []
    journal: str | None = None
    publisher: str | None = None

    year: int | None = None
    volume: str | None = None
    issue: str | None = None
    pages: str | None = None

    abstract: str | None = None
    keywords: list[str] = []

    citation_count: int | None = None

    fulltext_url: str | None = None

    sources: list[str] = []
    source_ranks: dict[str, int] = {}


class PaperCard(BaseModel):
    uid: str

    title: str
    authors_short: str
    journal: str | None
    year: int | None

    doi: str | None
    kci_id: str | None

    score: float
    citation_count: int | None

    matched_query: str
    sources: list[str]
    source_ranks: dict[str, int]

    abstract: str | None = None
    fulltext_url: str | None = None
```

---

# 9. Source Adapter

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

    async def references(
        self,
        uid: str,
        limit: int = 50,
    ) -> list[Paper]:
        ...

    async def citations(
        self,
        uid: str,
        limit: int = 50,
    ) -> list[Paper]:
        ...
```

V1:

```text
sources/
├─ base.py
├─ kci.py
└─ scienceon.py
```

후속:

```text
sources/
├─ oasis.py
└─ riss.py
```

---

# 10. Deduplication

국내 논문은 DOI가 없는 경우도 고려하여 다음 순서로 식별한다.

```text
DOI
 ↓
KCI / ScienceON 등 source ID 교차 매핑
 ↓
정규화 제목 + 제1저자 + 발행연도
```

제목 정규화:

- 공백 정리
- 영문 대소문자 통일
- 특수문자 최소화
- 괄호 속 부제 처리

여러 source에서 동일 논문이 발견되면 하나의 `Paper`로 병합한다.

---

# 11. Metadata Merge

소스 provenance는 유지한다.

예:

```json
{
  "sources": [
    "kci",
    "scienceon"
  ],
  "source_ranks": {
    "kci": 2,
    "scienceon": 6
  }
}
```

필드 충돌 시 우선순위는 실제 API 품질 평가 후 정한다.

초기 원칙:

- KCI 고유 인용·등재 정보 → KCI
- ScienceON 관련/참고/인용문헌 정보 → ScienceON
- DOI → 값이 존재하는 source 우선
- 초록 → 더 완전한 값 우선
- 원문 URL → 접근 가능한 URL 우선

---

# 12. RRF

KCI와 ScienceON의 검색 점수는 직접 비교하지 않는다.

```text
KCI Rank ────────┐
                 ├─ RRF → 통합 후보
ScienceON Rank ──┘
```

```python
rrf_score(paper) =
    Σ source_weight / (k + source_rank)
```

초기값:

```yaml
k: 60

source_weight:
  kci: 1.0
  scienceon: 1.0
```

평가 결과에 따라 조정한다.

---

# 13. Fast Search Reranking

V1에서는 복잡한 novelty/actionability score를 넣지 않는다.

기본 신호:

```text
Final Score
├─ RRF relevance
├─ KCI citation signal
├─ recency
└─ metadata completeness
```

예시:

```yaml
relevance: 0.60
citation: 0.20
recency: 0.15
metadata_completeness: 0.05
```

정확한 가중치는 소규모 평가셋을 기준으로 조정한다.

---

# 14. 선택적 LLM Reranking

Fast Search에서 정형 랭킹만으로 결과 품질이 부족한 경우에만 사용한다.

```text
RRF / deterministic ranking
          ↓
        Top 30
          ↓
    LLM relevance rerank
          ↓
        Top 10
```

입력:

- 사용자 한국어 질의
- 논문 제목
- 국문/영문 초록
- 키워드
- 학술지
- 발행연도

LLM의 역할은 **질의와 논문의 직접 관련도 판단**으로 제한한다.

---

# 15. Deep Research

## 15.1 목적

Deep Research는 국내 논문 후보를 나열하는 것을 넘어, 하나의 연구 질문에 대한 **근거 수집과 종합**을 수행한다.

예:

```text
황금의 항염 효과에 대한 국내 연구 근거는 무엇인가?
```

출력에는 다음을 포함한다.

- 핵심 국내 논문
- 주요 연구 결과
- 연구 유형
- 서로 일치하는 결과
- 상충하는 결과
- 근거의 한계
- 인용 가능한 출처

---

# 15.2 Deep Research 흐름

```text
Research Question
       │
       ▼
Initial Fast Search
       │
       ▼
Seed Papers
       │
       ▼
Evidence Planning
       │
       ▼
Abstract / Full-text Retrieval
       │
       ▼
Evidence Sufficient?
       │
       ├─ No
       │    │
       │    ▼
       │  Korean Query Reformulation
       │    │
       │    ▼
       │  Fast Search 재호출
       │    │
       │    ├─ KCI
       │    └─ ScienceON
       │
       ▼
References / Citations / Related Papers
       │
       ▼
PaperQA2 Evidence Retrieval
       │
       ▼
Citation-grounded Synthesis
       │
       ▼
ResearchReport
```

---

# 16. Deep Research에서의 질의 재작성

Fast Search에서는 별도 자연어 해석 모듈을 사용하지 않는다.

그러나 Deep Research에서는 **근거 부족을 보완하기 위한 내부 검색어 재작성**을 허용한다.

예:

```text
초기:
황금 항염

추가 검색:
황금 염증 억제
황금 NF-kB
황금 대식세포 염증
황금 동물실험 항염
```

이는 독립적인 Query Interpretation Module이 아니라 **Deep Research의 iterative search behavior**로 취급한다.

---

# 17. PaperQA2의 위치

PaperQA2는 Deep Research의 evidence engine으로 사용한다.

## 위임

- document ingestion
- chunking
- evidence retrieval
- 관련 passage 선택
- contextual summarization
- citation-grounded synthesis

## 직접 유지

- KCI / ScienceON 검색
- 국내 논문 필터
- Fast Search
- seed-paper selection
- provenance
- 반복 검색 제어
- MCP / UI interface

```text
Domestic Search Core
       │
       ▼
Selected Korean Papers
       │
       ▼
PaperQA2 Adapter
       │
       ▼
Evidence / Synthesis
```

한국어 PDF/초록에 대한 PaperQA2 retrieval 품질은 실제 데모 데이터로 검증한다.

---

# 18. 원문 확보 전략

국내 논문은 source마다 원문 공개 조건이 다르므로 metadata search와 full-text retrieval을 분리한다.

우선순위:

```text
1. source가 제공하는 합법적 원문 URL
2. 공개 원문
3. 사용자가 업로드한 PDF
4. abstract fallback
```

유료 DB의 원문을 비공식 방식으로 우회하거나 자동 수집하지 않는다.

Deep Research는 원문을 확보하지 못한 논문에 대해 초록 기반 근거만 사용할 수 있도록 fallback을 둔다.

---

# 19. MCP 인터페이스

## Fast

```python
search_literature(
    query: str,
    k: int = 10,
    year_from: int | None = None,
    year_to: int | None = None,
    journal: str | None = None,
) -> list[PaperCard]
```

---

## Deep

```python
research_literature(
    question: str,
    seed_uids: list[str] | None = None,
) -> ResearchReport
```

---

## 상세 조회

```python
get_paper(uid: str) -> Paper

get_fulltext(uid: str) -> str | None
```

MCP Tool은 위 4개를 우선 제공한다.

---

# 20. Human Web UI

Streamlit UI는 Fast와 Deep을 분리한다.

```text
┌──────────────────────────────────────────┐
│ 국내 한의학 논문 탐색                    │
├──────────────────────────────────────────┤
│ [ Fast Search ] [ Deep Research ]        │
└──────────────────────────────────────────┘
```

## Fast 화면

- 한국어 검색어
- KCI / ScienceON source 선택
- 발행연도 filter
- 학술지 filter
- Top-K 결과
- source별 원래 rank
- 최종 score
- KCI 피인용 횟수
- 초록
- DOI / 원문 링크

## Deep 화면

- 연구 질문
- 초기 Fast Search 결과
- seed papers
- 추가 검색어
- 반복 횟수
- evidence papers
- 핵심 근거
- 상충 근거
- 한계
- citation-grounded report

---

# 21. Provenance

국내 문헌 검색에서도 검색 과정은 추적 가능해야 한다.

```json
{
  "query": "황금 항염",
  "sources": [
    "kci",
    "scienceon"
  ],
  "source_ranks": {
    "kci": 2,
    "scienceon": 6
  },
  "final_score": 0.84
}
```

Deep Research에서는 추가로:

```json
{
  "queries_used": [
    "황금 항염",
    "황금 염증 억제",
    "황금 NF-kB"
  ],
  "search_iterations": 2,
  "evidence_uids": [
    "..."
  ]
}
```

를 기록한다.

---

# 22. 저장소 구조

```text
kmed-domestic-lit/
│
├─ src/kmed_domestic_lit/
│  │
│  ├─ models.py
│  ├─ cache.py
│  │
│  ├─ sources/
│  │  ├─ base.py
│  │  ├─ kci.py
│  │  └─ scienceon.py
│  │
│  ├─ fast/
│  │  ├─ search.py
│  │  ├─ merge.py
│  │  ├─ dedup.py
│  │  ├─ fusion.py
│  │  └─ rerank.py
│  │
│  └─ deep/
│     ├─ research.py
│     ├─ planner.py
│     ├─ evidence.py
│     └─ paperqa_adapter.py
│
├─ adapters/
│  ├─ mcp_server.py
│  └─ streamlit_app.py
│
├─ config/
│  ├─ sources.yaml
│  ├─ fast_ranking.yaml
│  └─ deep_research.yaml
│
├─ eval/
│  ├─ fast_queries.yaml
│  ├─ deep_questions.yaml
│  └─ run_eval.py
│
└─ tests/
```

후속 source:

```text
sources/
├─ oasis.py
└─ riss.py
```

---

# 23. Cache / Rate Limit

초기에는 SQLite + 파일 캐시를 사용한다.

| 대상 | TTL |
|---|---:|
| 논문 기본 서지정보 | 장기 |
| 초록 | 장기 |
| 인용수 | 7일 |
| 검색 결과 | 24시간 |
| 원문 파일 | 허용 범위 내 장기 |

API key와 quota는 source별 configuration으로 관리한다.

```yaml
sources:
  kci:
    enabled: true
    api_key: ${KCI_API_KEY}

  scienceon:
    enabled: true
    api_key: ${SCIENCEON_API_KEY}
```

---

# 24. 구현 단계

## Phase 1 — Fast Search Core

- [ ] 프로젝트 구조
- [ ] `Paper`, `PaperCard`
- [ ] `SourceAdapter`
- [ ] KCI API 신청/연동
- [ ] ScienceON API 신청/연동
- [ ] 국내 논문 조건 확인
- [ ] XML parser
- [ ] API response → `Paper`
- [ ] deduplication
- [ ] metadata merge
- [ ] RRF
- [ ] CLI Fast Search

### 완료 기준

```text
"황금 항염"
→ KCI + ScienceON
→ 국내 논문 후보
→ dedup
→ Top 10 PaperCard
```

---

## Phase 2 — Fast Search 품질

- [ ] KCI citation signal
- [ ] recency score
- [ ] metadata completeness
- [ ] lightweight final score
- [ ] optional LLM reranker
- [ ] provenance
- [ ] Fast Search 평가셋

### 완료 기준

대표 국내 한의학 질의에서 핵심 논문이 Top-K에 안정적으로 포함된다.

---

## Phase 3 — Interface

### MCP

- [ ] `search_literature`
- [ ] `get_paper`
- [ ] `get_fulltext`

### Streamlit

- [ ] Fast Search
- [ ] source 필터
- [ ] 검색 결과
- [ ] score / source rank
- [ ] citation count
- [ ] abstract / DOI / 원문

### 완료 기준

동일한 Fast Search Core를 Agent와 연구자가 각각 사용한다.

---

## Phase 4 — Deep Research MVP

- [ ] `ResearchReport`
- [ ] Fast → seed papers
- [ ] abstract/full-text loader
- [ ] PaperQA2 adapter
- [ ] evidence retrieval
- [ ] citation-grounded synthesis
- [ ] MCP `research_literature`
- [ ] Streamlit Deep 화면

### 완료 기준

한 연구 질문에 대해 국내 논문 기반의 근거 보고서를 생성한다.

---

## Phase 5 — Agentic Deep Research

- [ ] evidence gap 판단
- [ ] 한국어 query reformulation
- [ ] 최대 반복 횟수 제한
- [ ] KCI 참고문헌 활용
- [ ] ScienceON 관련/참고/인용문헌 활용
- [ ] 추가 Fast Search
- [ ] conflicting evidence 식별
- [ ] search trace 저장

### 완료 기준

초기 검색으로 근거가 부족할 경우 추가 국내 문헌을 자동으로 탐색하여 보고서를 보완한다.

---

## Phase 6 — 국내 source 확장

우선순위:

1. **OASIS**
   - 공식 기계 접근 방식이 확보되면 가장 우선적으로 추가
   - 한의학 특화 recall 보완

2. **RISS**
   - 학위논문까지 포함해야 할 경우 추가

3. 기타 국내 DB
   - API 및 라이선스 조건을 확인한 뒤 필요 시 추가

---

# 25. 평가

## Fast Search

대표 국내 한의학 질의 10~20개를 구축한다.

예:

```text
황금 항염
육미지황탕 당뇨
감초 간독성
마황 안전성
한약 류마티스 관절염
침 치료 만성 요통
한약 약물상호작용
```

각 질의별 전문가가 핵심 논문을 지정한다.

### 지표

- Recall@50
- Recall@10
- Precision@10
- nDCG@10
- deduplication 정확도

---

## Deep Research

평가 항목:

- citation correctness
- evidence coverage
- answer groundedness
- 핵심 근거 누락 여부
- 상충 근거 탐지 여부
- 전문가 평가

---

# 26. V1에서 제외하는 기능

- 한글→영문 질의 변환
- 한의학 다국어 정규화
- 대규모 한의학 ontology
- MeSH mapping
- 약재→성분 자동 expansion
- 별도 자연어 Query Interpreter
- LangGraph 기반 multi-agent
- novelty / disruption index
- 자체 vector database
- 자체 PDF parser
- 자체 embedding model
- network pharmacology
- target prediction
- knowledge graph

---

# 27. 기술 스택

```text
Language
- Python 3.11+

Domestic Academic APIs
- KCI
- ScienceON

Optional Domestic Sources
- OASIS
- RISS

Core
- Pydantic
- httpx
- asyncio
- XML parser
- SQLite

Fast Search
- Deduplication
- Metadata Merge
- RRF
- Lightweight Reranking

Deep Research
- PaperQA2
- Existing LLM API

Agent Interface
- MCP Python SDK

Human Interface
- Streamlit

Reference Architecture
- OriGene: Fast / DB Tool Agent
- Robin / PaperQA2: Deep Literature Research
```

---

# 28. 최종 구현 전략

본 데모는 **국내 한의학 논문 탐색에 범위를 한정**한다.

따라서 해외 DB 검색을 위해 필요했던 별도의 한의학 언어 정규화 계층을 제거하고, 국내 학술 DB의 검색·통합·근거 분석 자체에 집중한다.

## Fast Search

```text
한국어 질의
   ↓
KCI + ScienceON
   ↓
Dedup / Merge
   ↓
RRF / Rerank
   ↓
PaperCard[]
```

목표:

> 빠르게 관련 국내 논문 후보를 확보한다.

---

## Deep Research

```text
연구 질문
   ↓
Fast Search
   ↓
Seed Papers
   ↓
Evidence Retrieval
   ↓
근거 부족 시 한국어 추가 검색
   ↓
References / Citations
   ↓
PaperQA2
   ↓
ResearchReport
```

목표:

> 국내 논문을 반복 탐색하고 읽어 근거 기반의 심층 조사 결과를 만든다.

---

# 29. 한 문장 정의

> **본 시스템은 OriGene식 국내 학술 DB Tool 구조를 참고한 Fast Search와 Robin/PaperQA2식 agentic literature research를 참고한 Deep Research를 분리하여, KCI와 ScienceON을 중심으로 국내 한의학 논문 후보 검색부터 근거 기반 심층 조사까지 제공하는 문헌 탐색 모듈이다.**

---

# 30. 데이터 소스 확인 메모

- **KCI**
  - 한국연구재단 KCI Open API에서 논문 기본정보, 상세정보, 참고문헌, 인용정보 제공
  - API key 필요
  - XML 응답
  - 검색 필드에 제목, 저자, 학술지, 기관, 키워드, 초록, 발행기간, DOI 등 제공

- **ScienceON**
  - 논문 검색 API 및 논문 상세검색 API 제공
  - 상세검색에서 관련문헌, 참고문헌, 인용문헌 정보 제공
  - 회원가입 후 API 사용 신청
  - 무료
  - XML 응답
  - 국내외 논문을 함께 수집하므로 국내 논문 범위 필터를 실제 API 스펙에서 검증 후 적용

- **OASIS**
  - 한국한의학연구원의 전통의학정보포털
  - 한의학술논문 55종 및 한의학 연구정보 제공
  - 논문 서지/초록 검색과 원문 열람 기능 제공
  - 공개 Open API는 본 계획 작성 시 확인되지 않아 자동 연동은 후속 검토

- **RISS**
  - 국내 학술지 및 학위논문 검색 source
  - Open API 이용 조건 및 기관 권한 확인 후 후속 연동
