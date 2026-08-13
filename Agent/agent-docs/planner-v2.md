이 문서는 `planner.md`의 수정안이다. 목표는 동일하다 — 사람이 문헌을 찾을 때의 순서를 그대로 옮긴다.

1. 질의를 빠르고 넓게 탐색해서 후보를 추리고 (Fast)
2. 추려진 근거로 원 질의가 실제로 충분히 해결됐는지 판단하고, 부족하면 그 부족한 부분만 다시 찾는다 (Deep)

첫 초안에서 "합칠 수 있는 건 다 합친다"는 방향으로 갔더니 정확도를 깎는 병합과 그냥 낭비만 없애는 병합이 섞여 있었다. 이 버전은 그 둘을 구분한다 — **판단의 세분성(granularity)은 유지하고, 중복 작업만 제거한다.**

---

# 1. 계층 병합과 분할 사유

| planner.md | planner-v2.md | 병합 근거 / 리스크 |
|---|---|---|
| Entry Agent (목표·제약조건 추출) | **그대로 별도 1 call 유지** | 다른 작업과 섞이면 제약조건이 누락되기 쉽기에 별도로 분리 |
| Fast Planner + Query Generation | **Query Builder 1 call로 병합** | 이 둘은 사실상 하나의 연산이다 — "하위주제 → source별 검색어 문자열"을 중간 표현 없이 바로 만들면 된다. 분해와 변환을 별개 능력으로 볼 이유가 약하다. |
| Deep Planner (사전 분해) + Critic (사후 판단) — 별개 계층 | **Depth Judge 하나로 통합, 반복 호출** | 둘 다 "지금까지 근거로 목표가 해결됐는가, 안 됐으면 뭐가 빠졌는가"를 묻는 동일 질문이다. 최초 호출(근거 없음)이 초기 분해, 이후 호출이 Critic. |
| Relevance Selection — Need마다 별도 호출(N개) | **1 call, 단 후보마다 Q1~Q4 각각 태깅** | 판단을 뭉뚱그리면("전체적으로 관련 있나") 안전성만 다루는 논문처럼 한 측면에만 강하게 관련된 후보가 걸러질 수 있다. call 수는 줄이되(N번 → 1번), 판단 기준은 Need별로 유지한다 — 프롬프트가 후보마다 "Q1 관련: Y/N, Q2 관련: Y/N, ..."을 각각 출력하게 한다. |
| PaperQA2 — Need마다 독립 Docs 생성 (문서 중복 ingest) | **Docs 인스턴스는 세션 전체에서 공유, `.aquery()`는 aspect별로 따로** | 문서 중복 ingest(embedding/chunking)는 순수 낭비라 제거한다. 반면 PaperQA2에게 "효과·부작용·적용범위 다 조사해줘"처럼 뭉친 질문을 한 번에 던지면 검색 임베딩이 흐려져 얕은 답이 나온다 — 이건 정확도 문제라 유지한다. 즉 **ingest는 공유, query는 aspect별 분리**. |
| Synthesis (최종 종합 LLM 호출) | **제거, 결정론적 조립으로 대체** | PaperQA2가 aspect별로 이미 근거 인용된 답을 내놓는다. 이걸 다시 LLM이 종합하면 그 과정에서 근거 없는 문장이 새로 끼어들 위험이 생긴다. 여러 개의 근거-보장 답변을 그대로 구조에 얹는 게, 한 번 더 LLM을 거쳐 합치는 것보다 안전하다. |

---

# 2. 아키텍처

[시스템 아키텍처](./images/planner2_system_architecture.png)

---

# 3. 단계별 설명

## Entry Agent (LLM #1, 1회)

목표/명시적 제약조건만 뽑는 전용 호출. 다른 작업과 안 섞는 이유는 §1 표에 적은 대로 — 크라우드된 프롬프트에서 조건이 누락된 전례가 있다. 출력에 IF처럼 시스템이 채울 수 없는 제약이 있으면 `unfillable_constraints`로 표시해서 마지막 조립 단계가 결정론적으로 처리하게 한다 (`Agent/src/agent/graph.py`의 `ask()`에 있는 `_IF_MENTION` 가드와 같은 방식).

## Query Builder (LLM #2, 1회)

Fast Planner + Query Generation을 합친 것. sub-topic을 만드는 동시에 source별 문자열까지 바로 낸다.

```json
{
  "sub_queries": [
    {"topic": "효과", "kci": "뇌혈관질환후유증 침치료 효과", "pubmed": "post-stroke sequelae acupuncture efficacy"},
    {"topic": "부작용", "kci": "뇌혈관질환후유증 침치료 부작용", "pubmed": "acupuncture stroke adverse events"},
    {"topic": "적용범위", "kci": "뇌혈관질환후유증 침치료 적용범위", "pubmed": "acupuncture stroke indication scope"}
  ]
}
```

## Fast Search (LLM 없음)

기존 `search_literature`(MCP) / `search_pubmed` 툴 그대로 재사용, sub_query별 병렬 호출.

