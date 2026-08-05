import urllib.request
import json
from typing import Dict, Any, Optional

class OpenTargetsEvidenceFetcher:
    """
    Open Targets Platform GraphQL API (v4)를 활용하여
    Target Prioritisation (17개 평가 인자) 및 Association Evidence (6대 근거 점수)를
    단일 GraphQL 쿼리로 수집하는 모듈.
    """
    API_URL = "https://api.platform.opentargets.org/api/v4/graphql"

    # 대표 질환 MONDO/EFO ID 상수
    DISEASE_IDS = {
        "RA": "MONDO_0008383",      # Rheumatoid Arthritis (류마티스 관절염)
        "PsA": "EFO_0000384",       # Psoriatic Arthritis (건선성 관절염)
        "AS": "MONDO_0005404",      # Ankylosing Spondylitis (강직성 척추염)
        "OA": "MONDO_0005178"       # Osteoarthritis (골관절염)
    }

    def __init__(self, default_disease_id: str = "MONDO_0008383"):
        self.default_disease_id = default_disease_id

    def symbol_to_ensembl_id(self, symbol: str) -> Optional[str]:
        """HGNC Symbol(예: TNF, CXCR4, IL6R)을 Open Targets Ensembl ID로 변환"""
        query = """
        query SymbolToEnsembl($queryString: String!) {
          search(queryString: $queryString, entityNames: ["target"], page: {index: 0, size: 1}) {
            hits {
              id
              name
            }
          }
        }
        """
        payload = json.dumps({"query": query, "variables": {"queryString": symbol}}).encode("utf-8")
        req = urllib.request.Request(self.API_URL, data=payload, headers={"Content-Type": "application/json"})
        
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                hits = data.get("data", {}).get("search", {}).get("hits", [])
                if hits:
                    return hits[0]["id"]
        except Exception as e:
            print(f"[OpenTargets] Symbol 변환 에러 ({symbol}): {e}")
        return None

    def fetch_full_evidence(self, symbol_or_ensembl: str, disease_id: Optional[str] = None) -> Dict[str, Any]:
        """
        유전자 Symbol 또는 Ensembl ID를 받아 단일 GraphQL 호출로
        Target Prioritisation 및 Disease Association 근거를 수집하여 구조화된 반환값을 제공함.
        """
        target_disease = disease_id or self.default_disease_id
        if target_disease in self.DISEASE_IDS:
            target_disease = self.DISEASE_IDS[target_disease]

        if symbol_or_ensembl.startswith("ENSG"):
            ensembl_id = symbol_or_ensembl
        else:
            ensembl_id = self.symbol_to_ensembl_id(symbol_or_ensembl)
            if not ensembl_id:
                return {"error": f"Ensembl ID를 찾을 수 없습니다: {symbol_or_ensembl}"}

        # 단일 GraphQL 쿼리: Target Prioritisation + Disease Association 동시에 수집
        query = """
        query GetTargetFullEvidence($ensemblId: String!, $diseaseId: String!) {
          target(ensemblId: $ensemblId) {
            id
            approvedSymbol
            approvedName
            # 1. Target Prioritisation Factors (Safety, Tractability, Precedence 등 17개 인자)
            prioritisation {
              items {
                key
                value
              }
            }
            # 2. Associated Diseases (질환 연관성 및 6대 Datatype 근거 점수)
            associatedDiseases(Bs: [$diseaseId], enableIndirect: true) {
              rows {
                disease {
                  id
                  name
                }
                score
                datatypeScores {
                  id
                  score
                }
              }
            }
          }
        }
        """
        
        variables = {"ensemblId": ensembl_id, "diseaseId": target_disease}
        payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
        req = urllib.request.Request(self.API_URL, data=payload, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req) as resp:
                raw_res = json.loads(resp.read().decode("utf-8"))
                return self._parse_response(raw_res)
        except Exception as e:
            return {"error": f"API 호출 에러: {str(e)}"}

    def _parse_response(self, raw_res: Dict[str, Any]) -> Dict[str, Any]:
        """Open Targets GraphQL 응답 파싱 및 L2 아키텍처 규격 데이터 반환"""
        target_data = raw_res.get("data", {}).get("target")
        if not target_data:
            return {"error": "Target 정보를 찾을 수 없습니다."}

        # 1. Target Prioritisation Factors 파싱
        prioritisation_dict = {}
        if target_data.get("prioritisation") and target_data["prioritisation"].get("items"):
            for item in target_data["prioritisation"]["items"]:
                prioritisation_dict[item["key"]] = item["value"]

        # 2. Disease Association Scores 파싱
        association_info = {"total_score": 0.0, "datatype_scores": {}}
        assoc_rows = target_data.get("associatedDiseases", {}).get("rows", [])
        if assoc_rows:
            row = assoc_rows[0]
            association_info["disease_name"] = row["disease"]["name"]
            association_info["disease_id"] = row["disease"]["id"]
            association_info["total_score"] = round(row["score"], 4)
            for dt in row.get("datatypeScores", []):
                association_info["datatype_scores"][dt["id"]] = round(dt["score"], 4)

        return {
            "symbol": target_data["approvedSymbol"],
            "ensembl_id": target_data["id"],
            "name": target_data["approvedName"],
            "target_prioritisation": prioritisation_dict,
            "disease_association": association_info
        }

if __name__ == "__main__":
    print("=========================================================================")
    print(" Open Targets Evidence Fetcher 검증 테스트 (snippets/opentargets_evidence_fetcher.py)")
    print("=========================================================================\n")
    
    fetcher = OpenTargetsEvidenceFetcher()
    
    # 1. TNF 테스트 (류마티스 관절염 RA)
    tnf_res = fetcher.fetch_full_evidence("TNF", "RA")
    print(f"1. Target: {tnf_res['symbol']} ({tnf_res['ensembl_id']}) - {tnf_res['name']}")
    print(f" - Disease: {tnf_res['disease_association'].get('disease_name')} ({tnf_res['disease_association'].get('disease_id')})")
    print(f" - Total Association Score: {tnf_res['disease_association'].get('total_score', 0.0)}")
    print(" - Datatype Evidence Scores:")
    for dt, score in tnf_res['disease_association'].get('datatype_scores', {}).items():
        print(f"    * {dt:<25}: {score}")
    print(" - Prioritisation Key Factors:")
    for k in ["geneticConstraint", "hasLigand", "hasPocket", "hasSafetyEvent", "isInMembrane", "isSecreted", "maxClinicalStage"]:
        if k in tnf_res['target_prioritisation']:
            print(f"    * {k:<30}: {tnf_res['target_prioritisation'][k]}")

    print("\n-------------------------------------------------------------------------\n")

    # 2. CXCR4 테스트 (류마티스 관절염 RA)
    cxcr4_res = fetcher.fetch_full_evidence("CXCR4", "RA")
    print(f"2. Target: {cxcr4_res['symbol']} ({cxcr4_res['ensembl_id']}) - {cxcr4_res['name']}")
    print(f" - Disease: {cxcr4_res['disease_association'].get('disease_name')} ({cxcr4_res['disease_association'].get('disease_id')})")
    print(f" - Total Association Score: {cxcr4_res['disease_association'].get('total_score', 0.0)}")
    print(" - Datatype Evidence Scores:")
    for dt, score in cxcr4_res['disease_association'].get('datatype_scores', {}).items():
        print(f"    * {dt:<25}: {score}")
