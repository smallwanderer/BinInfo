# 신약 개발 Agent - EDA 분석 및 가설 생성

## 1. 신약 개발이 가장 활발한 지점

![image.png](image.png)

> [https://www.visualcapitalist.com/sp/ranked-which-areas-receive-the-most-pharma-rd/](https://www.visualcapitalist.com/sp/ranked-which-areas-receive-the-most-pharma-rd/)
> 

| 영역 | Area | 숫자 | 비율 |
| --- | --- | --- | --- |
| 종양 | Oncology | 	9,476 | 	24.95% |
| 신경계 | Neurology | 	3,868 | 	10.18% |
| 대사 질환 | Metabolic | 	3,314 | 	8.73% |
| 감염 질환 | Infectious Disease | 	2,879 | 	7.58% |
| 근 골격계 | Musculoskeletal | 	2,157 | 	5.68% |
| 면역학 | Immunology | 	1,469 | 	3.87% |
| 피부과 | Dermatology | 	1,327 | 	3.49% |
| 감각기관 | Sensory | 	1,312 | 	3.45% |
| 심혈관계 | Cardiology | 	1,207 | 	3.18% |
| 호흡기계 | Respiratory | 	1,172 | 	3.09% |
| 비뇨생식기계 | Genitourinary | 	885 | 	2.33% |
| 혈액학 | Hematology | 	811 | 	2.14% |
| 호르몬 | Hormonal | 	273 | 	0.72% |
| 기생충 | Parasitology | 	109 | 	0.29% |
| 희귀질환 | Rare diseases | 	7,721 | 	20.33% |
| 합계 | Total | **37,980** | **100%** |

## 각 영역 별 EDA Agent 조사

![image.png](image%201.png)

### 1. 종양학 (Oncology)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| RegNetAgents (2026.07) | 암 네트워크 조절유전자 후보 식별 | [https://en.cryptonomist.ch/2026/07/18/cancer-genomics-ai-regnetagents/](https://en.cryptonomist.ch/2026/07/18/cancer-genomics-ai-regnetagents/) | TCGA | [https://portal.gdc.cancer.gov/](https://portal.gdc.cancer.gov/) |
|  |  |  | GREmLN(단일세포) | 특정 링크 미확인 |
| 대장암 우선순위화 (bioRxiv) | LLM 가설생성→실험검증 | [https://www.biorxiv.org/content/10.64898/2026.07.05.736565v2.full.pdf](https://www.biorxiv.org/content/10.64898/2026.07.05.736565v2.full.pdf) | DepMap(CCLE) | [https://depmap.org/portal/](https://depmap.org/portal/) |
|  |  |  | GEO GSE39582 | [https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE39582](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE39582) |
| OriGene | 가상 질병생물학자 | arXiv:2503.24047 내 인용 | 멀티오믹스+KG | 특정 링크 미확인 |
| CancerGPT | 희귀조직 약물병용 예측 | cell.com/iscience 내 인용 | 고처리량 in vitro | 특정 링크 미확인 |
| AI co-scientist | 백혈병 재창출 후보 | arXiv:2508.16613 내 인용 | 문헌+멀티오믹스 | 특정 링크 미확인 |
| Lantern | 희귀암 전용 | [https://intuitionlabs.ai/articles/multi-agent-ai-rare-cancer-drug-discovery](https://intuitionlabs.ai/articles/multi-agent-ai-rare-cancer-drug-discovery) | 니치 저널·케이스리포트 | 특정 링크 미확인 |

### 2. 신경계 (Neurology)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| ADAgent | AD 다중모달 진단·예후 | [https://doi.org/10.1007/978-3-032-06004-4_3](https://doi.org/10.1007/978-3-032-06004-4_3) | 영상+임상+유전 | 특정 링크 미확인 |
| Coated-LLM | AD 약물병용 가설생성 | [https://github.com/QidiXu96/Coated-LLM](https://github.com/QidiXu96/Coated-LLM) | AlzPED | [**https://alzped.nia.nih.gov/**](https://alzped.nia.nih.gov/) |
|  |  |  | CTDbase | [**https://ctdbase.org/**](https://ctdbase.org/) |
| ADAM-1 | 임상+미생물+문헌 RAG | [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12727125/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12727125/) | 요양시설 코호트(자체수집) | 공개 링크 없음(자체 데이터) |
| AgenticAD | AD 관리 통합 | [https://arxiv.org/pdf/2510.08578](https://arxiv.org/pdf/2510.08578) | CARE-AD·LITERAS 통합 | 특정 링크 미확인 |
| CARE-AD | 장기 임상노트 AD 예측 | NPJ Digital Medicine 8(1):541 | 장기추적 임상노트(자체수집) | 공개 링크 없음 |

### 3. 대사질환 (Metabolic)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| MADRIGAL | 당뇨·MASH 다약제 관리 | [https://zitniklab.hms.harvard.edu/projects/Madrigal/](https://zitniklab.hms.harvard.edu/projects/Madrigal/) | 전임상 다중오믹스+약물반응 | 특정 링크 미확인 |

### 4. 감염질환 (Infectious Disease)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| AI co-scientist (항생제내성) | 세균 진화·내성 가설 | arXiv:2603.28924 내 인용 | 세균 유전체+표현형 | 특정 링크 미확인 |

### 5. 감각기관 (Sensory)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| Robin | dAMD 신약후보 발굴 | [https://arxiv.org/abs/2503.24047](https://arxiv.org/abs/2503.24047) | 표현형 스크리닝 | 특정 링크 미확인 |

### 6. 희귀질환 (Rare Diseases)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| DeepRare | 희귀질환 진단, MCP 구조 | [https://arxiv.org/html/2506.20430v2](https://arxiv.org/html/2506.20430v2) | HPO(표준용어) | [https://hpo.jax.org/](https://hpo.jax.org/) |
|  |  |  | VCF 유전자검사 | (표준 파일형식, DB 아님) |
| RaDaR | 320억 파라미터 진단 LLM | [https://arxiv.org/pdf/2606.24510](https://arxiv.org/pdf/2606.24510) | 자유텍스트+합성데이터+EHR | 자체 구축, 공개 링크 없음 |
| Augmented Nature | 희귀질환 재창출 | Seal et al. 2026 논문 내 | (논문 내 명시) | — |

### 7. 피부과 (Dermatology)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| SkinGPT-X | 피부질환 진단 멀티에이전트 | [https://arxiv.org/pdf/2603.26122](https://arxiv.org/pdf/2603.26122) | 피부경 이미지+임상텍스트+오믹스 | 특정 링크 미확인 |

### 8. 심혈관계 (Cardiology)

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| (명칭 미확인) | 심근병증 유전자 식별 | [https://www.sciencedirect.com/science/article/pii/S2666389925001941](https://www.sciencedirect.com/science/article/pii/S2666389925001941) | 전사체+iPSC 마이크로조직 | 특정 링크 미확인 |

### 9. 범용

| Agent | 설명 | Agent 링크 | 데이터셋 | 데이터셋 링크 |
| --- | --- | --- | --- | --- |
| DrugAgent | 약물-타겟 예측 KG | arXiv:2503.24047 내 인용 | DrugBank | [https://go.drugbank.com/](https://go.drugbank.com/) |
| PharmaSwarm | 통합 스웜 | [https://arxiv.org/pdf/2504.17967](https://arxiv.org/pdf/2504.17967) | 멀티소스 통합 | 특정 링크 미확인 |
| BioScientist Agent | RTX-KG2 기반 재창출 | arXiv:2503.24047 내 인용 | RTX-KG2 | 특정 링크 미확인 |

## 3. 질병 특화 EDA Agent 조사 내역 기반 논의 사항

1. 이미 대부분 유명한 병에는 특화된 EDA Agent가 존재해서 경쟁력이 없지 않나
2. 그래서 찾아본 Agent 종류 중 신약 개발 횟수는 많은데 실제 Agent의 개발은 잘 안되는 타겟을 정하는 것이 좋아보임
3. 혹은? 아예 다른 쪽으로 

→ 그래서 근골격계 쪽으로 타겟을 한번 잡아봄

|  | Age | BMI | Race | Smoking | Osteoporosis(baseline) | KOA(follow-up) |
| --- | --- | --- | --- | --- | --- | --- |
| 예시1 | 62 | 27.4 | 1 | 0 | 0 | 1 |
| 예시2 | 58 | 31.2 |  | 1 | 1 | 0 |

이거 골 관절염쪽 데이터인데 이게 대부분 데이터가 범주형이고 좀 너무 잘 알려진 데이터기는 한데

NAC, UBX0101, Anakinra, Lorecevivint, Sprifermin

여기 논문 보면 지금 골관절염쪽 치료제쪽 임상이 좀 활발하긴 한데 계속 실패하고 있고 근데 연구는 아직도 투자를 많이 하고 있어서 이쪽으로 가보는거 나쁘지 않다고 생각함

| 데이터 | 규모 | 링크 |
| --- | --- | --- |
| OAI | 4,796명 종단 코호트 | [https://nda.nih.gov/oai/](https://nda.nih.gov/oai/) |
| GWAS Catalog | ~100개 OA 위험 유전자좌 | [https://www.ebi.ac.uk/gwas/](https://www.ebi.ac.uk/gwas/) |
| GEO(GSE236924/82107/169454) | Bulk+단일세포 발현데이터 | 각 accession 페이지 |
| T2 relaxation time | 연골 조기손상 정량 바이오마커(ms 단위, 연속형) | OAI 내 MRI 서브데이터 |

사용할 수 있는 데이터는 이정도?