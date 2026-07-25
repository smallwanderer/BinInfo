# 신약 개발 에이전트 관련 사전 조사

## 1. 용어

- **타겟(Target)**: 질병 발생 및 진행에 관여하는 생체 분자(단백질, 유전자, 수용체 등). 약물이 결합하여 조절하고자 하는 대상.
- **화합물(Compound)**: 타겟과 결합하여 기능을 조절할 수 있는 분자. 소분자(분자량 900 Da 이하), 항체, 펩타이드 등이 포함됨.
- **효과(Effect)**: 화합물 혹은 타겟 조작이 만들어내는 관찰 가능한 결과.
- **화합물 스크리닝(HTS, High-Throughput Screening)**: 로봇 자동화, 액체 핸들링 장비, 고감도 검출기를 활용해 수천~수백만 개의 화합물을 짧은 시간 안에 특정 타겟에 대한 생물학적 활성 여부로 검사하는 자동화된 스크리닝 기법. 96, 384, 1536 well 플레이트 기반으로 진행되며, 하루 또는 일주일에 수천 개 이상의 화합물을 처리할 수 있다. 다만 HTS 자체는 독성이나 생체이용률과 같이 신약 개발에 필수적인 특성까지 평가하지는 못하므로, HTS로 발굴된 "히트(hit)"는 이후 추가 검증과 최적화 과정을 거쳐야 한다.
- **히트(Hit)**: HTS 또는 기타 스크리닝을 통해 발굴된 초기 활성 화합물. 이후 Lead Optimization을 통해 개선됨.
- **리드(Lead)**: 타겟에 대해 유효한 활성을 가지면서, in vitro 및 초기 in vivo에서 개선 가능성이 있는 화합물. 이후 Lead Optimization을 통해 개선됨.
- **ADMET**: 흡수(Absorption), 분포(Distribution), 대사(Metabolism), 배설(Excretion), 독성(Toxicity). 약물이 생체 내에서 어떻게 작용하는지, 얼마나 안전한지를 평가하는 지표.

## 2. General Drug Discovery Process

### 2.1 Target Identification and Validation (타겟 발굴 및 검증)

- Proteomics, Genomics/Genetics와 같은 연구 결과들을 바탕으로 후보 타겟을 탐색.
- 환자 혹은 의사가 원하는 타겟으로 결정되는 경우도 있음.
- 해당 타겟이 유효한지 확인(Target Validation).
- 타겟이 질병과 어떠한 관계를 가지는지, 원하는 방향(flow)으로 움직이는지 검증.

### 2.2 Hit Discovery (히트 발굴)

여전히 많은 부분(43% 이상)이 논문이나 연구 자료를 바탕으로 Hit Discovery가 이루어지고 있다. HTS(29%)는 자체 보유 화합물 라이브러리를 대상으로 진행되며, Virtual Screening(14%)은 실제 화합물이 아닌 컴퓨터 상의 가상 화합물을 대상으로 Hit Discovery가 진행된다. 아래 2.2.1~2.2.6은 대표적인 세부 방법론이다.

#### 2.2.1 Phenotypic (표현형 기반 스크리닝)

Phenotypic screening은 특정 타겟을 미리 특정하지 않고, 질병과 관련된 표현형(phenotype)을 먼저 정의한 뒤 이를 재현하는 세포·조직·모델 생물 기반의 assay를 구축해 화합물을 스크리닝하는 방식이다.

- 타겟에 대한 사전 지식 없이도 복잡한 생물학적 기전을 포착할 수 있다는 장점이 있으며, 알려지지 않은 타겟이나 기존에 알려진 타겟의 새로운 작용 기전을 가진 화합물도 발굴할 수 있다.
- 반면 히트 화합물이 어떤 타겟을 통해 작용하는지 규명하는 target deconvolution 과정이 별도로 필요해 시간과 비용이 더 소요될 수 있다.
- 최근 target-based 접근이 기대에 못 미치는 사례가 누적되면서 phenotypic 접근에 대한 관심이 다시 높아지고 있다.

#### 2.2.2 Target-based Hit Identification

Target-based screening은 질병 기전에 관여하는 것으로 확인된 특정 분자 타겟(단백질 등)에 결합·조절하는 화합물을 찾는 방식이다. 타겟에 대한 사전 지식(질병 생물학)을 바탕으로 진행되므로 고효율·저비용의 고처리량 스크리닝이 가능하고, 작용 기전이 명확해 이후 활성 최적화(hit-to-lead) 과정에서 구조-활성 관계(SAR)를 정밀하게 다루기 용이하다. 다만 타겟이 실제 질병 표현형과 얼마나 밀접하게 연결되어 있는지(Target Validation 수준)에 결과의 신뢰도가 크게 좌우된다.

