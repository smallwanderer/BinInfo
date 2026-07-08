from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem
from rdkit import DataStructs
import numpy as np

from rdkit import Chem

smi1 = "OCC"
smi2 = "CCO"

mol1 = Chem.MolFromSmiles(smi1)
mol2 = Chem.MolFromSmiles(smi2)

fp1 = AllChem.GetMorganFingerprintAsBitVect(mol1, 2, nBits=2048)
fp2 = AllChem.GetMorganFingerprintAsBitVect(mol2, 2, nBits=2048)

tan = DataStructs.TanimotoSimilarity(fp1, fp2)

print(tan)

can1 = Chem.MolToSmiles(mol1, canonical=True)
can2 = Chem.MolToSmiles(mol2, canonical=True)

print(can1)
print(can2)
print(can1 == can2)