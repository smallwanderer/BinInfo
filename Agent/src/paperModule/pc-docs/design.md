# 한의학 문헌 탐색 에이전트 — 디자인 목적 및 구현 근거

## 1. 문서 목적

본 문서는 한의학 문헌 탐색 에이전트 데모의 **설계 목적, 주요 기술 선택의 이유, 직접 구현 범위와 오픈소스 재사용 범위**를 정리한다.

세부 API 스키마나 단계별 구현 체크리스트보다 다음 질문에 답하는 것을 목적으로 한다.

- 왜 별도의 한의학 문헌 탐색 모듈이 필요한가?
- 왜 여러 학술 데이터 소스를 함께 사용하는가?
- 왜 검색 Core와 MCP/Web UI를 분리하는가?
- 어떤 기능은 직접 구현하고 어떤 기능은 기존 오픈소스를 재사용하는가?
- PaperQA2와 TCM-Agent는 어떤 위치에서 활용하는가?
- 데모 단계에서 무엇을 구현하고 무엇을 후속으로 미루는가?

---

# 2. 문제 정의

일반적인 논문 검색 시스템만으로는 한의학 문헌 탐색에 필요한 recall과 추적 가능성을 확보하기 어렵다.

한의학의 동일한 약재·처방·성분이 여러 언어와 표기로 분산되어 있기 때문이다.

예:

```text
황금
├─ 黃芩
├─ Scutellaria baicalensis
├─ Scutellariae Radix
├─ Chinese skullcap
├─ baicalin
├─ baicalein
└─ wogonin
```

또한 상위 신약개발 Agent가 문헌을 사용할 경우 단순한 검색 결과보다 다음 정보가 필요하다.

- 어떤 용어 확장을 통해 논문이 검색되었는가
- 어느 데이터베이스에서 검색되었는가
- 왜 상위 결과로 선정되었는가
- DOI/PMID 등 동일 논문 식별자가 무엇인가
- 후속 근거 분석에 사용할 수 있는 초록 또는 원문이 있는가

따라서 본 시스템의 핵심 목적은 **한의학 자연어 질의를 학술 검색에 적합한 형태로 변환하고, 복수의 학술 데이터베이스에서 근거 문헌을 회수하여 구조화된 결과로 제공하는 것**이다.

---

# 3. 핵심 디자인 목표

## 3.1 한의학 특화 검색

일반 검색엔진을 다시 만드는 것이 아니라, 기존 학술 검색 API 위에 **한의학 Domain Retrieval Layer**를 추가한다.

핵심 기능:

- 한글·한자·영문·라틴명 정규화
- 약재·처방·활성 성분 간 연결
- 소스별 query expansion
- 검색 결과의 matched term 기록

차별화 영역은 검색 인프라 자체가 아니라 **한의학 용어를 실제 학술 문헌과 연결하는 계층**이다.

---

## 3.2 검색 Core와 사용 인터페이스 분리

검색 로직은 하나의 Python Core에 구현하고, 이를 서로 다른 방식으로 사용한다.

```text
                    Literature Search Core
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
              MCP Tool                  Web UI
                 │                         │
                 ▼                         ▼
        Drug Discovery Agent           Researcher
```

### 이유

- Agent용 검색과 사람용 검색을 각각 구현하지 않는다.
- 동일 검색 결과를 Agent와 연구자가 비교할 수 있다.
- MCP, Web UI 또는 상위 Agent 프레임워크가 변경되어도 검색 로직은 유지된다.
- 검색 품질 평가를 interface와 독립적으로 수행할 수 있다.

따라서 MCP는 검색 시스템 자체가 아니라 **Search Core를 외부 Agent에 노출하는 adapter**로 취급한다.

---

## 3.3 검색과 근거 분석의 책임 분리

본 시스템은 다음 두 계층을 구분한다.

```text
[Retrieval Layer]
관련 논문을 찾고 선별
        │
        ▼
[Evidence Layer]
선별된 논문 내부의 근거를 읽고 종합
```

### Retrieval Layer

직접 구현 중심:

