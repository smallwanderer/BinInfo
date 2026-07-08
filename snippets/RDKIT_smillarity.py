from typing import Optional
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator, rdMCS
from rdkit import DataStructs

class MolSimilarity:
    """
    동일 분자의 비교와 유사도 비교
    1. 두 SMILES가 같은 분자인가?
    2. 두 분자가 비슷한 분자인가?
    3. 한 분자가 다른 분자의 부분구조를 포함하는가?
    4. 두 분자 간 공유하는 공통 구조는 무엇인가?

    
    """

    def __init__(self, smi: str):
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            raise ValueError("Invalid SMILES string")
        self.smi = smi
        self.mol = mol
        self.can_smiles = self.canonical_smiles()


    def canonical_smiles(self) -> str:
        # isomericSmiles: 동일성 비교에서 입체 정보 및 동위원소 정보를 포함할지 결정(입체이성질체, stereoisomeric 고려)
        # canonical=True: 동일한 분자의 canonical SMILES를 반환
        return Chem.MolToSmiles(self.mol, canonical=True, isomericSmiles=True)


    def is_same_molecule(self, other: 'MolSimilarity') -> bool:
        # canonical SMILES를 비교하여 두 분자가 동일한 분자인지 확인
        return self.canonical_smiles() == other.canonical_smiles()

    
    def is_similar_molecule(self, other: 'MolSimilarity', threshold: float = 0.8) -> float:
        # fingerprint: 분자의 구조적 특징을 압축한 벡터
        # morgan fingerprint: 분자의 특정 원자를 중심으로 반지름 2만큼의 범위 내에 있는 원자 및 연결 정보를 해싱하여 벡터로 변환
        # 즉, 각 원자 주변의 부분구조 패턴을 모아 만든 분자 지문
        generator = rdFingerprintGenerator.GetMorganGenerator(
            radius=2,       # radius: fingerprint의 범위, 반지름이 클수록 더 많은 정보를 포함
            fpSize=2048     # fpSize: fingerprint의 길이, 길수록 더 많은 정보를 포함
        )
        fp1 = generator.GetFingerprint(self.mol)
        fp2 = generator.GetFingerprint(other.mol)

        print(fp1.GetNumBits())
        print(fp2.GetNumBits())
        print(fp1.ToBitString()[:100])
        print(fp2.ToBitString()[:100])
        
        # Tanimoto Similarity: 두 벡터 간의 유사도를 계산하는 방법 (두 벡터의 교집합 / 두 벡터의 합집합)
        tan = DataStructs.TanimotoSimilarity(fp1, fp2)
        return tan
    

    def substructure_search(self, other: 'MolSimilarity') -> bool:
        # substructure search: 한 분자가 다른 분자의 부분구조를 포함하는지 확인
        pattern1 = Chem.MolFromSmarts(self.smi)
        pattern2 = Chem.MolFromSmarts(other.smi)

        # HasSubstructMatch: self.mol이 pattern1 또는 pattern2를 부분구조로 포함하는지 확인
        if self.mol.HasSubstructMatch(pattern1):
            print(f"{self.smi} is a substructure of {other.smi}")
        
        if self.mol.HasSubstructMatch(pattern2):
            print(f"{other.smi} is a substructure of {self.smi}")

        return self.mol.HasSubstructMatch(pattern1) or self.mol.HasSubstructMatch(pattern2)


    def maximum_common_substructure(self, other: 'MolSimilarity'):
        # maximum_common_substructure: 두 분자 간 공유하는 최대 공통 구조 찾기
        res = rdMCS.FindMCS([self.mol, other.mol])
        # res.numAtoms: MCS의 원자 수
        # res.numBonds: MCS의 결합 수
        # res.numFragments: MCS의 조각 수
        # res.smartsString: MCS의 SMARTS 문자열
        return res


if __name__ == "__main__":
    mol1 = MolSimilarity("OCC")
    mol2 = MolSimilarity("CCCO")

    print(mol1.is_same_molecule(mol2))
    print(mol1.is_similar_molecule(mol2))