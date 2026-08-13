현재 문서는 사용자 질의를 바탕으로 에이전트가 계획을 수립하고, 툴을 호출하는 과정을 기술하는 문서이다.

# 1. 시스템 아키텍처

![architecture](./images/planner_system_architecture.png)

# 2. 동작 과정

동작 과정은 Fast / Deep 두 깊이로 나눠 탐색을 수행한다.

## (공통) Entry Agent

사용자가 궁극적으로 무엇을 원하는지 파악하는 부분입니다.
요청의 의미와 명시적 조건을 구조화합니다.

요청의 답변에 **반드시** 포함되어야 하는 항목들을 구조화합니다.

## Fast

하나의 정보 요구를 수평적으로 확장하여 논문을 찾는다.

### Fast Planner
목표: 현재 어떤 관련 연구들이 존재하는지 넓고 빠르게 확인

사용자 질의: "뇌졸중 후유증에 대한 침치료의 효과, 부작용, 적용범위 관련 연구논문 IF 5 이상 찾아줘."

사용자 질의 분해:
Q1. 뇌혈관질환후유증 + 침치료 + 효과
Q2. 뇌혈관질환후유증 + 침치료 + 부작용
Q3. 뇌혈관질환후유증 + 침치료 + 적용범위
Q4. 뇌혈관질환후유증 + 침치료

하나의 information need를 더 잘 검색하기 위한 병렬 query

### Query Generation

적용할 수 있는 Tool에 제한하여 알맞는 tool을 선택하거나 사용자가 원하는 검색 결과를 알맞게 표현해준다. 

{
  "query": ["뇌혈관질환후유증", "침치료", "효과"],
  "query_index": 1,
  "search_queries": [
    {
      "source": "kci",
      "query": "뇌혈관질환후유증 침치료 효과"
    },
    {
      "source": "pubmed",
      "query": "post-stroke sequelae acupuncture"
    },
  ],
}

### Evidence Landscape

Fast에서 발견된 논문들을 Deep Coordinator 혹은 사용자가 이해할 수 있도록 요약해주는 계층

---

## Deep

사용자 목표를 1차적으로 여러 정보 요구로 분해하고, 실제 근거를 본 뒤 부족한 정보 요구만 수직적으로 깊게 확장한다.

### Deep Architecture
```text
            Deep 요청
                │
                ▼
        Deep Coordinator
                │
        User Goal + Fast Results
                │
                ▼
        Information Needs
    ┌────────┬────────┬────────┐
    ▼        ▼        ▼        ▼
    N1       N2       N3       N4
    │        │        │        │
    └──── 각 Need별 Fast ─────┘
                │
                ▼
        KCI / PubMed
                │
                ▼
        Relevant Papers
                │
                ▼
            PaperQA2
                │
                ▼
        Evidence State
                │
                ▼
        Critic "원래 목표가 해결됐나?"
                │
    ┌────────────┴────────────┐
    │                         │
    YES                       NO
    │                         │
    ▼                         ▼
    Synthesis               Missing Need
                            │
                            ▼
                    Deep Coordinator loop
                            │
                필요한 Need만 추가 분해
                            │
                            ▼
                        Fast → PaperQA2
```


### Deep Planer

사용자의 목표에 충분히 답하려면 무엇을 알아야 하는가? 에 대해서 단계적으로 질문을 생성한다.

Fast에서 전달한 User Goal + Evidence Landscape를 바탕으로 Deep Planer는 Information Needs를 생성한다.

### 사용 예시

사용자 질의: "뇌혈관질환후유증에 침치료의 효과와 안정성 확인."

예상 답변:
{
  "goal": "뇌혈관질환후유증에서 침치료 효과 평가",
  "information_needs": [
    {
      "id": "N1",
      "question": "침치료가 주요 후유증을 개선하는가?"
    },
    {
      "id": "N2",
      "question": "어떤 outcome에서 효과가 나타나는가?"
    },
    {
      "id": "N3",
      "question": "고품질 임상근거는 어떤 결론을 내리는가?"
    },
    {
      "id": "N4",
      "question": "근거의 수준과 일관성은 어떠한가?"
    }
  ]
}

검색어를 만드는 Agent가 아니라 연구 문제를 구조화하는 Agent입니다. Origene의 Coordinator에 가까운 역할입니다.

### Information Needs

구조화된 연구 문제를 작업 단위로 나누는 역할입니다.

```text
{
  "id": "N3",
  "question": "고품질 임상시험과 체계적 문헌고찰은 침치료의 효과에 대해 어떤 결론을 내리는가?",
  "priority": "high"
}
```

각 Need를 독립적으로 조사한다.

### Fast Loop

각 Information Need는 다시 Fast Scout 기능을 재사용합니다.
```text
N3:
"고품질 임상근거는?"

        ↓

Fast Query Expansion

KCI
- 뇌졸중 후유증 침 무작위 대조시험
- 뇌졸중 침 체계적 문헌고찰

PubMed
- post-stroke acupuncture randomized controlled trial
- acupuncture stroke systematic review
```

### Relevant Paper Selection

찾은 논문 중 해당 Information Need에 실제로 관련된 논문만 남김

여기에서 LLM은 "이 논문이 N3에 답하는 데 직접 관련 있는가?" 정도만 판단합니다.

### PaperQA2

결국 구현하지 않아도 되는 것. 선택된 논문 내부에서 실제 근거를 깊게 찾는다.

PaperQA2와 중복되므로 다음을 자체 구현할 필요가 낮습니다.

문서 내부 iterative query refinement
chunk retrieval loop
passage reranking
contextual summarization
evidence passage selection
논문 corpus 내부에서의 반복 evidence gathering

PaperQA2가 이 역할을 이미 제공합니다.

### Evidence State

PaperQA2 결과를 Need별 상태로 구조화합니다.

### Critic

PaperQA2가 논문을 잘 읽었는지가 아니라, 원래 사용자가 알고 싶었던 것이 해결되었는지를 판단

### Re-planning / Loop

Critic이 부족하다고 판단했다고 모든 것을 다시 조사하지 않습니다.

부족한 부분에 대해서만 재탐색을 이어갑니다.

```text
N5: 안전성
   ↓
왜 답이 부족한가?
   ↓
필요하면 더 구체적으로 분해

N5.1 침치료 관련 이상반응은?
N5.2 중대한 adverse event가 보고되었는가?
N5.3 RCT에서 안전성 reporting은 충분한가?
```

### Synthesis

Information Need별 근거를 다시 사용자의 원래 질문에 맞춰 통합