- terminology normalization
- query expansion
- academic API orchestration
- deduplication
- metadata merge
- rank fusion
- lightweight reranking

### Evidence Layer

기존 오픈소스 재사용 중심:

- full-text parsing
- chunk retrieval
- evidence selection
- citation-grounded synthesis

이 분리를 통해 논문 검색 품질 문제와 RAG/요약 품질 문제를 독립적으로 검증할 수 있다.

---

# 4. 전체 아키텍처

```text
                  User / Drug Discovery Agent
                              │
                              ▼
                  K-Medicine Query Layer
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          Domain Normalizer          Query Builder
                 │                         │
                 └────────────┬────────────┘
                              ▼
                  Literature Search Core
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
        Europe PMC         OpenAlex      Semantic Scholar
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    Deduplication / Merge
                              │
                              ▼
                          RRF Fusion
                              │
                              ▼
                     Lightweight Rerank
                              │
                              ▼
                         PaperCard[]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
           MCP / UI                    PaperQA2 (후속)
                                              │
                                      Evidence Retrieval
                                      Synthesis / Citation
```

---

# 5. 학술 데이터 소스 선택 이유

## 5.1 Europe PMC

### 역할

- 생의학 중심 문헌 검색
- PMID
- abstract
- MeSH
- publication type
- OA/full-text 접근 정보

### 선택 이유

한의학 연구를 신약개발 관점에서 탐색할 경우 생의학적 기전, 전임상, 임상 연구를 다뤄야 하므로 biomedical indexing이 중요하다.

특히 MeSH와 publication type은 임상근거와 기전 연구를 구분하는 데 유용하다.

따라서 **한의학-생의학 연결을 담당하는 핵심 소스**로 사용한다.

---

## 5.2 OpenAlex

### 역할

- 폭넓은 학술 문헌 coverage
- citation metadata
- topic / source 정보
- 관련 문헌 및 인용 관계 확장

### 선택 이유

Europe PMC만으로는 생의학 색인 밖의 관련 연구나 학술 영향력 신호를 충분히 확보하기 어렵다.

OpenAlex는 검색 결과 보강과 citation 기반 메타데이터 제공 역할을 담당한다.

현재 OpenAlex API 정책은 변경 가능성이 있으므로 quota나 비용 수치를 코드에 고정하지 않고 configuration으로 관리한다.

---

## 5.3 Semantic Scholar

### 역할

- 보조 검색
- citation 관련 metadata
- 유사 논문 탐색
- semantic retrieval 보완

### 선택 이유

Europe PMC와 OpenAlex에서 회수되지 않거나 lexical query만으로 놓칠 수 있는 논문을 보완할 수 있다.

다만 데모 V1에서는 필수 source로 두지 않고, **검색 품질 개선 효과가 확인된 경우 추가하는 보조 source**로 취급한다.

---

## 5.4 국내 및 중의학 데이터베이스

KCI, CNKI 등의 데이터 소스는 V1의 필수 범위에서 제외한다.

### 이유

- 초기 소스 수가 많아질수록 검색 실패 원인을 분리하기 어렵다.
- 국내/중문 DB는 별도의 메타데이터 및 인증 정책을 고려해야 한다.
- 먼저 국제 학술 DB 기반 검색 Core의 품질을 검증하는 것이 우선이다.

국내 한의학 문헌의 중요성이 실제 데모에서 확인되면 후속 source adapter로 추가한다.

---

# 6. 한의학 Domain Layer를 직접 구현하는 이유

본 프로젝트에서 가장 직접적인 차별화가 필요한 부분이다.

기존 PaperQA2, OpenAlex, Europe PMC 등은 일반적인 scientific literature를 대상으로 하며 다음 관계를 자동으로 충분히 해석하지 않는다.

```text
한글 약재명
  ↕
한자명
  ↕
식물 학명
  ↕
생약명
  ↕
활성 성분
```

따라서 별도의 `kmed_lexicon`과 normalization layer를 둔다.

예:

```yaml
- id: HERB:SCUTELLARIA_BAICALENSIS
  type: herb
  ko: [황금, 속썩은풀]
  hanja: [黃芩]
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
```

### 설계 원칙

