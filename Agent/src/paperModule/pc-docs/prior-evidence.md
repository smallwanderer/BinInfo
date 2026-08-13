# 부록 A — 기존 시스템 조사

---

## 1. 오픈소스 — 직접 가져다 쓸 수 있는 것

### 1.1 PaperQA2 (Future-House/paper-qa) — 최우선 참조

Apache 2.0, GitHub 7,000+ stars. 2024년 논문에서 PhD·박사후 연구원 대비 초인적 성능을 보고했고, RAG-QA Arena 과학 벤치마크에서 차순위 도구보다 10점 이상 앞섰습니다.

**차용할 핵심 설계 3가지:**

1. RCS (Retrieval-augmented Contextual Summarization)

PaperQA2는 검색된 청크를 그대로 답변 프롬프트에 넣지 않음. 대신 각 청크를 질의 맥락에서 요약하면서 동시에 관련도 점수를 매겨 그 요약본만 최종 답변에 씀.

중요한 점은 요약 프롬프트에 인용수와 저널 품질 추정치를 함께 넣어버림. 즉 인용수를 별도 점수 축으로 계산할 필요 없고, LLM이 요약하면서 통합 판단하도록 컨텍스트로 제공할 수 있음.

즉, 결정론 신호는 계산해서 `signals` 필드로 노출하되, 동시에 RCS 프롬프트의 컨텍스트로도 주입하는 형태로 구현. 가중치 튜닝 부담이 크게 줄고 설명가능성도 유지됨.

2. Citation Traversal

인용 그래프를 계층적 인덱스처럼 써서 recall을 보강하는 별도 툴임. v0.1에서는 `find_related`라는 부수 툴로 뒀지만, 검색 파이프라인의 정식 단계로 올릴 수 있음. 한의학처럼 용어가 흩어진 도메인에서는 키워드 검색이 놓친 논문을 "이미 찾은 좋은 논문이 인용한 논문"으로 건지는 경로로 활용 가능성 존재.

3. 에이전트가 툴을 임의 순서로 호출

Paper Search / Gather Evidence / Generate Answer 세 툴을 LLM 에이전트가 자유 순서로 호출함. 좁은 검색과 넓은 검색을 섞거나, evidence 수집과 답변 생성에서 다른 표현을 쓰는 식임. v0.1의 고정 그래프(PLAN→SEARCH→SCORE→JUDGE→REFLECT)보다 유연함.

```
우리 코드                      PaperQA2
─────────────────────────────────────────────
한의학 용어 정규화  ──┐
KCI/국내 소스 어댑터 ─┼──▶ 커스텀 검색 소스로 주입
intent 프로파일    ──┘
                          RCS 랭킹·요약  ← 그대로 사용
                          Citation Traversal ← 그대로 사용
                          답변 생성·인용 ← 그대로 사용
```

주의: 최근 CalVer 전환과 Edison Scientific 문서 이관이 있었으므로 **착수 전 현재 라이선스와 API 안정성을 반드시 재확인**하십시오.

### 1.2 OpenScholar / Ai2 Scholar QA — 인용 귀속 설계 참조

OpenScholar는 AI2·워싱턴대 공동 연구로 **2026년 2월 Nature 게재**됐습니다. 4,500만 편 OA 논문 datastore를 검색해 인용 근거가 붙은 답변을 생성합니다.

주목할 수치: 범용 LLM은 인용을 78~90% 확률로 환각하는 반면 OpenScholar는 인간 전문가 수준의 인용 정확도를 달성했고, PhD급 전문가 16명 평가에서 전문가 작성 답변보다 선호된 비율이 GPT-4o 증강 버전 기준 70%였습니다.

**코드·모델 체크포인트·리트리버/리랭커 가중치·검색 인덱스·학습 데이터·평가 벤치마크를 전부 공개**한 첫 사례입니다. 리랭커 가중치는 바로 실험해볼 수 있습니다.