#### 2.2.3 활성평가 방법의 선택과 개발 (Assay Development & Selection)

타겟 검증 이후에는 화합물의 활성을 정량적으로 측정할 assay를 설계·구축해야 한다. Assay는 크게 생화학적 assay(biochemical assay)와 세포 기반 assay(cell-based assay)로 구분된다.

- **Biochemical assay**: 정제된 단백질(효소, 수용체 등)을 이용해 화합물의 결합·억제·활성화 효과를 직접 측정. 효소 활성 assay는 정량적인 kinetic 데이터를 제공하며 hit-to-lead 단계의 기초 assay로 널리 사용된다.
- **Cell-based assay**: 세포 투과성, 대사, 하위 신호전달까지 반영할 수 있어 생리학적 타당성이 높지만, biochemical assay 대비 변동성이 크고 스케일업이 어려워 주로 1차 히트의 2차 확인(secondary confirmation) 용도로 사용된다.

Assay 선택은 타겟 단백질의 생물학적 특성, 스크리닝 규모(처리량), 보유 장비 인프라 등을 종합적으로 고려하여 결정한다.

#### 2.2.4 CADD (Computer-Aided Drug Design)

CADD는 컴퓨터 연산을 활용해 신약 개발의 효율을 높이는 접근법으로, 크게 **구조 기반(Structure-based)** 방식과 **리간드 기반(Ligand-based)** 방식으로 나뉜다.

- **Structure-based**: 타겟 단백질의 3차원 구조를 입력으로 사용하며, 분자 도킹(molecular docking)을 통해 force field 및 스코어링 함수로 리간드의 결합 포즈와 결합력을 예측한다.
- **Ligand-based**: 타겟의 3차원 구조가 알려지지 않은 경우, 이미 알려진 활성 리간드의 화학 구조 정보를 바탕으로 2D/3D 구조 유사도를 계산해 새로운 화합물을 탐색한다.

CADD는 일반적으로 다음 네 단계로 적용된다.

1. Virtual Screening(VS) 프로토콜로 소분자 라이브러리를 타겟에 대해 스크리닝하여 히트/리드 후보 도출.
2. 추가로 알려진 타겟들에 대한 도킹을 통해 선택된 VS 히트의 특이성(selectivity) 평가.
3. In silico 기법으로 히트의 ADMET 특성 예측 및 유망 후보를 리드로 격상.
4. 합성·평가를 위한 개선된 분자 설계를 통해 리드 최적화 지원.

CADD의 발전으로 대규모 화합물 라이브러리에 대한 virtual HTS(vHTS)가 가능해지면서 히트 발굴의 탐색 공간이 크게 확장되었다.

#### 2.2.5 Fragment-Based Drug Discovery (FBDD)

FBDD는 분자량 300 Da 이하의 작은 화학 fragment를 스크리닝하여 타겟과의 결합을 확인한 뒤, 여러 fragment를 연결·성장·병합(growing, linking, merging)해 점차 큰 친화도를 가진 화합물로 발전시키는 방식이다. HTS보다 훨씬 작은 라이브러리로도 넓은 화학 공간을 효율적으로 탐색할 수 있다는 장점이 있다.

- Fragment는 결합력이 약하기 때문에(㎛~mM 수준) 일반적인 활성 assay로는 검출이 어렵고, **SPR(Surface Plasmon Resonance)**, **NMR**, **X-ray crystallography** 같은 고감도 biophysical 기법으로 검출한다.
  - SPR: 소량의 단백질로도 결합의 kinetics·thermodynamics 정보를 제공.
  - NMR: nM~mM 범위의 다양한 결합력을 검출할 수 있고 위양성이 적으며, 여러 fragment를 혼합하여 스크리닝 가능.
  - X-ray crystallography: 원자 수준의 결합 구조 정보를 제공해 히트의 우선순위 결정과 최적화 방향을 안내.
- Vemurafenib, Venetoclax 등 FDA 승인 신약이 FBDD 경로로 개발된 대표 사례.

#### 2.2.6 DNA-Encoded Library (DEL) Screening