- 사전 기반 deterministic matching을 우선한다.
- LLM은 미등록 표현 분석과 검색어 후보 생성에 보조적으로 사용한다.
- LLM이 생성한 synonym을 자동으로 영구 사전에 추가하지 않는다.
- 검색 중 매칭되지 않은 표현은 로그로 남겨 사전 확장 후보로 사용한다.

---

# 7. 다중 검색 결과를 하나로 통합하는 이유

각 학술 DB의 검색 점수는 의미와 스케일이 다르다.

따라서 raw score를 직접 합산하지 않는다.

```text
Europe PMC ranking
OpenAlex ranking
Semantic Scholar ranking
          │
          ▼
 Reciprocal Rank Fusion
```

### RRF 사용 이유

- 소스별 검색 점수 스케일을 맞출 필요가 없다.
- 각 소스에서 높은 순위를 받은 논문을 안정적으로 융합할 수 있다.
- 구현이 단순하고 explainability가 높다.
- 데모 단계에서 복잡한 학습 기반 rank fusion이 필요하지 않다.

초기에는 RRF를 기본 fusion 방식으로 사용하고, 이후 평가셋이 확보되면 가중치를 조정한다.

---

# 8. 복잡한 랭킹을 V1에서 제외하는 이유

초기 설계에는 다음과 같은 다수의 신호가 포함되어 있었다.

- relevance
- impact
- influence
- velocity
- venue
- evidence
- recency
- novelty
- LLM judge
- actionability

이 구조는 최종 시스템에서는 검토할 수 있으나 데모에서는 과도하다.

### V1 원칙

우선 다음 정도만 사용한다.

```text
Final Score
├─ 검색 관련도
├─ citation signal
├─ publication/evidence type
└─ recency
```

### 이유

- 랭킹 신호가 많을수록 가중치 튜닝을 위한 라벨 데이터가 필요하다.
- 평가셋 없이 복잡한 score를 도입하면 설계자의 직관이 그대로 bias가 된다.
- novelty, actionability 같은 개념은 별도 검증이 필요한 연구 문제다.

따라서 V1의 목적은 **검색 후보를 잘 회수하고 납득 가능한 순서로 보여주는 것**에 둔다.

---

# 9. LLM 사용 위치

LLM API는 이미 확보되어 있으므로 필요한 위치에 제한적으로 사용한다.

## 9.1 Query interpretation

사용 예:

```text
"황금이 류마티스 관절염에서 염증을 낮추는 기전"
```

를 다음과 같이 구조화한다.

```text
Herb     → Scutellaria baicalensis
Disease  → rheumatoid arthritis
Intent   → mechanism
Concept  → inflammation
```

다만 entity canonicalization은 가능한 경우 사전 기반 결과를 우선한다.

---

## 9.2 선택적 reranking

RRF 결과 중 Top-N의 제목과 초록을 LLM에 전달하여 질의 직접 관련도를 재평가할 수 있다.

```text
Search
 ↓
RRF Top 30
 ↓
LLM relevance rerank
 ↓
Top 10
```

V1에서는 필수가 아니며 deterministic ranking으로 충분하지 않은 경우에만 사용한다.

---

# 10. PaperQA2 활용 이유와 범위

## 10.1 전체 fork를 기본 전략으로 사용하지 않는 이유

PaperQA2의 강점은 scientific document RAG와 evidence synthesis이다.

반면 본 시스템에서 직접 통제해야 하는 핵심은:

- 한의학 terminology normalization
- source별 query 생성
- 복수 DB 검색
- retrieval provenance
- 문헌 통합 및 선별

이다.

PaperQA2 전체를 fork해서 이 검색 계층까지 변경하면 upstream 변화와 커스텀 검색 로직이 강하게 결합된다.

---

## 10.2 권장 활용 방식

PaperQA2를 **Evidence Engine dependency**로 사용한다.

```text
우리 Retrieval Core
       │
       ▼
    Top-K Papers
       │
       ▼
     PaperQA2
       │
       ├─ 문서 parsing
       ├─ evidence retrieval
       ├─ contextual summarization
       └─ citation-grounded synthesis
```

