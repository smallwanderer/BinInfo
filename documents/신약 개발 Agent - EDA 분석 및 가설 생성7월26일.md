# 신약 개발 Agent - EDA 분석 및 가설 생성

## 1. 신약 개발이 가장 활발한 지점

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

![image.png](image.png)

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
3. 혹은? 아예 다른 쪽으로 (바이오 마커나, 분자구조 EDA나..)

→ 그래서 근골격계 쪽으로 타겟을 한번 잡아봄

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

## 4. 바이오 마커 쪽

[https://data.biomarkerkb.org/](https://data.biomarkerkb.org/)

```jsx
                    "access_time": "2024-06-06T04:00:00.000Z"
                }
            }
        ],
        "script_driver": "R Script",
        "software_prerequisites": [
            {
                "name": "R",
                "version": "4.2.0",
                "uri": {
                    "uri": "https://www.r-project.org/",
                    "access_time": "2024-06-06T04:00:00.000Z"
                }
            }
        ],
        "external_data_endpoints": [
            {
                "name": " rusp_metaboliteBM_v1.0.xlsx",
                "url": " https://github.com/metabolomicsworkbench/MW-biomarker/blob/main/rusp_metaboliteBM_v1.0.xlsx"
            }
        ],
        "environment_variables": {
            "ENVIRONMENT": "R"
        }
    },
    "io_domain": {
        "input_subdomain": [
            {
                "uri": {
                    "filename": "rusp-august-2023.pdf",
                    "uri": "https://www.hrsa.gov/sites/default/files/hrsa/advisory-committees/heritable-disorders/rusp/rusp-august-2023.pdf",
                    "access_time": "2024-05-13T14:01:02.000Z"
                }
            }
        ],
        "output_subdomain": [
            {
                "mediatype": "tsv",
                "uri": {
                    "filename": "biomarkers_mw_newborn_screening.tsv",
                    "uri": "/data/shared/biomarkerdb/downloads/mw_newborn_screening/current/mw_newborn_screening.tsv",
                    "access_time": "2024-05-14T04:00:00.000Z"
                }
            }
        ]
    },
    "error_domain": {
        "empirical_error": {
            "empirical_error": "null"
        },
        "algorithmic_error": {
            "algorithmic_error": "null"
        }
    }
}
```

저 사이트 내에 이미 이런식으로 특징적 biomarker에 대한 EDA 분석 결과가 있는데 biomarker 쪽으로 EDA 분석 틀을 잡고 진행하는건 좀 무리가 있지 않을까

차라리 질병 특정 타겟 → 데이터를 잡고 → 데이터 컬럼에 대한 설명을 논문으로 뽑아오는 RAG + EDA 분석 틀로 가는 것이 더 좋아보임

이미 데이터베이스가 있는데 굳이 이걸 할 필요는 없어보인다. 까지가 제 생각입니다.

## 5. 최종 생각

그래서 제 최종 생각은 특정 질병 도메인 딱 잡고 하는건데 

근 골격계 쪽이 지금 연구는 되게 활발한데, 계속 임상이 실패하고 있단 말이지

그 중에서 골관절염 쪽에 임상 실패하면서도 투자는 계속 하고 있는데 개발된 AI Agent는 거의 전무하니, 확실한 어필은 될 것 같다라는게 생각이라

이 분야에 한정해서 EDA쪽을 해보는 게 좀 어떻나 

[https://www.dailypharm.com/user/news/340628](https://www.dailypharm.com/user/news/340628)

[https://www.monews.co.kr/news/articleView.html?idxno=412827](https://www.monews.co.kr/news/articleView.html?idxno=412827)

이거 뉴스기사만 보더라도 효과 완화제만 있고 치료제는 안나오는 실정인데 투자는 계속 하고 

[https://kbthink.com/securities-view.html?docId=20250829101152347K](https://kbthink.com/securities-view.html?docId=20250829101152347K)

![image.png](image%201.png)

이런거 보면 이걸로 EDA를 토대로 연구 병목을 줄여줄 수 있다 이런식으로 가면 되게 괜찮을 것 같단말이지

그래서 실제 EDA Agent들 중 하나 효과를 가져오면

## AutoBA (Automated Bioinformatics Analysis)

- 데이터 경로·설명·목표 입력
- 분석 계획 수립 → 코드 생성 → 실행
- 계획 수립 성공률 90% (40건 중 36건), 코드 생성 성공률 87.5%, 완전 자동화 종단 분석 성공률 87.5%
- 컬럼 40개 기준 3~18분 정도 소요

→ 우리 같은 경우는 컬럼 설명 / 분석 계획 수립 / EDA 분석 코드 생성 / 실행

뭐 이정도 순으로 가면 되지 않을까

![image.png](image%202.png)

이게 데이터 예시고 여기 안에 R로 이미 EDA코드가 있어서 Few-Shot 쓰기도 좋은듯

[https://nda.nih.gov/general-query.html?q=query=data-structure ~and~ dataSources=Osteoarthritis Initiative ~and~ orderBy=shortName ~and~ orderDirection=Ascending](https://nda.nih.gov/general-query.html?q=query=data-structure%20~and~%20dataSources=Osteoarthritis%20Initiative%20~and~%20orderBy=shortName%20~and~%20orderDirection=Ascending)

OAI 데이터 구조

### 1. 인구통계·기초정보 (Demographics)

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_enrollee01 | 등록자 인구통계 | 4,796 (전체) |

### 2. 병력·생활습관·약물 (Med History)

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_oarisk01 | 개인 병력, 체중 이력, 가족력, 생활습관·위험요인 | 4,796 |
| oai_meduse01 | 복용 약물 인벤토리 | 4,536 |
| oai_nutrition01 | 영양 섭취 | 4,796 |

### 3. 통증·삶의 질 (Pain / Quality of Life)

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_oapain01 | 통증 병력, 간헐적·지속적 OA 통증(ICOAP), 치료·약물 | 4,796 |
| oai_koos_womac01 | KOOS/WOMAC — 무릎손상·OA 결과지수 | 5,295 |
| oai_cope01 | 대처전략 설문(Coping Strategies) | 4,141 |
| oai_charlson01 | Charlson 동반질환지수 | 4,786 |
| oai_ces_d01 | 우울척도(CES-D) | 4,792 |
| oai_sf1201 | 의료결과조사(SF-12) | 4,796 |
| oai_lld01 | 노년기 장애(Late Life Disability) | 4,143 |

### 4. 신체활동·기능 (Activity / Physical Function)

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_pase01 | 노인 신체활동척도(PASE) | 4,796 |
| oai_physfunct01 | 신체기능 (의자 일어서기, 보행, 등척성 근력) | 4,796 |
| oai_gfadl01 | 일상생활 전반 기능(GFADL) | 4,074 |
| oai_exercise01 | 운동(과거 신체활동력) | 2,655 |
| oai_accelday01 | 보행 가속도계 — 일별 | 2,024 |
| oai_accelmin01 | 보행 가속도계 — 분별 | 2,017 |
| oai_accelsummary01 | 보행 가속도계 요약 | 1,978 |

### 5. X-Ray 영상·평가

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_kxrsemiquant01 | 무릎 X-ray 반정량 점수 **(KL grade 포함)** | 4,508 |
| oai_hxrsemiquant01 | 고관절 X-ray 반정량 점수 | 4,762 |
| oai_kxrquantjsw01 | 무릎 X-ray 관절강 폭(JSW) 측정 | 3,469 |
| oai_xralign01 | 무릎·전체하지 X-ray 정렬 | 4,291 |
| oai_kxrquant_ftb01 | 무릎 X-ray 해면골 프랙탈 측정 | 598 |
| oai_xrmeta01 | X-ray 메타데이터 | 4,796 |

### 6. MRI 영상·평가

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_kmriquant01 | 무릎 MRI 정량 측정 (반월판·연골·뼈) | 1,816 |
| **oai_kmriquant_t201** | **무릎 MRI 정량 연골 측정 — T2 매핑** | **300** |
| oai_kmrisemiquant01 | 무릎 MRI 반정량 스코어링 | 2,763 |
| oai_kmrisemiquantbml01 | 무릎 MRI 반정량 점수 — 골수병변(BML) | 112 |
| oai_mrimeta01 | MRI 메타데이터 | 4,796 |
| oai_bone01 | 해면골(trabecular bone) 측정 (MRI, DEXA, Lab) | 629 |
| oai_sage01 | 피부 자가형광(Skin Auto-fluorescence) 측정 | 746 |

### 7. 검사·결과 (Lab / Outcomes)

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_labcollection01 | 검사 시료 수집 | 4,796 |
| oai_biomarker01 | 생화학적 바이오마커 | 729 |
| oai_outcome01 | 결과 (사망, 무릎·고관절 치환술) | 4,796 |

### 8. 요약·기타

| Short Name | 한글 설명 | 공유 대상자 수 |
| --- | --- | --- |
| oai_inventory01 | 영상 인벤토리 (MRI/X-ray 요약) | 4,796 |
| image03 | 원본 이미지 데이터 (DTI, MRI, fMRI) — AMP SCZ/NDA/OAI 공용 구조 | 69,116 (여러 연구 통합치) |

검사의 무릎 X-ray 관절강 폭(JSW) 측정 / 무릎 MRI 반정량 점수 — 골수병변(BML) 이런 점수같은 것들도 EDA하기 좋아보이기는 해서


## 6. 추가 논의 사항
분자구조 관련: 얘도 저기 특정 질병처럼 하나의 질병 영역을 타게팅하고 가져온 후에 이미 5번에서 정한거랑 이어 붙이는 방식이 더 좋을 것 같음
https://www.ebi.ac.uk/chembl/explore/targets/ 

만약에 SMILES 분자구조 데이터를 쓸거면 어떤 방식으로 쓸건지는 이야기를 해봐야 할 거 같음

<img width="1340" height="663" alt="image" src="https://github.com/user-attachments/assets/5a0e23eb-e6dc-4fb4-aadf-ab322831a134" />

데이터는 찾을때 target -> 그러니까 DYRK1A 뭐 이런식으로 특정 담백질 계열을 검색하면, 이 타겟을 없애거나 증진시키는 실험이 보고된 화합물들의 분자구조랑 뭐 실험 단계들의 형태가 나옴


## 7. OAI 데이터 관련 사항

## 공통 사항 (모든 데이터셋에 반복 등장하는 컬럼)

| 컬럼명 | 설명 | 데이터 타입 |
|---|---|---|
| `collection_id`, `dataset_id`, `oai_xxx01_id` | NDA 내부 관리용 ID | ID(수치) — 분석에는 불필요 |
| `subjectkey` | 연구대상자 전역 고유식별자 (예: NDAR_INVV5HVXTKF) | **GUID — 여러 데이터셋을 조인할 때 이 컬럼 기준** |
| `src_subject_id` | 원 연구실 기준 피험자 번호 (예: 9000099) | ID(수치) — OAI 원본 ID와 매칭할 때 사용 |
| `interview_date`, `interview_age`, `ageyears`, `sex` | 방문 시점 날짜/나이/성별 | 날짜/수치/범주형 |
| `visit` | 방문 시점 코드 (V00=baseline, V01=12개월... 등) | 범주형 |
| `collection_title` | 항상 "Osteoarthritis Initiative" 고정값 | |
---

-> 데이터 1차 정리: 각 환자(싦험군)의 방문마다 먹거나 시도중인 약물에 대해 병과, 및 각 환자의 설문을 기록해둔 데이터셋 (환자 설명, 환자 설문, XRAY(Imgage, X-ray 반정량 점수 (KL grade)) 

## OAI 등록자 인구통계 (Enrollees Demographics) (`oai_enrollee01`, 총 17개 컬럼)

| 컬럼명 | 설명(한글) | 데이터 타입 | 예시값 |
|---|---|---|---|
| `collection_id` | collection_id | ID(수치) | 2343 |
| `oai_enrollee01_id` | oai_enrollee01_id | ID(수치) | 1 |
| `dataset_id` | dataset_id | ID(수치) | 47605 |
| `subjectkey` | 연구대상자 전역 고유식별자(GUID) | GUID | NDAR_INVV5HVXTKF |
| `src_subject_id` | 연구실/프로젝트 내부 피험자 ID | ID(수치) | 9000099 |
| `interview_date` | 면담/검사/영상촬영 등이 완료된 날짜 | 날짜(문자열, MM/DD/YYYY) | 07/08/2005 |
| `interview_age` | 면담/검사 시점의 나이(개월) | 수치(연속형) | 708 |
| `sex` | 출생 시 성별 | 범주형/문자열 | M |
| `ageyears` | 나이(년) | 수치(연속형) | 59 |
| `e_cohort` | 하위코호트 배정 | 수치(정수) | 1 |
| `visit` | 방문시점 명칭 | 범주형/문자열 | V00 |
| `version` | 평가 버전/코드 | 범주형/문자열 | 25 |
| `ethnicity` | 참가자 민족(히스패닉 여부) | 범주형/문자열 | Not Hispanic or Latino |
| `race` | 연구대상자 인종 | 범주형/문자열 | White |
| `site` | 수행기관(사이트) | 범주형/문자열 | B |
| `interim_visit` | 중간(6개월) 방문 여부 지표 | 수치(정수) | 2 |
| `collection_title` | collection_title | 범주형/문자열 | Osteoarthritis Initiative |

## OAI KOOS/WOMAC 무릎 통증·기능 설문 (`oai_koos_womac01`, 총 101개 컬럼)

| 컬럼명 | 설명(한글) | 데이터 타입 | 예시값 |
|---|---|---|---|
| `collection_id` | collection_id | ID(수치) | 2343 |
| `oai_koos_womac01_id` | oai_koos_womac01_id | ID(수치) | 5085 |
| `dataset_id` | dataset_id | ID(수치) | 55082 |
| `subjectkey` | 연구대상자 전역 고유식별자(GUID) | GUID | NDAR_INVFZEAN6JV |
| `src_subject_id` | 연구실/프로젝트 내부 피험자 ID | ID(수치) | 9397088 |
| `interview_date` | 면담/검사/영상촬영 등이 완료된 날짜 | 날짜(문자열, MM/DD/YYYY) | 02/23/2004 |
| `interview_age` | 면담/검사 시점의 나이(개월) | 수치(연속형) | 600 |
| `sex` | 출생 시 성별 | 범주형/문자열 | F |
| `ageyears` | 나이(년) | 수치(연속형) | 50 |
| `visit` | 방문시점 명칭 | 범주형/문자열 | V00 |
| `version` | 평가 버전/코드 | 범주형/문자열 | 0.2.3 |
| `sym_rkn1` | 오른쪽 무릎 증상: 부종, 지난 7일간 | 수치(정수) | 1 |
| `sym_rkn2` | 오른쪽 무릎 증상: 무릎 움직일 때 갈리는 느낌/소리, 지난 7일간 | 수치(정수) | 2 |
| `sym_rkn3` | 오른쪽 무릎 증상: 움직일 때 무릎 걸림, 지난 7일간 | 수치(정수) | 1 |
| `sym_rkn4` | 오른쪽 무릎 증상: 무릎 완전히 펴기, 지난 7일간 | 수치(정수) | 0 |
| `sym_rkn5` | 오른쪽 무릎 증상: 무릎 완전히 굽히기, 지난 7일간 | 수치(정수) | 0 |
| `pain_rkfr` | 오른쪽 무릎 통증: 빈도 | 수치(정수) | 3 |
| `pain_rknsp1` | 오른쪽 무릎 통증: 무릎 비틀기/회전, 지난 7일간 | 수치(정수) | 1 |
| `pain_rknsp2` | 오른쪽 무릎 통증: straightening knee fully, 지난 7일간 | 수치(정수) | 0 |
| `pain_rknsp3` | 오른쪽 무릎 통증: bending knee fully, 지난 7일간 | 수치(정수) | 1 |
| `pain_rkn1` | 오른쪽 무릎 통증: 보행, 지난 7일간 | 수치(정수) | 1 |
| `pain_rkn2` | 오른쪽 무릎 통증: 계단, 지난 7일간 | 수치(정수) | 1 |
| `pain_rkn3` | 오른쪽 무릎 통증: 침대에서, 지난 7일간 | 수치(정수) | 0 |
| `pain_rkn4` | 오른쪽 무릎 통증: 앉거나 눕기, 지난 7일간 | 수치(정수) | 0 |
| `pain_rkn5` | 오른쪽 무릎 통증: 서있기, 지난 7일간 | 수치(정수) | 1 |
| `diff_rkn1` | 오른쪽 무릎 어려움: Down 계단, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn2` | 오른쪽 무릎 어려움: Up 계단, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn3` | 오른쪽 무릎 어려움: 앉았다 일어서기, 지난 7일간 | 수치(정수) | 1 |
| `diff_rkn4` | 오른쪽 무릎 어려움: 서있기, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn5` | 오른쪽 무릎 어려움: 굽히기, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn6` | 오른쪽 무릎 어려움: 보행, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn7` | 오른쪽 무릎 어려움: 차 타고내리기, 지난 7일간 | 수치(정수) | 1 |
| `diff_rkn8` | 오른쪽 무릎 어려움: 쇼핑, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn9` | 오른쪽 무릎 어려움: 양말 신기, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn10` | 오른쪽 무릎 어려움: 침대에서 일어나기, 지난 7일간 | 수치(정수) | 1 |
| `diff_rkn11` | 오른쪽 무릎 어려움: 양말 벗기, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn12` | 오른쪽 무릎 어려움: 눕기, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn13` | 오른쪽 무릎 어려움: 욕조 출입, 지난 7일간 | 수치 또는 결측(値 없음) | (결측) |
| `diff_rkn14` | 오른쪽 무릎 어려움: 앉기, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn15` | 오른쪽 무릎 어려움: 화장실 앉고 일어서기, 지난 7일간 | 수치(정수) | 1 |
| `diff_rkn16` | 오른쪽 무릎 어려움: 힘든 집안일, 지난 7일간 | 수치(정수) | 0 |
| `diff_rkn17` | 오른쪽 무릎 어려움: 가벼운 집안일, 지난 7일간 | 수치(정수) | 0 |
| `stiff_rkn1` | 오른쪽 무릎 강직(뻣뻣함): 아침에, 지난 7일간 | 수치(정수) | 1 |
| `stiff_rkn2` | 오른쪽 무릎 강직(뻣뻣함): 낮 동안, 지난 7일간 | 수치(정수) | 1 |
| `sym_lkn1` | 왼쪽 무릎 증상: 부종, 지난 7일간 | 수치(정수) | 1 |
| `sym_lkn2` | 왼쪽 무릎 증상: 무릎 움직일 때 갈리는 느낌/소리, 지난 7일간 | 수치(정수) | 2 |
| `sym_lkn3` | 왼쪽 무릎 증상: 움직일 때 무릎 걸림, 지난 7일간 | 수치(정수) | 2 |
| `sym_lkn4` | 왼쪽 무릎 증상: 무릎 완전히 펴기, 지난 7일간 | 수치(정수) | 0 |
| `sym_lkn5` | 왼쪽 무릎 증상: 무릎 완전히 굽히기, 지난 7일간 | 수치(정수) | 0 |
| `pain_lkfr` | 왼쪽 무릎 통증: 빈도 | 수치(정수) | 3 |
| `pain_lknsp1` | 왼쪽 무릎 통증: 무릎 비틀기/회전, 지난 7일간 | 수치(정수) | 1 |
| `pain_lknsp2` | 왼쪽 무릎 통증: straightening knee fully, 지난 7일간 | 수치(정수) | 0 |
| `pain_lknsp3` | 왼쪽 무릎 통증: bending knee fully, 지난 7일간 | 수치(정수) | 0 |
| `pain_lkn1` | 왼쪽 무릎 통증: 보행, 지난 7일간 | 수치(정수) | 1 |
| `pain_lkn2` | 왼쪽 무릎 통증: 계단, 지난 7일간 | 수치(정수) | 2 |
| `pain_lkn3` | 왼쪽 무릎 통증: 침대에서, 지난 7일간 | 수치(정수) | 0 |
| `pain_lkn4` | 왼쪽 무릎 통증: 앉거나 눕기, 지난 7일간 | 수치(정수) | 0 |
| `pain_lkn5` | 왼쪽 무릎 통증: 서있기, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn1` | 왼쪽 무릎 어려움: Down 계단, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn2` | 왼쪽 무릎 어려움: Up 계단, 지난 7일간 | 수치(정수) | 1 |
| `diff_lkn3` | 왼쪽 무릎 어려움: 앉았다 일어서기, 지난 7일간 | 수치(정수) | 2 |
| `diff_lkn4` | 왼쪽 무릎 어려움: 서있기, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn5` | 왼쪽 무릎 어려움: 굽히기, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn6` | 왼쪽 무릎 어려움: 보행, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn7` | 왼쪽 무릎 어려움: 차 타고내리기, 지난 7일간 | 수치(정수) | 1 |
| `diff_lkn8` | 왼쪽 무릎 어려움: 쇼핑, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn9` | 왼쪽 무릎 어려움: 양말 신기, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn10` | 왼쪽 무릎 어려움: 침대에서 일어나기, 지난 7일간 | 수치(정수) | 1 |
| `diff_lkn11` | 왼쪽 무릎 어려움: 양말 벗기, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn12` | 왼쪽 무릎 어려움: 눕기, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn13` | 왼쪽 무릎 어려움: 욕조 출입, 지난 7일간 | 수치 또는 결측(値 없음) | (결측) |
| `diff_lkn14` | 왼쪽 무릎 어려움: 앉기, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn15` | 왼쪽 무릎 어려움: 화장실 앉고 일어서기, 지난 7일간 | 수치(정수) | 1 |
| `diff_lkn16` | 왼쪽 무릎 어려움: 힘든 집안일, 지난 7일간 | 수치(정수) | 0 |
| `diff_lkn17` | 왼쪽 무릎 어려움: 가벼운 집안일, 지난 7일간 | 수치(정수) | 0 |
| `stiff_lkn1` | 왼쪽 무릎 강직(뻣뻣함): 아침에, 지난 7일간 | 수치(정수) | 1 |
| `stiff_lkn2` | 왼쪽 무릎 강직(뻣뻣함): 낮 동안, 지난 7일간 | 수치(정수) | 2 |
| `qol_kn1` | 삶의 질: 빈도 aware of problems with knee(s) | 수치(정수) | 3 |
| `qol_kn2` | 삶의 질: 무릎 손상 우려로 생활습관 변경 | 수치(정수) | 0 |
| `qol_kn3` | 삶의 질: 무릎에 대한 자신감 부족 정도 | 수치(정수) | 0 |
| `qol_kn4` | 삶의 질: 전반적인 무릎 어려움 정도 | 수치(정수) | 1 |
| `diff_kn1` | 양쪽 무릎 중 하나 difficulty: 쪼그려앉기, 지난 7일간 | 수치 또는 결측(値 없음) | (결측) |
| `diff_kn2` | 양쪽 무릎 중 하나 difficulty: 달리기, 지난 7일간 | 수치(정수) | 0 |
| `diff_kn3` | 양쪽 무릎 중 하나 difficulty: 점프, 지난 7일간 | 수치 또는 결측(値 없음) | (결측) |
| `diff_kn4` | 양쪽 무릎 중 하나 difficulty: 손상된 무릎 비틀기, 지난 7일간 | 수치(정수) | 1 |
| `diff_kn5` | 양쪽 무릎 중 하나 difficulty+E105: 무릎 꿇기, 지난 7일간 | 수치 또는 결측(値 없음) | (결측) |
| `koos_rksymptoms` | 오른쪽 무릎: KOOS 증상 점수 | 수치(연속형, 소수) | 78.6 |
| `koos_lksymptoms` | 왼쪽 무릎: KOOS 증상 점수 | 수치(연속형, 소수) | 71.4 |
| `koos_qol` | KOOS 삶의 질 점수 | 수치(정수) | 75 |
| `koos_rkpain` | 오른쪽 무릎: KOOS 통증 점수 | 수치(연속형, 소수) | 77.8 |
| `koos_lkpain` | 왼쪽 무릎: KOOS 통증 점수 | 수치(연속형, 소수) | 80.6 |
| `koos_sports` | KOOS 기능/스포츠/여가활동 점수 | 수치 또는 결측(値 없음) | (결측) |
| `womac_stiffness_right` | 오른쪽 무릎: WOMAC 강직 점수(계산값) | 범주형(등급/점수, 정수) | 2 |
| `womac_stiffness_left` | 왼쪽 무릎: WOMAC 강직 점수(계산값) | 범주형(등급/점수, 정수) | 3 |
| `womac_disability_right` | 오른쪽 무릎: WOMAC 장애(기능저하) 점수(계산값) | 수치(연속형, 소수) | 4.3 |
| `womac_disability_left` | 왼쪽 무릎: WOMAC 장애(기능저하) 점수(계산값) | 수치(연속형, 소수) | 6.4 |
| `womac_pain_left` | 왼쪽 무릎: WOMAC 통증 점수(계산값) | 범주형(등급/점수, 정수) | 3 |
| `womac_pain_right` | 오른쪽 무릎: WOMAC 통증 점수(계산값) | 범주형(등급/점수, 정수) | 3 |
| `womac_total_left` | 왼쪽 무릎: WOMAC 총점(계산값) | 수치(연속형, 소수) | 12.4 |
| `womac_total_right` | 오른쪽 무릎: WOMAC 총점(계산값) | 수치(연속형, 소수) | 9.3 |
| `collection_title` | collection_title | 범주형/문자열 | Osteoarthritis Initiative |

## OAI 무릎 X-ray 관절강 폭(JSW) 정량측정 (`oai_kxrquantjsw01`, 총 46개 컬럼)

| 컬럼명 | 설명(한글) | 데이터 타입 | 예시값 |
|---|---|---|---|
| `collection_id` | collection_id | ID(수치) | 2343 |
| `oai_kxrquantjsw01_id` | oai_kxrquantjsw01_id | ID(수치) | 37117 |
| `dataset_id` | dataset_id | ID(수치) | 53834 |
| `subjectkey` | 연구대상자 전역 고유식별자(GUID) | GUID | NDAR_INVV5HVXTKF |
| `src_subject_id` | 연구실/프로젝트 내부 피험자 ID | ID(수치) | 9000099 |
| `interview_date` | 면담/검사/영상촬영 등이 완료된 날짜 | 날짜(문자열, MM/DD/YYYY) | 07/08/2005 |
| `interview_age` | 면담/검사 시점의 나이(개월) | 수치(연속형) | 708 |
| `sex` | 출생 시 성별 | 범주형/문자열 | M |
| `ageyears` | 나이(년) | 수치(연속형) | 59 |
| `visit` | 방문시점 명칭 | 범주형/문자열 | V00 |
| `version` | 평가 버전/코드 | 범주형/문자열 | 0.8 |
| `readprj` | 프로젝트(판독 그룹) | 수치(정수) | 16 |
| `side` | 측(좌/우) | 범주형/문자열 | 1 |
| `incplm` | Incomplete delineation of 내측 구획 - some JSW(x) set to .T | 수치(정수) | 0 |
| `nomjswx` | 자세/화질 불량으로 내측 JSW 측정불가 | 수치(정수) | 0 |
| `nommjsw` | 내측 최소JSW 측정불가(자세/화질/기타) | 수치(정수) | 0 |
| `nolmin` | 내측 최소JSW 측정됐으나 국소최솟값 없음 | 수치(정수) | 0 |
| `mjswbb` | mJSW is set to zero, used when reader judges bone on bone in 내측 구획 | 수치(정수) | 0 |
| `tpcfds` | Distance from 경골l plateau to 경골l rim closest to femoral condyle (mm) | 수치(연속형, 소수) | 1.6 |
| `impixsz` | 픽셀→mm 변환용 픽셀크기(확대보정 안 됨)(mm) | 수치(연속형, 소수) | 0.1 |
| `bmang` | Synaflexer 팬텀 기준 X-ray 빔 각도(도) | 수치(연속형, 소수) | 11.57 |
| `mcmjsw` | 내측 최소 관절강폭(mm) | 수치(정수) | 4 |
| `xmjsw` | 최소 JSW 지점의 X좌표 | 수치(연속형, 소수) | 0.184 |
| `incstps` | 가장자리 거리 기준, 방문시점 간 자세 불일치 | 수치(정수) | 0 |
| `cfwdth` | x=1.0 기준이 되는 대퇴과 폭(mm) | 수치(연속형, 소수) | 95.76 |
| `jsw150` | 내측 관절강폭(JSW), x=0.150 (mm) | 수치(연속형, 소수) | 4.12 |
| `jsw175` | 내측 관절강폭(JSW), x=0.175 (mm) | 수치(연속형, 소수) | 4.12 |
| `jsw200` | 내측 관절강폭(JSW), x=0.200 (mm) | 수치(연속형, 소수) | 4.12 |
| `jsw225` | 내측 관절강폭(JSW), x=0.225 (mm) | 수치(연속형, 소수) | 4.01 |
| `jsw250` | 내측 관절강폭(JSW), x=0.250 (mm) | 수치(연속형, 소수) | 4.32 |
| `jsw275` | 내측 관절강폭(JSW), x=0.275 (mm) | 수치(연속형, 소수) | 4.82 |
| `jsw300` | 내측 관절강폭(JSW), x=0.300 (mm) | 수치(연속형, 소수) | 5.51 |
| `noljswx` | 자세/화질 불량으로 외측 JSW 측정불가 | 수치(정수) | 0 |
| `ltpmebe` | Lateral 경골l plateau margin is the same as the bone edge | 수치(정수) | 0 |
| `incpll` | Incomplete delineation of 외측 구획 - some JSW(x) set to .T | 수치(정수) | 0 |
| `ljsw700` | 외측 관절강폭(JSW), x=0.700 (mm) | 수치(연속형, 소수) | 6.02 |
| `ljsw725` | 외측 관절강폭(JSW), x=0.725 (mm) | 수치(연속형, 소수) | 6.33 |
| `ljsw750` | 외측 관절강폭(JSW), x=0.750 (mm) | 수치(연속형, 소수) | 6.12 |
| `ljsw775` | 외측 관절강폭(JSW), x=0.775 (mm) | 수치(연속형, 소수) | 6.22 |
| `ljsw800` | 외측 관절강폭(JSW), x=0.800 (mm) | 수치(연속형, 소수) | 6.42 |
| `ljsw825` | 외측 관절강폭(JSW), x=0.825 (mm) | 수치(연속형, 소수) | 6.22 |
| `ljsw850` | 외측 관절강폭(JSW), x=0.850 (mm) | 수치(연속형, 소수) | 5.82 |
| `ljsw875` | 외측 관절강폭(JSW), x=0.875 (mm) | 수치(연속형, 소수) | 5.61 |
| `ljsw900` | 외측 관절강폭(JSW), x=0.900 (mm) | 수치(연속형, 소수) | 5.52 |
| `barcode` | 분석된 영상의 바코드(이미지 자체 아님, 참조 ID) | 문자열(이미지 참조 ID, 이미지 파일 아님) | 16600839603 |
| `collection_title` | collection_title | 범주형/문자열 | Osteoarthritis Initiative |

## OAI 무릎 X-ray 반정량 점수 (KL grade 등) (`oai_kxrsemiquant01`, 총 34개 컬럼)

| 컬럼명 | 설명(한글) | 데이터 타입 | 예시값 |
|---|---|---|---|
| `collection_id` | collection_id | ID(수치) | 2343 |
| `oai_kxrsemiquant01_id` | oai_kxrsemiquant01_id | ID(수치) | 1 |
| `dataset_id` | dataset_id | ID(수치) | 55677 |
| `subjectkey` | 연구대상자 전역 고유식별자(GUID) | GUID | NDAR_INVV5HVXTKF |
| `src_subject_id` | 연구실/프로젝트 내부 피험자 ID | ID(수치) | 9000099 |
| `interview_date` | 면담/검사/영상촬영 등이 완료된 날짜 | 날짜(문자열, MM/DD/YYYY) | 07/08/2005 |
| `interview_age` | 면담/검사 시점의 나이(개월) | 수치(연속형) | 708 |
| `sex` | 출생 시 성별 | 범주형/문자열 | M |
| `ageyears` | 나이(년) | 수치(연속형) | 59 |
| `visit` | 방문시점 명칭 | 범주형/문자열 | V00 |
| `version` | 평가 버전/코드 | 범주형/문자열 | 0.8 |
| `readprj` | 프로젝트(판독 그룹) | 수치(정수) | 15 |
| `side` | 측(좌/우) | 범주형/문자열 | 1 |
| `xrkl` | Kellgren-Lawrence(KL) 등급 (0~4) | 범주형(등급/점수, 정수) | 2 |
| `xrjsl` | 관절강협착 OARSI 등급(0~3) 외측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrjsm` | 관절강협착 OARSI 등급(0~3) 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrcytl` | 낭종 유무(0~1) 경골 외측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrcytm` | 낭종 유무(0~1) 경골 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrcyfl` | 낭종 유무(0~1) 대퇴골 외측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrcyfm` | 낭종 유무(0~1) 대퇴골 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrostl` | 골극 OARSI 등급(0~3) 경골 외측 구획 | 범주형(등급/점수, 정수) | 1 |
| `xrostm` | 골극 OARSI 등급(0~3) 경골 내측 구획 | 범주형(등급/점수, 정수) | 1 |
| `xrosfl` | 골극 OARSI 등급(0~3) 대퇴골 외측 구획 | 범주형(등급/점수, 정수) | 2 |
| `xrosfm` | 골극 OARSI 등급(0~3) 대퇴골 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrsctm` | 경화 OARSI 등급(0~3) 경골 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrsctl` | 경화 OARSI 등급(0~3) 경골 외측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrscfm` | 경화 OARSI 등급(0~3) 대퇴골 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrscfl` | 경화 OARSI 등급(0~3) 대퇴골 외측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrattl` | 마모 OARSI 등급(0~3) 경골 외측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrattm` | 마모 OARSI 등급(0~3) 경골 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrchl` | 연골석회화증 유무(0~1) 외측 구획 | 범주형(등급/점수, 정수) | 0 |
| `xrchm` | 연골석회화증 유무(0~1) 내측 구획 | 범주형(등급/점수, 정수) | 0 |
| `barcode` | 분석된 영상의 바코드(이미지 자체 아님, 참조 ID) | 문자열(이미지 참조 ID, 이미지 파일 아님) | 16600839603 |
| `collection_title` | collection_title | 범주형/문자열 | Osteoarthritis Initiative |

## OAI 결과 데이터 (사망·고관절/무릎 치환술) (`oai_outcome01`, 총 106개 컬럼)

| 컬럼명 | 설명(한글) | 데이터 타입 | 예시값 |
|---|---|---|---|
| `collection_id` | collection_id | ID(수치) | 2343 |
| `oai_outcome01_id` | oai_outcome01_id | ID(수치) | 4797 |
| `dataset_id` | dataset_id | ID(수치) | 77337 |
| `subjectkey` | 연구대상자 전역 고유식별자(GUID) | GUID | NDAR_INVV5HVXTKF |
| `src_subject_id` | 연구실/프로젝트 내부 피험자 ID | ID(수치) | 9000099 |
| `interview_date` | 면담/검사/영상촬영 등이 완료된 날짜 | 날짜(문자열, MM/DD/YYYY) | 07/08/2005 |
| `interview_age` | 면담/검사 시점의 나이(개월) | 수치(연속형) | 708 |
| `sex` | 출생 시 성별 | 범주형/문자열 | M |
| `ageyears` | 나이(년) | 수치(연속형) | 59 |
| `version` | 평가 버전/코드 | 범주형/문자열 | 14 |
| `visit` | 방문시점 명칭 | 범주형/문자열 | V99 |
| `rntcnt` | 가장 최근 OAI 접촉시점 | 수치(정수) | 11 |
| `lhblrp` | 왼쪽 고관절, 고관절 치환술 seen on 기저(시작) X-ray | 수치(정수) | 0 |
| `lhdate` | 왼쪽 고관절, date of 추적관찰 고관절 치환술 | 날짜(문자열, MM/DD/YYYY) | (결측) |
| `lhdays` | 왼쪽 고관절, days between enrollment visit and 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lhfldt` | 왼쪽 고관절, 날짜 플래그, date of 추적관찰 고관절 치환술 from 자가보고 or 의무기록으로 판정됨 | 수치 또는 결측(値 없음) | (결측) |
| `lhpodx` | 왼쪽 고관절, 수술 전 주진단 | 수치 또는 결측(値 없음) | (결측) |
| `lhrpcf` | 왼쪽 고관절, 추적관찰 고관절 치환술 판정/확인 상태 | 수치 또는 결측(値 없음) | (결측) |
| `lhrpsn` | 왼쪽 고관절, 고관절 치환술 seen on 추적관찰 OAI x-ray | 수치 또는 결측(値 없음) | (결측) |
| `lhvsaf` | 왼쪽 고관절, 이후 가장 가까운 접촉시점 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lhvspr` | 왼쪽 고관절, 이전 가장 가까운 방문시점 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lhvsrp` | 왼쪽 고관절, OAI visit 추적관찰 고관절 치환술 자가보고 시점 | 수치 또는 결측(値 없음) | (결측) |
| `lhxraf` | 왼쪽 고관절, 가장 가까운 방문시점(해당 촬영 포함) hip x-ray after 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lhxrpr` | 왼쪽 고관절, 가장 가까운 방문시점(해당 촬영 포함) hip x-ray prior to 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `ljsfp` | 왼쪽 무릎, 최초 관찰 방문시점: 관절강협착(JSN) 진행 (부분등급 이상) | 범주형(등급/점수, 정수) | 1 |
| `ljsfw` | 왼쪽 무릎, 최초 관찰 방문시점: 관절강협착(JSN) 진행 (전체등급 이상) | 범주형(등급/점수, 정수) | 1 |
| `ljslp` | 왼쪽 무릎, 마지막 관찰 방문시점: 관절강협착(JSN) 진행 (부분등급 이상) | 수치(정수) | 6 |
| `ljslw` | 왼쪽 무릎, 마지막 관찰 방문시점: 관절강협착(JSN) 진행 (전체등급 이상) | 수치(정수) | 6 |
| `ljstfp` | 왼쪽 무릎, 대퇴경골(TF) 구획, 최초 관절강협착(JSN) 진행 (부분등급 이상) | 범주형(등급/점수, 정수) | 1 |
| `ljstfw` | 왼쪽 무릎, 대퇴경골(TF) 구획, 최초 관절강협착(JSN) 진행 (전체등급 이상) | 범주형(등급/점수, 정수) | 1 |
| `lkblrp` | 왼쪽 무릎, 무릎 치환술 seen on 기저(시작) X-ray | 수치(정수) | 0 |
| `lkdate` | 왼쪽 무릎, date of 추적관찰 무릎 치환술 | 날짜(문자열, MM/DD/YYYY) | (결측) |
| `lkdays` | 왼쪽 무릎, days between enrollment visit and 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lkfldt` | 왼쪽 무릎, 날짜 플래그, date of 추적관찰 무릎 치환술 from 자가보고 or 의무기록으로 판정됨 | 수치 또는 결측(値 없음) | (결측) |
| `lkloa` | 왼쪽 무릎, 마지막 관찰 방문시점: OA (KLG>=2) (calc) | 수치(정수) | 6 |
| `lkloan` | 왼쪽 무릎, 마지막 관찰 방문시점: OA (KLG>=2 and JSN>=1) (calc) | 수치(정수) | 6 |
| `lkpodx` | 왼쪽 무릎, 수술 전 주진단 | 수치 또는 결측(値 없음) | (결측) |
| `lkrpcf` | 왼쪽 무릎, 추적관찰 무릎 치환술 판정/확인 상태 | 수치 또는 결측(値 없음) | (결측) |
| `lkrpsn` | 왼쪽 무릎, 무릎 치환술 seen on 추적관찰 OAI x-ray | 수치 또는 결측(値 없음) | (결측) |
| `lktlpr` | 왼쪽 무릎, total or partial 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lktppr` | 왼쪽 무릎, type of partial 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lkvsaf` | 왼쪽 무릎, 이후 가장 가까운 방문시점 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lkvspr` | 왼쪽 무릎, 이전 가장 가까운 방문시점 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lkvsrp` | 왼쪽 무릎, OAI visit 추적관찰 무릎 치환술 자가보고 시점 | 수치 또는 결측(値 없음) | (결측) |
| `lkxraf` | 왼쪽 무릎, 가장 가까운 방문시점(해당 촬영 포함) knee x-ray after 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lkxrpr` | 왼쪽 무릎, 가장 가까운 방문시점(해당 촬영 포함) knee x-ray prior to 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `lnjslp` | 왼쪽 무릎, 마지막 관찰 방문시점: no 관절강협착(JSN) 진행 (부분등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `lnjslw` | 왼쪽 무릎, 마지막 관찰 방문시점: no 관절강협착(JSN) 진행 (전체등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `lxioa` | 왼쪽 무릎, 요약: 신규발생 대퇴경골 방사선학적OA(KL>=2) | 수치(정수) | 1 |
| `lxioan` | 왼쪽 무릎, 요약: 신규발생 대퇴경골 방사선학적OA(KL>=2) with JSN | 수치(정수) | 1 |
| `lxjsnl` | 왼쪽 무릎, 요약: 외측 관절강협착(JSN) 진행 to 96 mo visit | 수치(정수) | 4 |
| `lxjsnm` | 왼쪽 무릎, 요약: 내측 관절강협착(JSN) 진행 to 96 mo visit | 수치(정수) | 2 |
| `lxnoa` | 왼쪽 무릎, 마지막 방문시점 KL 2 미만 | 수치 또는 결측(値 없음) | (결측) |
| `lxnoan` | 왼쪽 무릎, 마지막 방문시점 KL 2 미만 or KL=2 with no JSN | 수치 또는 결측(値 없음) | (결측) |
| `rhblrp` | 오른쪽 고관절, 고관절 치환술 seen on 기저(시작) X-ray | 수치(정수) | 0 |
| `rhdate` | 오른쪽 고관절, date of 추적관찰 고관절 치환술 | 날짜(문자열, MM/DD/YYYY) | (결측) |
| `rhdays` | 오른쪽 고관절, days between enrollment visit and 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rhfldt` | 오른쪽 고관절, 날짜 플래그, date of 추적관찰 고관절 치환술 from 자가보고 or 의무기록으로 판정됨 | 수치 또는 결측(値 없음) | (결측) |
| `rhpodx` | 오른쪽 고관절, 수술 전 주진단 | 수치 또는 결측(値 없음) | (결측) |
| `rhrpcf` | 오른쪽 고관절, 추적관찰 고관절 치환술 판정/확인 | 수치 또는 결측(値 없음) | (결측) |
| `rhrpsn` | 오른쪽 고관절, 고관절 치환술 seen on 추적관찰 OAI x-ray | 수치 또는 결측(値 없음) | (결측) |
| `rhvsaf` | 오른쪽 고관절, 이후 가장 가까운 방문시점 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rhvspr` | 오른쪽 고관절, 이전 가장 가까운 방문시점 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rhvsrp` | 오른쪽 고관절, OAI visit 추적관찰 고관절 치환술 자가보고 시점 | 수치 또는 결측(値 없음) | (결측) |
| `rhxraf` | 오른쪽 고관절, 가장 가까운 방문시점(해당 촬영 포함) hip x-ray after 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rhxrpr` | 오른쪽 고관절, 가장 가까운 방문시점(해당 촬영 포함) hip x-ray prior to 추적관찰 고관절 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rjsfp` | 오른쪽 무릎, 최초 관찰 방문시점: 관절강협착(JSN) 진행 (부분등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `rjsfw` | 오른쪽 무릎, 최초 관찰 방문시점: 관절강협착(JSN) 진행 (전체등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `rjslp` | 오른쪽 무릎, 마지막 관찰 방문시점: 관절강협착(JSN) 진행 (부분등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `rjslw` | 오른쪽 무릎, 마지막 관찰 방문시점: 관절강협착(JSN) 진행 (전체등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `rjstfp` | 오른쪽 무릎, 대퇴경골(TF) 구획, 최초 관절강협착(JSN) 진행 (부분등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `rjstfw` | 오른쪽 무릎, 대퇴경골(TF) 구획, 최초 관절강협착(JSN) 진행 (전체등급 이상) | 범주형(등급/점수, 정수) | 0 |
| `rkblrp` | 오른쪽 무릎, 무릎 치환술 seen on 기저(시작) X-ray | 수치(정수) | 0 |
| `rkdate` | 오른쪽 무릎, date of 추적관찰 무릎 치환술 | 날짜(문자열, MM/DD/YYYY) | (결측) |
| `rkdays` | 오른쪽 무릎, days between enrollment visit and 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rkfldt` | 오른쪽 무릎, 날짜 플래그, date of 추적관찰 무릎 치환술 from 자가보고 or 의무기록으로 판정됨 | 수치 또는 결측(値 없음) | (결측) |
| `rkloa` | 오른쪽 무릎, 마지막 관찰 방문시점: OA (KLG>=2) (calc) | 수치(정수) | 6 |
| `rkloan` | 오른쪽 무릎, 마지막 관찰 방문시점: OA (KLG>=2 and JSN>=1) (calc) | 수치 또는 결측(値 없음) | (결측) |
| `rkpodx` | 오른쪽 무릎, 수술 전 주진단 | 수치 또는 결측(値 없음) | (결측) |
| `rkrpcf` | 오른쪽 무릎, 추적관찰 무릎 치환술 판정/확인 상태 | 수치 또는 결측(値 없음) | (결측) |
| `rkrpsn` | 오른쪽 무릎, 무릎 치환술 seen on 추적관찰 OAI x-ray | 수치 또는 결측(値 없음) | (결측) |
| `rktlpr` | 오른쪽 무릎, total or partial 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rktppr` | 오른쪽 무릎, type of partial 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rkvsaf` | 오른쪽 무릎, 이후 가장 가까운 방문시점 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rkvspr` | 오른쪽 무릎, 이전 가장 가까운 방문시점 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rkvsrp` | 오른쪽 무릎, OAI visit 추적관찰 무릎 치환술 자가보고 시점 | 수치 또는 결측(値 없음) | (결측) |
| `rkxraf` | 오른쪽 무릎, 가장 가까운 방문시점(해당 촬영 포함) knee x-ray after 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rkxrpr` | 오른쪽 무릎, 가장 가까운 방문시점(해당 촬영 포함) knee x-ray prior to 추적관찰 무릎 치환술 | 수치 또는 결측(値 없음) | (결측) |
| `rnjslp` | 오른쪽 무릎, 마지막 관찰 방문시점: no 관절강협착(JSN) 진행 | 수치(정수) | 6 |
| `rnjslw` | 오른쪽 무릎, 마지막 관찰 방문시점: no 관절강협착(JSN) 진행 | 수치(정수) | 6 |
| `rxioa` | 오른쪽 무릎, 요약: 신규발생 대퇴경골 방사선학적OA(KL>=2) | 수치(정수) | 1 |
| `rxioan` | 오른쪽 무릎, 요약: 신규발생 대퇴경골 방사선학적OA(KL>=2) with JSN | 수치(정수) | 2 |
| `rxjsnl` | 오른쪽 무릎, 요약: 외측 관절강협착(JSN) 진행 to 96 mo visit | 수치(정수) | 2 |
| `rxjsnm` | 오른쪽 무릎, 요약: 내측 관절강협착(JSN) 진행 to 96 mo visit | 수치(정수) | 2 |
| `rxnoa` | 오른쪽 무릎, 마지막 방문시점 KL 2 미만 | 수치 또는 결측(値 없음) | (결측) |
| `rxnoan` | 오른쪽 무릎, 마지막 방문시점 KL 2 미만 or KL=2 with no JSN | 수치(정수) | 6 |
| `xlvsqd` | 마지막 관찰 방문시점: 중앙판독 추적관찰 knee x-ray SQ (KL or JSN) data | 수치(정수) | 4 |
| `ddcf` | death 판정/확인 상태 | 수치(정수) | 2 |
| `dthdate` | 사망 날짜 | 날짜(문자열, MM/DD/YYYY) | 3/26/2018 |
| `ddvspr` | 이전 가장 가까운 방문시점 death | 수치(정수) | 11 |
| `ddfldt` | 날짜 플래그, date of death from documentation or from reported date of death | 수치(정수) | 1 |
| `edcod` | 국가사망지수 사망원인(ICD-10) | 수치 또는 결측(値 없음) | (결측) |
| `edcodr` | 사망원인 재분류(358개 ICD-10 그룹) | 수치 또는 결측(値 없음) | (결측) |
| `edcodr2` | 사망원인 재분류(113개 ICD-10 그룹) | 수치 또는 결측(値 없음) | (결측) |
| `eddyear` | 사망 연도 | 수치(정수) | 2018 |
| `collection_title` | collection_title | 범주형/문자열 | Osteoarthritis Initiative |

<img width="962" height="692" alt="image" src="https://github.com/user-attachments/assets/262a96d1-b4ca-4945-908c-e63b71b6f962" />

<img width="947" height="805" alt="image" src="https://github.com/user-attachments/assets/7d6fa81f-fa0e-4f3c-9b84-f4243b7d61c6" />

## 데이터 위치 ## : https://nda.nih.gov/landing_page.html (API 사용 허가는 받아둠)

## 8. 논의 사항 ##
1. oai_meduse01/oai_oapain01 라는 데이터에 환자들의 현재 복용 / 처치 중인 약물 정보가 존재
2. 각 데이터는 subject key로 전부 join 가능
3. 환자의 증상을 정량적으로 분석한 자료(XRay. MRI) 등의 이미지 분석 자료도 있지만, 환자의 주관적인 데이터 또한 담겨 있는데 이 데이터 들의 활용 야부
4. 환자의 데이터를 토대로 알 수 있는 내용 - oai_meduse01/oai_oapain01에서 같은 참가자의 복용 약물을 토데로 해당 약으로 치료받는 사람의 시간 별 경과 내역을 확인 할 수 있음
5. 만약 이 데이터를 활용할 거면 여기 데이터를 저장 후 사용하는 것이 아니라 tool로 받아오게 하는 방법이 더 좋을 것 같음( 데이터 용량이 말도 안되게 큼 )
6. 데이터가 너무 많아서 다 조사하지는 못했고 / 이 데이터를 활용할지에 대한 여부는 알 수 없으나 사용할만한 데이터들만 추려서 8/2 일 까지 정리해 둠
7. 영상 자료의 분석 결과(병의 질병 경과)를 이미 KLGrade로 점수화 시켜 놨기 떄문에 딱히  멀티 모달 모델이 필요해보이지는 않음
8. 사용한다면, 각 환자의 나이 분포에 따른 약물 처리 결과로 사용 가능하거나 혹은 약물별 치료 경과를 알 수 있음
9. 데이터 확인 중이나 특정 약물(치료 약물에 대한) 바이오 마커 데이터는 없는 것으로 확인되어 약물 바이오마커 데이터는 따로 가져와야 할 것 같음