DEL 스크리닝은 각 화합물에 고유한 DNA 서열(바코드)을 결합시켜, 수억~수백억 개 규모의 초대형 화합물 라이브러리를 하나의 튜브 안에서 동시에 타겟 단백질과 결합 반응시킨 뒤, 차세대 시퀀싱(NGS)으로 타겟에 결합해 농축된 화합물의 DNA 바코드를 읽어 히트를 식별하는 방식이다. HTS 대비 훨씬 적은 자원으로 훨씬 넓은 화학 공간을 실험적으로 탐색할 수 있어, 최근 가상 스크리닝(virtual screening)과 결합한 형태(virtual DEL screening)로도 활용이 확대되고 있다.


### 2.3 Lead Identification (Hit-to-Lead)

- 스크리닝으로 확보한 히트(hit) 화합물 중 화학적으로 개선 가능성이 높은 물질을 선별하고, 초기 구조-활성 관계(SAR)를 탐색해 리드(lead) 후보로 전환하는 단계.
- 이 단계에서 이미 potency, selectivity, 초기 ADMET 특성에 대한 기초적인 개선이 시작되며, 이후 Lead Optimization으로 이어짐.


### 2.4 Lead Optimization (리드 최적화)

- Biology, Medicinal Chemistry(의약화학), PK(약동학), TOX(독성) 연구자들이 참여하며, 리드 화합물의 역가(potency), 선택성(selectivity), 약동학(PK), 독성(ADMET) 프로파일을 반복적·단계적으로 개선해 전임상 후보물질(preclinical candidate)을 도출하는 과정.
- 어렵고 반복적인 다차원 최적화(multi-parameter optimization) 작업으로, 하나의 특성을 개선하면 다른 특성이 악화되는 트레이드오프가 빈번히 발생함.


### 2.5 Preclinical Development (전임상 개발)

- IND(신약 임상시험계획) 신청을 위한 전임상 시험(IND-enabling studies) 단계로, 약리(pharmacology), 약동학/ADME, 독성(toxicology) 평가로 구성됨.
- 용량범위결정시험(Dose Range Finding)을 통해 적정 용량과 표적장기 독성을 우선 확인한 뒤, GLP(Good Laboratory Practice) 기준을 준수하는 반복투여 독성시험 등 규제기관 제출용 안전성 시험을 진행.
- in vitro 실험과 동물을 이용한 in vivo 시험을 병행하여, 사람 대상 최초 투여(First-in-Human) 전 안전성 근거를 확보하는 것이 목표.


### 2.6 Clinical Development (임상시험)

- **Phase 1**: 소규모 건강인/환자를 대상으로 안전성, 최대내약용량, 초기 약동학을 확인.
- **Phase 2**: 최대 약 100여 명 규모의 환자군을 대상으로 유효성 및 적정 용량을 탐색.
- **Phase 3**: 수백~수천 명 규모의 다기관 시험으로 유효성을 확증하고 이상반응을 모니터링하여 품목허가(NDA 등) 신청 자료를 확보.
- **Phase 4**: 허가 이후 실시하는 시판 후 조사(post-marketing surveillance)로, 장기 투여 시 안전성과 드문 이상반응을 추적.

----------------------------------------------------------------------

## 3. Data

신약 개발 파이프라인의 각 단계에서는 성격이 서로 다른 데이터가 생성·활용된다. 에이전트가 어떤 데이터 유형을 다룰 수 있어야 하는지 이해하기 위해, 주요 데이터 종류를 아래와 같이 정리한다.

### 3.1 Omics (오믹스)

유전체학(Genomics), 전사체학(Transcriptomics, RNA-seq), 단백질체학(Proteomics) 등 생물학적 정보. 주로 Target Identification/Validation 단계에서 질병과 타겟 간의 관계를 규명하는 데 사용된다.

### 3.2 Image (이미지 데이터)

Phenotypic screening 및 독성/기전 연구에서는 세포·조직 이미지 데이터가 핵심적으로 활용된다. 대표적으로 **Cell Painting**은 6종의 형광 염색 시약으로 세포 내 8개 구성요소(핵, 소포체, 인, 세포질 RNA, 액틴, 골지체, 세포막, 미토콘드리아)를 염색하고 5개 채널로 고배율 촬영하는 high-content imaging 기법이다. 특정 바이오마커에 국한되지 않고 편향 없는 고차원 형태학적(morphological) 정보를 대량으로 확보할 수 있어, 딥러닝 기반 화합물 활성·독성 예측, 작용기전(MoA) 추론, 약물 재창출(drug repurposing) 등에 폭넓게 활용된다.