후속인 **Ai2 Scholar QA**는 ScholarQA-CS 벤치마크에서 OpenScholar, PaperQA2, Perplexity Sonar Deep Research, STORM을 모두 앞섰습니다. 다만 이 벤치마크는 컴퓨터과학 도메인이라 **한의학 문헌에서의 성능은 별개 검증 대상**입니다.

**차용 포인트:** 인용 귀속(attribution) 검증 메커니즘, self-feedback 루프. 신약개발 맥락에서 "이 논문이 실제로 그렇게 말했는가"의 검증은 필수입니다.

### 1.3 paper-search-mcp (openags) — 소스 어댑터 재사용

arXiv, PubMed, bioRxiv, medRxiv, Semantic Scholar, Crossref, OpenAlex, PMC, CORE, **Europe PMC**, DOAJ, Zenodo, Unpaywall 등 20여 개 소스 어댑터가 이미 구현돼 있고 MCP·CLI·Skill 형태로 배포됩니다.

**랭킹 기능은 없습니다** — 단순 검색·다운로드 프록시입니다. 그래서 이걸 최종 답으로 쓸 수는 없지만, 설계서 Phase 1의 소스 어댑터 작업 상당량을 절약할 수 있습니다. 유사한 것으로 `Scientific-Papers-MCP`(arXiv + OpenAlex + PMC), `academic-search-mcp`(S2 + Crossref + OpenAlex + PubMed)가 있습니다.

> 다만 **OpenAlex의 2026-02 API 키 의무화가 반영됐는지 확인**하십시오. 그 이전에 작성된 어댑터는 `mailto` 파라미터를 쓰고 있어 그대로는 동작하지 않습니다.

---

## 2. 도메인 선행연구 — 이게 더 중요합니다

한의학 자체는 아니지만 **중의학(TCM) + 신약개발 + LLM 에이전트** 조합의 선행연구가 2025~2026년에 여럿 나왔습니다. 목표 시스템과 가장 가까운 것들입니다.

### 2.1 TCM-Agent (2026) — 사실상 이 프로젝트의 중의학 버전

LLM 멀티에이전트 기반으로 네트워크 약리학과 한약 발굴을 연결하는 프레임워크입니다. 4개 모듈로 구성됩니다.

1. 사용자 의도 인식 ← **설계서 1장의 intent 분류와 정확히 대응**
2. 자동 알고리즘 분석
3. 리포트 생성·해석
4. **문헌 근거 검색 및 결과 시각화** ← 우리가 만들려는 부분

**반드시 정독하시고, 모듈 경계와 실패 사례를 그대로 참조하십시오.** 특히 "문헌 검색"을 독립 모듈로 두지 않고 네트워크 약리학 분석과 엮은 구조가 신약개발 맥락에서 시사점이 큽니다.

### 2.2 그 외

| 시스템 | 접근 | 우리에게 주는 것 |
|---|---|---|
| **OpenTCM** | GraphRAG 기반 TCM 지식 검색·진단 | 지식그래프 + RAG 결합 방식. 용어 정규화를 KG로 푸는 대안 |
| **TCM-IntelliGraph** | LLM 에이전트를 오케스트레이션 허브로, KG + PPI 네트워크 + GNN | 문헌과 분자 네트워크를 잇는 구조 |
| **ZhiFangDanTai** | 방제(처방) 특화 Graph-RAG 파인튜닝 | 처방 단위 검색 — 육미지황탕 같은 복합 처방 처리 |
| **BATMAN-TCM2** | 한약 성분-타깃 상호작용 DB | **문헌만으로는 부족합니다.** 신약개발 에이전트라면 이 계층이 필요 |
| **TCM-Eval** | 전문가 수준 동적·확장형 벤치마크 | **골든셋 설계 방법론.** 설계서 4.6의 최대 리스크를 완화 |

> **설계서 10장 1번(골든셋 라벨러 확보)에 대한 답이 여기 있습니다.** TCM-Eval과 LitQA2의 문항 설계 방식을 차용하면 백지에서 시작하는 것보다 훨씬 적은 전문가 시간으로 평가셋을 만들 수 있습니다.

