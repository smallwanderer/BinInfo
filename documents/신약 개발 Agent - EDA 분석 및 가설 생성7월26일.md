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
