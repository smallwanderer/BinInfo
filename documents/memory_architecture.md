# Memory Architecture
 
이 문서는 (1) 일반 LLM 에이전트 분야의 memory 아키텍처 문헌과 (2) 신약개발 특화 에이전트에서 memory가 실제로 어떻게 구현되는지를 함께 정리한다.
 
## 목차
 
- [1. 왜 Memory가 필요한가](#1-왜-memory가-필요한가)
- [2. 일반 LLM 에이전트 Memory 아키텍처](#2-일반-llm-에이전트-memory-아키텍처)
  - [2.1 분류 체계 ① — Source / Form / Operation (Zhang et al., 2024)](#21-분류-체계-①--source--form--operation-zhang-et-al-2024)
  - [2.2 분류 체계 ② — 인지과학 기반 Working/Episodic/Semantic/Procedural](#22-분류-체계--인지과학-기반-workingepisodicsemanticprocedural)
  - [2.3 대표 아키텍처](#23-대표-아키텍처)
  - [2.4 최신 종합 서베이 — Du (2026)](#24-최신-종합-서베이--du-2026)
- [3. 신약개발 에이전트에서의 Memory 아키텍처](#3-신약개발-에이전트에서의-memory-아키텍처)
  - [3.1 Seal et al.(2026)이 제시한 구조](#31-seal-et-al2026이-제시한-구조)
  - [3.2 도메인 특화 시스템의 memory 설계 사례](#32-도메인-특화-시스템의-memory-설계-사례)
- [4. 일반 vs 신약개발 특화: 요약 비교](#4-일반-vs-신약개발-특화-요약-비교)
- [참고 자료](#참고-자료)
## 용어 설명
 
- **ICL(In-Context Learning)**: LLM의 Prompt 내에서 Few-shot learning, prompt engineering을 통해 context 내에서 학습하는 것. LLM 모델 자체의 weight를 변경하지 않고, input data 내에서 학습하는 것.
- **Context Window**: LLM이 한 번의 추론에서 참조할 수 있는 입력 토큰의 최대 범위. Working memory(단기기억)의 물리적 한계에 해당하며, 이 범위를 넘는 정보는 별도의 저장소(외부 장기기억)로 옮기거나 요약해야 한다.
- **RAG(Retrieval-Augmented Generation)**: LLM이 답변을 생성하기 전에 외부 문서·DB에서 관련 정보를 검색(retrieval)해 프롬프트에 포함시키는 방식. 모델 재학습 없이 최신·전문 지식을 반영할 수 있어 외부 장기기억의 표준 구현체로 쓰인다.
- **벡터 DB(Vector Database)**: 텍스트·이미지 등을 임베딩(embedding, 고차원 숫자 벡터)으로 변환해 저장하고, 벡터 간 유사도(코사인 유사도 등)로 검색하는 데이터베이스. 표준 RAG의 저장소로 가장 많이 쓰인다.
- **Agentic RAG**: 에이전트가 단순히 한 번 검색해 답을 생성하는 것이 아니라, 검색 쿼리를 스스로 재구성하거나 여러 차례 반복 검색하는 등 검색 전략 자체를 능동적으로 조정하는 RAG 방식.
- **GraphRAG**: 문서를 텍스트 청크로 쪼개 저장하는 대신, 지식을 그래프(개체-관계) 구조로 저장하고 그래프를 탐색(traverse)하며 정보를 검색하는 RAG 방식. 개체 간 다단계 관계(예: 약물-유전자-질병 연결)를 텍스트 유사도만으로는 찾기 어려운 경우에 강점이 있다.
- **Knowledge Graph(지식그래프)**: 개체(entity)와 그 사이의 관계(relation)를 노드-엣지 형태로 표현한 데이터 구조. Semantic memory의 대표적인 저장 형태.
- **Fine-Tuning**: 사전학습된 모델의 가중치를 특정 작업·스타일·지시사항에 맞게 추가 학습으로 조정하는 것. Internal long-term memory를 갱신하는 방법 중 하나.
- **Continued Pretraining**: 새로운 도메인 특화 데이터로 모델을 이어서 사전학습해, 모델 가중치 자체에 새로운 사실 지식을 반영하는 것.
- **Model Merging**: 여러 특화 모델의 가중치를 결합해 하나의 모델로 합치는 기법. 각 모델의 학습 데이터가 독점적(proprietary)이라 공유가 어려울 때 지식을 통합하는 대안으로 쓰인다.
- **MCP(Model Context Protocol)**: Anthropic이 개발한, 에이전트가 외부 데이터 소스·도구와 통신하기 위한 표준 인터페이스 프로토콜. ChEMBL, PubMed 같은 서로 다른 DB를 동일한 방식으로 호출할 수 있게 해준다.
- **Tool Calling(Function Calling)**: LLM이 미리 정의된 함수·API를 호출해 외부 정보를 가져오거나 작업을 수행하도록 하는 메커니즘. 검색 결과나 계산 결과가 다시 컨텍스트(단기기억)에 포함되는 방식으로 memory와 연결된다.
- **ReAct**: "Reasoning + Acting"의 약자로, LLM이 추론(생각)과 행동(도구 호출)을 번갈아 수행하며 관찰 결과를 다음 추론에 반영하는 가장 기본적인 에이전트 아키텍처.
- **Reflection**: 에이전트가 자신의 과거 행동·관찰을 되돌아보고 더 상위 수준의 통찰이나 교훈을 스스로 생성해 memory에 다시 저장하는 절차. Generative Agents와 Reflexion 모두에서 핵심 메커니즘으로 쓰인다.
- **Episodic / Semantic / Procedural / Working Memory**: 인지심리학에서 차용한 memory 분류. Episodic은 사건·행동의 시간순 기록, Semantic은 일반화된 사실 지식, Procedural은 작업 수행 절차, Working은 현재 처리 중인 즉각적 정보를 가리킨다.
- **SAR(Structure-Activity Relationship, 구조-활성 관계)**: 화합물의 화학 구조 변화가 생물학적 활성에 미치는 영향의 패턴. 신약개발 에이전트의 memory가 주로 축적하는 지식 유형 중 하나.
- **DTI(Drug-Target Interaction)**: 약물(화합물)과 생체 타겟(단백질 등) 간의 결합·상호작용. 이를 예측하는 것이 신약개발 AI의 대표적인 벤치마크 과제 중 하나다.
- **LangChain**: LLM에 외부 도구·메모리·체인(연속된 프롬프트 호출)을 연결하기 쉽게 만들어주는 오픈소스 프레임워크. ChemCrow 등 여러 화학·신약개발 에이전트의 구현에 쓰였다.

## 1. 왜 Memory가 필요한가

원본 LLM은 고정된 context window 안에서만 동작하는 사실상 stateless 시스템이다. 반면 에이전트는 장기간에 걸친 복잡한 환경-에이전트 상호작용(여러 세션에 걸친 실험, 반복되는 DMTA 사이클 등)을 처리해야 하므로, 과거 경험을 저장 및 학습한 memory 모듈이 에이전트의 "self-evolving" 능력을 뒷받침하는 핵심 구성요소가 된다.

## 2. 일반 LLM 에이전트 Memory 아키텍처

### 2.1 분류 체계 ① — Source / Form / Operation (Zhang et al., 2024)

*A Survey on the Memory Mechanism of Large Language Model based Agents* (arXiv:2404.13501, Renmin University of China·Huawei Noah's Ark Lab, ACM TOIS 게재)는 이 분야 최초의 종합 서베이로, memory를 3가지 축으로 분류한다.

- **Source(출처)**: 에이전트 자신의 행동·경험에서 오는 내부 정보 vs 환경, 사용자, 다른 에이전트로부터 오는 외부 정보.
- **Form(형태)**: 자연어 텍스트로 저장되는 memory vs 모델 파라미터(가중치) 형태로 인코딩되는 memory.
- **Operation(연산)**: **Memory Writing**(관찰·경험을 저장) → **Memory Management**(압축·요약·중요도 기반 망각/유지) → **Memory Reading**(현재 태스크에 관련된 memory를 검색해 활용)의 순환 루프.

### 2.2 분류 체계 ② — 인지과학 기반 Working/Episodic/Semantic/Procedural

여러 서베이가 인간 인지심리학의 memory 분류를 차용해 LLM 에이전트에 적용한다.

- **Working memory(단기기억)**: 현재 context window 안의 대화 이력, API 응답, 참조 파일 등 즉각적으로 쓰이는 정보.
- **Episodic memory**: "언제 어떤 행동을 했고 어떤 결과가 나왔는가" 같은 시간순 사건·행동 이력.
- **Semantic memory**: 지식그래프, 문서, API 스키마 등 일반화된 사실 지식.
- **Procedural memory**: 특정 작업을 수행하는 절차·규칙(스킬)에 대한 기억.

### 2.3 대표 아키텍처

- **MemGPT** (Packer et al., 2023) — OS의 virtual memory paging 개념을 LLM에 적용. 빠른 티어인 *main context*와 느린 티어인 *recall storage / archival storage*를 구분하고, LLM이 함수 호출(function calling)로 두 티어 사이의 정보를 스스로 "페이징"한다. 장문 대화의 일관성 유지, 컨텍스트 한계를 넘는 문서 분석에 활용됨.
- **Generative Agents** (Park et al., 2023, Stanford·Google DeepMind) — 자연어 형태의 *memory stream*에 모든 관찰을 저장하고, **recency(최신성, 지수 감쇠) × relevance(관련성, 임베딩 유사도) × importance(중요도, LLM 자체 평가 점수)**를 조합한 retrieval scoring function으로 검색한다. 누적 중요도가 임계값을 넘으면 관련 관찰들을 클러스터링해 상위 수준의 통찰을 생성하는 **reflection** 단계를 주기적으로 실행, 그 결과를 다시 memory stream에 기록한다.
- **Reflexion** (Shinn et al., 2023) — 실패한 시도에 대해 LLM이 언어적 자기비판(self-critique)을 생성하고, 이를 gradient update 없이 episodic memory buffer에 저장했다가 다음 시도의 컨텍스트에 주입하는 "verbal reinforcement learning" 방식. HumanEval에서 reflection 없는 GPT-4(80%) 대비 91% pass@1을 기록.
- **Agentic RAG / GraphRAG** — 외부 장기기억의 대표적 구현체. 표준 RAG는 문서를 임베딩해 vector DB에 저장하고 유사도 검색으로 불러오며, Agentic RAG는 에이전트가 검색 전략 자체를 능동적으로 조정한다. GraphRAG는 지식을 그래프 구조로 저장해 개체 간 관계를 탐색하는 방식으로, 텍스트 청크 유사도만으로는 놓치기 쉬운 희귀하지만 중요한 연관관계(예: 특정 질병의 새로운 drug–gene–disease 연결)를 더 잘 찾아낸다는 연구도 있다.

### 2.4 최신 종합 서베이 — Du (2026)

*Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers* (arXiv:2603.07670, 2022~2026초 문헌 커버)는 memory를 **write → manage → read** 순환 루프로 형식화하고, **temporal scope(시간 범위) × representational substrate(표현 형태) × control policy(제어 정책)**의 3차원 taxonomy를 제시한다. 메커니즘을 5개 계열로 구분: context-resident compression(컨텍스트 내 압축), retrieval-augmented stores(검색 기반 외부 저장), reflective self-improvement(반성적 자기개선, Reflexion 계열), hierarchical virtual context(계층적 가상 컨텍스트, MemGPT 계열), policy-learned management(학습된 관리 정책).

## 3. 신약개발 에이전트에서의 Memory 아키텍처

### 3.1 Seal et al.(2026)이 제시한 구조

- **Short-term memory**: 현재 context window에 담긴 대화 이력·API 응답 등 즉시 활용되는 정보. In-Context Learning(ICL)을 가능하게 함.
- **Long-term memory**
  - *Internal*: 모델 가중치에 인코딩된 파라메트릭 지식. Continued Pretraining, Fine-Tuning, Model Merging(독점 데이터 보유 시 여러 특화 모델의 가중치를 결합)으로 갱신.
  - *External*: RAG 기반의 동적·영속적 저장소. 표준 RAG(벡터 DB) → Agentic RAG → GraphRAG(신약 맥락에서 드문 drug–gene–disease 연관 발굴에 강점) 순으로 정교화.
- **Memory 확장 수단**: Tool Calling과 Model Context Protocol(MCP, Anthropic 개발)을 통해 ChEMBL·PubMed 같은 외부 DB를 실시간 조회하고, 그 결과를 short-term memory에 편입.
- **실제 사례**
  - 문헌분석 에이전트: **dual-memory 아키텍처** — short-term은 세션별 발견사항·중간 결과, long-term은 scaffold-property 패턴과 과거 쿼리 전략을 저장해 프로젝트 간에도 이전에 분석한 화합물 시리즈를 재인식.
  - Virtual Scientist(Kiin Bio) 플랫폼: 여러 전문 에이전트가 개별적으로 작동하면서도 **공유 조직 메모리(shared organisational memory)**에 기여해 팀 단위 의사결정을 조율.

신약개발 맥락에서 memory에 실제로 축적되는 지식의 예: SAR(구조-활성 관계) 패턴, 누적된 독성 발견 사례, 과거 discovery 프로그램에서 마주친 장애물과 그 해결책 등.

### 3.2 도메인 특화 시스템의 memory 설계 사례

- **PharmAgents** (arXiv:2503.22164) — 타겟 발굴부터 리드 최적화·전임상 평가까지 파이프라인 전체를 모사하는 멀티에이전트 시스템. 에이전트 간 구조화된 지식 교환과 자동 최적화 루프를 통해 "self-evolvement"를 지원한다고 명시 — 즉 과거 설계 경험을 축적해 향후 신약 설계를 개선하는 방식으로 memory를 활용.
- **DrugAgent** (arXiv:2411.15692) — LLM 기반 planner가 전략을 생성·정제하고, 별도의 instructor 모듈이 도메인 지식을 결합해 전략을 검증. DTI 예측 등 벤치마크에서 단일 에이전트 대비 ROC-AUC 4.92% 개선.
- **ChemCrow** (Bran, Cox, White et al., *Nature Machine Intelligence*, 2024) — GPT-4 + 18개 전문가 설계 화학 도구를 LangChain으로 orchestration. Memory보다는 **tool-augmentation**에 무게가 실려 있으며, 명시적인 장기기억 모듈은 상대적으로 제한적 — 이는 "모든 신약개발 에이전트가 정교한 memory를 갖춘 것은 아니며, tool 호출 자체로 상당 부분을 대체하는 설계도 있다"는 점을 보여주는 대조 사례.

## 4. 일반 vs 신약개발 특화: 요약 비교

| 구분 | 일반 LLM 에이전트 (학계 서베이) | 신약개발 에이전트 (Seal et al. 2026 등) |
|---|---|---|
| 단기기억 | Context window, working memory | Context window 기반 (동일) |
| 장기기억 저장 형태 | Vector DB / Knowledge graph / 모델 가중치 | RAG 기반 vector DB, GraphRAG, 도메인 DB(ChEMBL 등) 실시간 조회 |
| 대표 메커니즘 | MemGPT(paging), Generative Agents(reflection), Reflexion(verbal RL) | Dual-memory(세션별 vs 프로젝트 간), 공유 조직 메모리(멀티에이전트) |
| 저장되는 지식 | 대화 이력, 사건, 일반 지식, 절차 | SAR 패턴, 독성 발견 사례, 화합물 시리즈, 쿼리 전략 |
| 성숙도 | 이론·벤치마크 중심, 빠르게 발전 중 | 아직 초기 단계 — 시스템마다 memory 정교화 수준 편차 큼(ChemCrow처럼 tool 중심 vs PharmAgents처럼 self-evolvement 명시) |

## 참고 자료

- [Seal, Huynh et al., "AI Agents in Drug Discovery" | arXiv:2510.27130](https://arxiv.org/pdf/2510.27130)
- [Huynh, Seal et al., "AI agents in drug discovery: applications and case studies" | Drug Discov Today, 2026 (PubMed)](https://pubmed.ncbi.nlm.nih.gov/41887499/)
- [Zhang et al., "A Survey on the Memory Mechanism of Large Language Model based Agents" | arXiv:2404.13501](https://arxiv.org/abs/2404.13501)
- [GitHub repo tracking LLM agent memory literature](https://github.com/nuster1128/LLM_Agent_Memory_Survey)
- [Du, "Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers" | arXiv:2603.07670](https://arxiv.org/abs/2603.07670)
- [Packer et al., "MemGPT: Towards LLMs as Operating Systems"](https://shishirpatil.github.io/publications/memgpt-2023.pdf)
- [Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" 아키텍처 해설 | AgentPatterns.ai](https://agentpatterns.ai/agent-design/generative-agents-memory-stream/)
- [Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" | NeurIPS 2023](https://neurips.cc/virtual/2023/poster/70114)
- [PharmAgents: Building a Virtual Pharma with Large Language Model Agents | arXiv:2503.22164](https://arxiv.org/html/2503.22164v2)
- [DrugAgent: Automating AI-aided Drug Discovery Programming through LLM Multi-Agent Collaboration | arXiv:2411.15692](https://arxiv.org/html/2411.15692v2)
- [Augmenting large language models with chemistry tools (ChemCrow) | Nature Machine Intelligence](https://www.nature.com/articles/s42256-024-00832-8)