### 3.3 Assay Readouts (활성평가 결과 데이터)

HTS, Target-based/Phenotypic screening, FBDD 등에서 생성되는 정량적 활성 데이터. 대표적으로 화합물 농도에 따른 억제율/활성률을 측정한 **용량-반응 곡선(dose-response curve)**을 시그모이드 형태로 피팅하여 **IC50**(50% 저해 농도) 또는 **EC50**(50% 활성 농도) 값을 산출한다. 이 값들이 화합물의 역가(potency)를 나타내는 핵심 지표로 사용되며, 대조군 대비 %활성/%저해로 정규화한 well 단위 raw data와 이를 요약한 IC50/EC50/Emax 등 파라미터 데이터가 함께 축적된다.

### 3.4 Pharmacokinetic studies (약동학 데이터)

전임상·임상 단계에서 동물 또는 사람에게 약물을 투여한 뒤 시간에 따른 혈중 농도를 측정한 **농도-시간 프로파일** 데이터. 구획모델을 가정하지 않는 **비구획분석(NCA, Non-Compartmental Analysis)**을 통해 다음과 같은 핵심 파라미터를 산출한다.

- **Cmax**: 투여 후 관찰된 최고 혈중 농도.
- **Tmax**: 최고 농도에 도달하는 시간.
- **AUC**: 농도-시간 곡선 아래 면적(전체 약물 노출량의 척도).
- **반감기(half-life)**: 혈중 농도가 절반으로 감소하는 데 걸리는 시간(제거 속도 계산에 활용).

### 3.5 Clinical outcomes (임상 결과 데이터)

임상시험 단계 및 시판 후 조사(Phase 4)에서 수집되는 유효성·안전성 결과 데이터. 1차/2차 평가변수(endpoint), 이상반응(adverse event) 발생률과 같은 임상시험 데이터 외에도, 전자의무기록(EHR)이나 청구 데이터 기반의 **실제임상데이터(RWD)/실사용증거(RWE)**가 점차 보완적으로 활용되고 있다. RWD/RWE는 임상시험만으로는 검출이 어려운 드문 이상반응 탐지(pharmacovigilance), 대상군 선정, 시판 후 장기 안전성 모니터링 등에 활용된다.

## 4. 활용 가능한 화합물/활성 데이터베이스

Hit Identification 및 이후 단계에서는 아래와 같은 공개 데이터베이스가 핵심 자원으로 활용된다.

- **ChEMBL**: 생물학적 활성(bioactivity) 데이터가 수작업으로 큐레이션된 데이터베이스. 화학·생물활성·유전체 정보를 연결하여 신약 개발에 활용.
- **PubChem**: NIH가 운영하는 공개 화학 데이터베이스로 화학 구조, 물성, 생물학적 활성, 특허, 독성 정보 등을 포함. HTS 데이터 확인, 독성 예측, 약물 재창출(drug repurposing)에 유용.
- **ZINC**: 구매 가능한 화합물을 3D 형태로 제공하는 무료 데이터베이스(수억 개 규모). 약물유사성 기준으로 사전 필터링되어 있어 virtual screening 및 hit identification에 적합.

---

## 5. Case Studies

### Table S1. Case Studies 요약