---

## 3. 상용 서비스 — 참조는 되지만 붙일 수는 없음

| 서비스 | 강점 | 우리에게 주는 것 |
|---|---|---|
| **Elicit** | 구조화 스크리닝, 포함/배제 기준, 컬럼 단위 데이터 추출 | 체계적 문헌고찰 워크플로 UX. `summarize_paper`의 출력 스키마 참조 |
| **Consensus** | Semantic Scholar 2억 편 기반. **Consensus Meter**로 근거의 무게를 시각화 | 설계서의 `check_evidence` 툴이 지향할 형태. 한의학은 근거 논쟁이 많아 특히 유용 |
| **Undermind** | 재귀적 심층 검색 | 설계서 7.1 REFLECT 루프의 참조 사례 |
| **SciSpace** | 탐색→작성 파이프라인, 생의학 전문 에이전트 | |

전부 API로 도메인 커스터마이즈가 불가능하거나 한의학 용어 처리를 하지 않습니다. **다만 Consensus Meter 방식의 근거 대조 UI는 차용 가치가 높습니다.**

여러 도구를 조합해 쓰는 것이 실무 관행이라는 점도 참고할 만합니다 — 하나로 전부 해결하려 하지 않는 편이 낫습니다.

---

## 4. Build vs Adopt 결정표

| 구성요소 | 결정 | 근거 |
|---|---|---|
| 소스 어댑터 (OpenAlex/EuropePMC/S2) | **Adopt** — paper-search-mcp 참조 | 이미 검증됨. OpenAlex 키 의무화만 패치 |
| RRF 융합 | **Adopt** — PaperQA2 내장 검색 결합 사용 | 자체 RRF는 PaperQA2 위에 얹으면 불필요 |
| 랭킹·요약 (RCS) | **Adopt** | SOTA 검증됨. 직접 만들 이유 없음 |
| Citation Traversal | **Adopt** | |
| 인용 귀속 검증 | **Adopt** — OpenScholar 설계 참조 | 환각 인용은 신약개발 맥락에서 치명적 |
| **한의학 용어 정규화** | **Build** | 선행연구 없음. 이 프로젝트의 존재 이유 |
| **신약개발 intent 프로파일** | **Build** | 기전/임상/안전성/지형 4축은 도메인 고유 |
| **KCI 국내 문헌 채널** | **Build** | 선행연구 전무 |
| novelty 지표 | **Defer** | 설계서 4.4대로 프록시 + LLM 채점으로 시작 |
| 평가셋 | **Build (방법론은 Adopt)** | LitQA2·TCM-Eval 방식으로 한의학 문항 작성 |

---

## 5. 수정된 로드맵

기존 시스템 활용으로 Phase 1~2가 크게 단축됩니다.

| Phase | 기존 (v0.1) | 수정안 | 내용 |
|---|---|---|---|
| **0** (신규, 1주) | — | **선행연구 실측** | PaperQA2를 한의학 질의 10개로 그대로 돌려봄. Ai2 Scholar QA도 동일 질의로 비교. **어디서 깨지는지 확인** |
| **1** | 2~3주 | **1~1.5주** | PaperQA2 위에 한의학 용어 정규화 레이어 + 커스텀 소스 주입 |
| **2** | 2주 | **2주** | intent 프로파일, 골든셋 30~50, nDCG 평가 (변동 없음 — 여기가 실제 작업량) |
| **3** | 2주 | **1주** | MCP 래퍼 + 상위 에이전트 부착 |
| **4** | 선택 | 선택 | KCI, BATMAN-TCM2 연동, novelty 배치 |

**Phase 0을 반드시 먼저 하십시오.** PaperQA2가 한의학 질의에서 이미 충분히 잘한다면 우리가 만들 것은 정규화 레이어뿐이고, 심하게 깨진다면 그 실패 양상이 설계의 나머지를 결정합니다. 어느 쪽이든 일주일로 얻는 정보가 큽니다.