## Relevance Screen (LLM #3, 1회)

후보 전체를 한 번에 넣되, **후보마다 Q1~Q4 각각에 대해 관련 여부를 개별 태깅**하도록 요청한다.

```json
{"uid": "kci:123", "relevant_to": ["효과", "적용범위"]},
{"uid": "pmid:456", "relevant_to": ["부작용"]}
```

이러면 "부작용만 다루는 논문"이 뭉뚱그린 판단 때문에 탈락하는 일이 없다 — 호출은 1번이지만 판단 단위는 Need만큼 세분화되어 있다.

## PaperQA2 — 공유 ingest + aspect별 query

세션 시작 시 `Docs()` 하나를 만들고 Screened Pool 전체를 ingest(1회, 중복 없음). 이후 Depth Judge 루프에서 aspect마다 **같은 Docs 인스턴스에** `docs.aquery(aspect_question)`을 개별 호출한다. 이미 검증된 aspect는 재조회하지 않고 캐시된 답을 그대로 쓴다.

`paperModule/src/kmed_domestic_lit/deep/paperqa_adapter.py`는 지금 호출마다 `Docs()`를 새로 만드는데, 여기서는 이 인스턴스를 Deep Research 세션 동안 재사용하도록 바꿔야 한다.

## Depth Judge Loop (LLM #4 × aspect 수 + LLM #5, 라운드당, 최대 `max_iterations`회)

Deep Planner + Critic 통합. 최초 라운드는 아직 읽은 게 없으니 missing_aspects가 자연히 Query Builder의 sub_queries 전체가 되고, 이후 라운드부터는 실제로 읽은 aspect별 답을 보고 진짜 부족한 것만 남긴다. `missing_aspects`는 라운드당 최대 2~3개로 제한한다.

## 최종 조립 (LLM 없음)

aspect별 `docs.aquery()` 결과(각각 citation-grounded)를 `ResearchReport.key_findings`에 aspect 단위로 그대로 배치한다. 추가 종합 LLM 호출을 넣지 않는 이유는 §1 표 마지막 줄 — 이미 근거가 보장된 답변 여러 개를 다시 LLM이 재종합하면 그 과정에서 근거 없는 문장이 새로 생길 위험이 있기 때문이다.

---

# 4. LLM call 수 비교

가정: sub-query/aspect 3개, Depth Judge 루프 2라운드, 2라운드째는 missing_aspects 1개만 재조회.

| | planner.md | planner-v2.md |
|---|---:|---:|
| 질의 이해/분해 | 3 (Entry+Planner+QueryGen, 순차) | 2 (Entry 1 + Query Builder 1) |
| 관련도 판단 | Need마다 별도(4) | 1 (단, 후보별 Q-tag 유지) |
| Coordinator/Critic | Deep Planner(1) + Critic(라운드당 1×2) = 3 | Depth Judge(라운드당 1×2) = 2 |
| PaperQA2 ingest | Need마다 독립 생성·ingest(4회, 중복 포함) | 1회 (세션 공유) |
| PaperQA2 query | Need마다(4, ingest에 포함) | aspect별(1라운드 3 + 2라운드 1) = 4 |
| Synthesis | 1 | 0 (결정론적 조립) |
| **LLM call 합** | **약 11+ (Need 수·라운드 수에 비례해 더 커짐)** | **약 9, 단 ingest 중복은 완전히 제거** |

호출 수 자체는 planner.md와 크게 차이 나지 않는다 — 이번엔 "판단 정확도가 걸리는 부분은 세분성을 유지"했기 때문이다. 대신 **가장 비쌌던 부분(같은 논문을 Need마다 다시 embedding/chunking하는 중복 ingest)은 완전히 사라진다.** call 수보다 이쪽이 실제 비용·지연에 더 크게 기여했던 부분이다.

---

# 5. 기존 구현과의 관계

`paperModule/src/kmed_domestic_lit/deep/research.py` 업그레이드에 가깝다.

- 지금: `fast_search` seed → while 루프(`max_iterations` 있음) → `reformulate_queries`(LLM) → 재검색 → 끝에서 딱 한 번 `run_paperqa` (매번 `Docs()` 새로 생성)
- 바뀌는 것:
  1. 루프 종료 조건을 `len(pool) >= min_evidence_papers`(단순 개수)에서 **Depth Judge의 실제 "aspect들이 해결됐는가" 판단**으로 교체
  2. `paperqa_adapter.py`가 호출마다 새 `Docs()`를 만드는 대신, **Deep Research 세션 동안 하나의 Docs를 유지**하며 라운드마다 incremental add
  3. PaperQA2 조회를 goal 전체로 한 번이 아니라 **aspect별로 개별 조회** (같은 Docs, 여러 번 `aquery`)
  4. `reformulate_queries`가 만드는 검색어를 Depth Judge가 지목한 missing_aspects 기반으로 생성

기존 `deep/` 모듈 세 파일(`research.py`, `planner.py`, `paperqa_adapter.py`)을 이 방향으로 고치면 됩니다. 반영할까요?