| Case Studies | 도메인 | 에이전트 설계 | 통합된 핵심 도구 | 주요 성과 |
|---|---|---|---|---|
| 분자 우선순위 결정을 위한 종합 문헌 분석 | 초기 발굴(Early discovery) | Supervisor | MCP + RAG + ADMET 예측 모델 + dual-memory(단기·장기) | - 검토 시간을 수 주에서 수 시간으로 단축<br>- 출처 추적이 가능한(citation-traceable) SAR/ADMET 종합 보고서를 생성하고 상충되는 데이터에는 충돌 플래그를 표시 |
| In Silico 독성 예측 | 내분비교란 위험성 평가 | ReAct | 독성예측 모델 + 케모인포매틱스 툴킷 + 문헌·규제문서 검색 | - Cashmeran 대사산물 전반에서 예측된 내분비교란 위험도가 감소했으며, 이는 문헌 결과와 일치해 낮은 내분비 위험 프로파일을 뒷받침 |
| 프로토콜 설계 및 실행 자동화 | 실험 설계(Experiment Planning) | Multi-agent | RAG + 비교 평가 도구 + MIQE 기준에 부합하는 qPCR 프로토콜 생성기 + 자동화 스크립트 생성기 + 구조화 보고서 생성기 | - 자동화 실행이 가능한 AAV qPCR 워크플로우를 2시간 이내에 완성, 수작업 대비 400배 이상의 사이클타임 단축 달성 |
| Virtual Scientists를 활용한 신약 개발 가속화 | 전임상 신약 발굴 | Swarm | API 기반 검색 도구 + 바이오인포매틱스 파이프라인 + 예측/생성 모델 | - 데이터셋 규모에 따라 다르지만, 특발성 폐섬유증(IPF) 전임상 워크플로우 전체를 2시간 이내에 실행(기존 방식은 수 주 소요) |
| 희귀질환 대상 약물 재창출 | 약물 재창출(Drug repurposing) | Supervisor | MCP 서버: Ensembl, OpenTargets, Reactome, KEGG, AlphaFold, PDB, ChEMBL, PubChem | - 자동화되고 병렬화된 파이프라인을 통해 척수성근위축증(SMA) 재창출 후보물질 shortlist를 수 시간 내 도출(기존 방식은 수 주 소요) |
| 소분자 합성 자동화 | 분자 합성 | Supervisor | 역합성(retrosynthesis) 엔진 + 내부 데이터베이스 + 로봇팔 + LC/MS 시스템 | - 7가지 서로 다른 반응을 커버하는 자동화 합성 시설을 구축, 하루 수십 개 화합물의 처리량 달성 |
| Focal graph를 활용한 신약 개발 가설 생성 | 타겟 발굴 | ReAct | 지식그래프(KG) 추출 및 검색 + 네트워크 분석 | - Focal graph 기반 LLM이 RNA-seq perturbation 프로파일의 phenocopier 분석을 통해 eIF2 복합체를 포함한 잠재적 신규 Wnt 경로 종양 타겟을 다수 발굴 |
| Discovery-to-Deal 의사결정 | 바이오파마 자산 발굴 | Supervisor | MCP + PKG(Pharma Knowledge Graph) + Hybrid RAG + ML 모델 + 물리 기반 모델(도킹, MD) | - PKG 기반 후보 shortlist와 구매자 맞춤형 아웃리치 계획을 수 시간 내, 수작업 컨설팅 대비 더 높은 재현율(recall)과 속도로, 훨씬 낮은 비용에 제공 |

### 5.1 문헌 분석 (Misogi Labs) 
- Supervisor 구조. 
- 특허·문헌·교차검증 에이전트가 협업해 신규 분자 후보의 SAR/ADMET 프로파일을 인용 추적 가능한 형태로 정리, dual-memory로 프로젝트 간 화합물 시리즈를 재인식.

### 5.2 In Silico 독성 예측 (Human Chemical Co.) 
- ReAct 구조. 
- Cashmeran의 대사산물을 BioTransformer로 예측하며 내분비교란 위험도를 단계적으로 재평가, 문헌 근거와 대조.

### 5.3 qPCR 프로토콜 자동화 (Potato.ai, Tater) 
- Multi-agent 구조. 
- AAV qPCR assay 설계를 4개월에서 2시간 이내로 단축.

### 5.4 Virtual Scientists를 통한 신약 개발 가속 (Kiin Bio)
- Swarm 구조. 
- 100개 이상의 데이터·도구·AI 모델(API, 대규모 오믹스 파이프라인, GPU 모델)을 통합한 인프라형 플랫폼으로, 문헌·데이터 탐색 담당, 오믹스/GWAS 분석 담당, 분자설계·가상스크리닝·단백질 접힘/도킹 담당 등 역할이 나뉜 전문 에이전트들이 공유 조직 메모리를 통해 협업합니다. 
- 특발성 폐섬유증(IPF) 전임상 프로그램 사례에서 시장기회 파악→타겟 우선순위화→소분자 히트 생성·랭킹까지 비선형 워크플로우를 오케스트레이션했고, 보통 2~3주 걸리는 작업을 데이터셋 크기에 따라 2시간 이내로 단축했습니다. 
- 다만 이질적인 오믹스·구조 데이터의 정규화/어노테이션 표준 불일치는 여전히 과제로 남는다고 밝혔습니다.