즉:

- **논문을 어떤 기준으로 찾을지는 우리 시스템**
- **찾은 논문에서 어떤 근거를 읽어낼지는 PaperQA2**

로 역할을 분리한다.

PaperQA2는 release 간 API 변경 가능성이 있으므로 연동 시 버전을 명시적으로 pin하고 adapter 계층을 둔다.

---

# 11. TCM-Agent 활용 이유와 범위

TCM-Agent는 현재 데모 검색 Core를 직접 구현하기 위한 기반 코드라기보다 **향후 상위 한의학 신약개발 Agent 아키텍처를 설계하기 위한 참고 사례**로 본다.

참고 영역:

- 약재/성분/타깃을 연결하는 workflow
- network pharmacology Agent
- knowledge graph 연동
- multi-agent orchestration

현재 데모는 Literature Retrieval Module이므로 TCM-Agent의 전체 구조를 그대로 가져오지 않는다.

따라서:

```text
TCM-Agent
→ Reference Architecture

PaperQA2
→ Reusable Evidence Component

kmed-lit
→ 직접 개발하는 Domain Retrieval Core
```

로 역할을 구분한다.

---

# 12. MCP 설계 이유

상위 Agent가 검색 기능을 사용할 수 있도록 MCP Tool interface를 제공한다.

다만 MCP 코드는 가능한 한 얇게 유지한다.

```text
MCP Tool
   │
   ▼
search_literature()
   │
   ▼
Search Core
```

### 이유

- Tool protocol과 business logic을 분리한다.
- MCP 버전 변화가 검색 Core에 영향을 주지 않는다.
- 같은 함수를 Python에서 직접 import할 수도 있다.
- 향후 다른 agent framework에서도 재사용 가능하다.

현재 MCP Python SDK v2 기준으로 high-level server는 `MCPServer`를 사용한다.

예:

```python
from mcp.server import MCPServer

mcp = MCPServer("kmed-lit")
```

기존 `FastMCP` v1 import를 기준으로 새 코드를 작성하지 않는다.

---

# 13. Human UI를 별도로 제공하는 이유

Agent용 API만 만들 경우 검색 품질을 사람이 직접 검토하기 어렵다.

따라서 Streamlit 기반의 간단한 UI를 제공한다.

UI에서 보여줄 핵심 정보:

- 사용자 원문 query
- 정규화된 entity
- 확장된 검색어
- 검색 source
- source별 rank
- 최종 score
- matched terms
- title / year / journal
- DOI / PMID / full-text 링크

### 목적

단순 편의 기능이 아니라 **검색 시스템의 디버깅·검증 인터페이스**이다.

특히 한의학 용어 expansion이 올바르게 수행되었는지 사람이 즉시 확인할 수 있어야 한다.

---

# 14. Provenance를 유지하는 이유

최종 점수만 반환하면 검색 결과가 왜 선택되었는지 알 수 없다.

따라서 다음 정보를 보존한다.

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

### 효과

- 잘못된 query expansion 탐지
- 특정 source 편향 확인
- 랭킹 문제 디버깅
- 상위 Agent의 추가 판단
- 연구자의 수동 검증

이 때문에 explainability를 단순 LLM explanation이 아니라 **검색 과정에서 생성된 실제 metadata**로 확보한다.

---

# 15. V1 구현 범위

## 필수

- `Paper`, `PaperCard` 공통 데이터 모델
- Europe PMC adapter
- OpenAlex adapter
- 한의학 lexicon
- entity normalization
- source별 query builder
- DOI/PMID 중심 deduplication
- metadata merge
- RRF
- lightweight reranking
- provenance
- MCP interface
- Streamlit interface
- cache / retry / rate-limit 대응

## 선택

- Semantic Scholar
- LLM relevance reranking

---

# 16. V1에서 제외할 기능

다음 기능은 초기 데모 목표를 달성하는 데 필수가 아니므로 후속으로 이동한다.