구체적 실측 질의 예시:

```
1. 육미지황탕의 신장 보호 기전                    ← 처방명 이형태 처리 테스트
2. 황금 추출물의 항염 활성과 NF-κB 경로            ← 약재명↔학명↔성분 매핑 테스트
3. 만성 요통에 대한 침 치료 RCT의 최신 근거        ← 임상 evidence 계층 테스트
4. 감초 장기 복용의 간독성 보고                    ← 안전성 recall 테스트
5. 한약재 유래 항암 후보물질 최근 5년 동향          ← novelty/지형 테스트
```

1·2번에서 깨질 가능성이 높고, 그게 우리 정규화 레이어의 가치를 정량화해줍니다.

---

## 6. 설계서 v0.1에서 바뀌는 부분 요약

- **4장** — Stage 2/3 분리를 유지하되, 결정론 신호를 **RCS 프롬프트 컨텍스트로도 주입**하는 하이브리드로 변경. 가중치 튜닝 부담 감소
- **5장** — `find_related`를 부수 툴에서 **Citation Traversal 정식 단계**로 승격
- **6장** — `ranking/` 모듈 대부분이 PaperQA2 호출로 대체. 저장소 구조 축소
- **7장** — 고정 그래프 대신 PaperQA2의 자유 툴 호출 방식 검토 (REFLECT 루프는 유지)
- **9장** — Phase 0 신설, Phase 1·3 단축
- **10장 1번** — LitQA2/TCM-Eval 방법론 차용으로 골든셋 리스크 일부 완화

---

## 참고

**오픈소스**
- [PaperQA2 — Future-House/paper-qa (GitHub)](https://github.com/future-house/paper-qa) · [Language agents achieve superhuman synthesis of scientific knowledge (arXiv 2409.13740)](https://arxiv.org/html/2409.13740v2) · [RAG-QA Arena SOTA 발표](https://www.futurehouse.org/research-announcements/paperqa2-achieves-sota-performance-on-rag-qa-arena-science-benchmark)
- [OpenScholar (arXiv 2411.14199)](https://arxiv.org/abs/2411.14199) · [Nature 게재본 (2026-02)](https://www.nature.com/articles/s41586-025-10072-4) · [Ai2 Scholar QA (arXiv 2504.10861)](https://ui.adsabs.harvard.edu/abs/arXiv:2504.10861)
- [paper-search-mcp (GitHub)](https://github.com/openags/paper-search-mcp) · [Scientific-Papers-MCP](https://github.com/benedict2310/Scientific-Papers-MCP)

**도메인 선행연구**
- [TCM-Agent: Advancing Network Pharmacology and Herbal Medicine Discovery with LLM-Based Multi-Agent Systems](https://www.sciencedirect.com/science/article/pii/S2095177926000365)
- [OpenTCM: A GraphRAG-Empowered LLM-based System for TCM Knowledge Retrieval and Diagnosis](https://www.researchgate.net/publication/391282232_OpenTCM_A_GraphRAG-Empowered_LLM-based_System_for_Traditional_Chinese_Medicine_Knowledge_Retrieval_and_Diagnosis)
- [ZhiFangDanTai: Graph-based RAG for TCM Formula (arXiv 2509.05867)](https://arxiv.org/pdf/2509.05867)
- [TCM-Eval: Expert-Level Dynamic and Extensible Benchmark for TCM (arXiv 2511.07148)](https://arxiv.org/pdf/2511.07148)
- [Integrating knowledge graphs with ancient Chinese medicine classics (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12502320/)

**상용 비교**
- [Best AI tools for medical research 2026](https://www.iatrox.com/blog/best-ai-tools-medical-research-2026-elicit-consensus-semantic-scholar-perplexity)
- [10 Best AI Tools for Life-Science Literature Review (2026)](https://bioskepsis.ai/blog/best-ai-tools-for-literature-review-2026)