### 5.5 희귀질환 약물 재창출 (Augmented Nature)
- Supervisor 구조. 
- Disease/Pathway/Protein/Compound/Safety 5개 서브 에이전트를 감독자가 조율합니다. 
- "척수성근위축증(SMA) 재창출 기회를 찾아라"는 질의에 대해, disease agent가 Ensembl·OpenTargets에서 SMN1/SMN2 등 관련 유전자를 찾고, pathway agent가 Reactome·KEGG로 생물학적 기전을 매핑하고, protein agent가 AlphaFold·PDB에서 구조 정보를, compound agent가 ChEMBL·PubChem에서 해당 단백질을 타겟하는 기존 화합물을 검색한 뒤, safety agent가 ADMET 프로파일로 필터링합니다. 
- 결과적으로 재창출 가능 후보 shortlist를 수 주 대신 수 시간 만에 생성했고, 이미 승인되었거나 임상 중인 약물 위주로 도출되어 규제·비용 장벽이 낮다는 실무적 이점도 언급합니다.

### 5.6 소분자 합성 자동화 (onepot.ai)
- Supervisor 구조. 
- 소분자 합성은 흔히 개발의 병목으로, 합성 경로를 못 찾은 화합물이 태반이고(약물유사 화합물 10^60개 vs DB에 등재된 것은 수억 개), 반응 실패 시 복구 전략도 필요합니다. 
- onepot.ai는 튜브 피커·디캐퍼·리퀴드 핸들러·플레이트 실러·LC/MS로 구성된 하드웨어와, 역합성 엔진·웹검색·코드실행·문헌검색을 갖춘 "AI 유기화학자"를 결합해 프로토콜을 스스로 수정하며 실험을 반복하는 폐루프를 구현했습니다. 
- 실제 상업 운영 결과 7개 반응 유형(반응당 2~5개 프로토콜)을 커버하며 반응별 성공률 50~88%, 하루 수십 개 화합물 처리량을 달성했습니다.

### 5.7 Focal graph 기반 검색 (Plex Research)
- ReAct 구조. 
- 대규모 생의학 데이터셋은 복잡·희소·비정형이라 전체 지식그래프를 직접 분석하기엔 계산비용이 크고 시각화도 어렵습니다. Focal graph는 특정 질의와 관련된 부분그래프만 추출해 핵심 개체를 드러내는 방식입니다. 
- "Wnt 경로에서 신규 종양 타겟을 찾아라"는 프롬프트에 대해, 에이전트가 Wnt 경로의 알려진 구성원을 나열하고 이들이 교란된 RNA-seq 프로파일을 찾은 뒤, focal graph 검색으로 "비슷한 유전자 발현 프로파일을 만들어내는, 아직 알려지지 않은 유전자(phenocopier)"를 탐색해 eIF2 복합체 등 잠재적 신규 종양 타겟 후보를 다수 도출했습니다.

### 5.8 Discovery-to-Deal 의사결정 (Convexia Bio)
- Supervisor 구조. 
- 바이오파마 자산 발굴은 데이터가 다국어·비정형으로 흩어져 있어 수작업 프로세스가 병목입니다. Asset Discovery(질의별 지식그래프 구축)→Scientific Evaluation(도킹·MD 등 물리기반 모델+ML로 기술적 타당성 평가)→Market Analysis(시장·규제·IP 시나리오)→Clinical Assessment(과거 임상 데이터 기반 리스크 스코어링)→Business Development(딜 패턴 기반 최적 경로 계산)의 5개 모듈이 피드백 루프로 연결됩니다. 
- 중견 제약사가 포트폴리오 트리아지를 의뢰한 사례에서, 학회 발표·논문·대학 자료·공시자료 등을 수집해 Property Knowledge Graph(PKG)를 구축하고, 과학적/임상적 모델로 효과크기·운영리스크를 정량화한 뒤, buyer graph와 대조해 구매자 맞춤 아웃리치 계획까지 수 시간·저비용에 산출했으며, 비정형 데이터 커버리지 덕분에 수작업 컨설팅보다 재현율(recall)과 속도 모두 앞섰다고 보고합니다.

### 요약

초기 발굴·재창출·자산평가처럼 "여러 전문 서브에이전트를 감독자가 조율"하는 작업엔 Supervisor가, 단일 루프의 반복 탐색(독성 대사경로 추적, focal graph 가설 탐색)엔 ReAct가, IPF처럼 생물·화학·임상이 뒤섞인 비선형 워크플로우엔 Swarm이 쓰였습니다. 모든 사례가 공통적으로 "수 주~수 개월 → 수 시간" 수준의 압축을 보고하는 점도 눈에 띕니다.