- LangGraph 기반 별도 multi-agent graph
- REFLECT 자동 재검색 loop
- 복잡한 intent별 가중치 프로파일
- novelty score
- Uzzi / disruption index
- LLM judge의 다차원 채점
- actionability score
- citation graph traversal
- network pharmacology
- target prediction
- knowledge graph
- 대규모 vector DB
- 자체 PDF parser
- 자체 embedding pipeline
- 대규모 golden set

이 기능들은 검색 Core의 기본 유용성이 확인된 후 필요성에 따라 추가한다.

---

# 17. V1.5 이후 확장

## Evidence Analysis

- PaperQA2 adapter
- full-text 확보
- evidence passage 검색
- 논문별 구조화 요약
- 다중 논문 synthesis
- citation-grounded answer

## Retrieval Expansion

- Semantic Scholar 유사논문
- citation graph traversal
- KCI
- CNKI
- 관련 논문 자동 탐색

## Agentic Workflow

검색 품질과 use case가 충분히 검증된 이후 필요하면 다음을 추가한다.

```text
PLAN
 ↓
SEARCH
 ↓
EVALUATE
 ↓
근거 부족?
 ├─ Yes → query reformulation → SEARCH
 └─ No  → synthesis
```

Agent loop를 먼저 구현하지 않는 이유는 **단일 검색 호출의 품질이 확보되지 않으면 반복 실행해도 낮은 품질의 검색을 반복할 뿐이기 때문**이다.

---

# 18. 평가 전략

## V1

소규모 대표 query를 이용한 검색 품질 확인을 우선한다.

평가 항목:

- 한의학 entity normalization 정확성
- query expansion 적절성
- 관련 논문의 Top-K 포함 여부
- 중복 제거 정확성
- source merge 정확성
- provenance 확인 가능 여부
- MCP와 UI 결과 일관성

## 이후

도메인 전문가가 라벨링한 평가셋이 확보되면 다음 지표를 적용한다.

- Precision@10
- Recall@50
- nDCG@10
- MRR

가중치가 많은 복잡한 랭킹은 이 단계 이후에 도입한다.

---

# 19. 기술 스택

```text
Language
- Python 3.11+

Academic Sources
- Europe PMC
- OpenAlex
- Semantic Scholar (optional)

Core
- Pydantic
- httpx
- asyncio
- PyYAML
- SQLite

Agent Interface
- MCP Python SDK v2 / MCPServer

Human Interface
- Streamlit

LLM
- 기존 보유 API

Evidence Engine
- PaperQA2 (V1.5+)

Reference
- TCM-Agent
```

---

# 20. 최종 설계 결정 요약

| 결정 | 선택 | 이유 |
|---|---|---|
| 검색 구조 | Federated Search | 기존 학술 DB를 재사용하면서 coverage 확대 |
| 한의학 특화 | 자체 Domain Layer | 일반 검색기로 해결하기 어려운 명칭·성분 관계 처리 |
| 결과 융합 | RRF | 소스별 score scale 차이를 안전하게 통합 |
| 검색 Core | 프레임워크 독립 Python | MCP/UI/상위 Agent와 결합도 최소화 |
| Agent 연결 | MCP adapter | 상위 Agent에서 표준 Tool로 사용 |
| Human 확인 | Streamlit | 검색 과정과 용어 확장을 직접 검증 |
| PaperQA2 | 후속 Evidence Engine | 이미 구현된 document RAG를 재사용 |
| TCM-Agent | Reference Architecture | 향후 network pharmacology / multi-agent 설계 참고 |
| LangGraph | V1 제외 | 데모 검색 Core 구현에는 불필요 |
| 복잡한 novelty/judge | V1 제외 | 평가셋 없는 조기 최적화 방지 |
| 직접 개발 중심 | normalization + retrieval orchestration | 프로젝트의 실제 차별화 영역에 집중 |

---

# 21. 한 문장 정의

> **본 시스템은 Europe PMC·OpenAlex 등 기존 학술 인프라 위에 한의학 특화 용어 정규화와 검색 통합 계층을 구축하고, 동일한 Search Core를 MCP와 Web UI로 제공하며, 논문 내부 근거 분석은 PaperQA2와 같은 검증된 오픈소스에 위임하는 경량 문헌 탐색 모듈이다.**
