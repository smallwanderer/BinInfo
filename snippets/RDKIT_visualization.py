import os

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem

class MoleculeVisualization:
    def __init__(self, smiles):
        if isinstance(smiles, str):
            self.mol = [Chem.MolFromSmiles(smiles)]
            self.smiles = [smiles]
        elif isinstance(smiles, list):
            self.mols = [Chem.MolFromSmiles(s) for s in smiles if Chem.MolFromSmiles(s) is not None]
            self.smiles = [s for s in smiles if Chem.MolFromSmiles(s) is not None]
        elif isinstance(smiles, Chem.Mol):
            self.mol = [smiles]
            self.smiles = [smiles.smiles]
        else:
            raise ValueError("Invalid input type")

    def visualize_single_molecule(self):
        img = Draw.MolToImage(self.mol[0], legend=self.smiles[0])
        img.show()


    def visualize_multiple_molecules(self, molsPerRow: int = 3):
        if self.mols is None:
            raise ValueError("No molecules to visualize")
        img = Draw.MolsToGridImage(
            self.mols, 
            molsPerRow=molsPerRow,
            subImgSize=(250, 250),
            legends=([smi for smi in self.smiles])
            )
        img.show()
    

    def draw_single_molecule(self, save_path: str, svg=True):
        ext = 'svg' if svg else 'png'
        os.makedirs(save_path, exist_ok=True)
        dir_path = os.path.join(save_path, f"{self.smiles[0]}.{ext}")

        img = Draw.MolToGridImage(
            self.mol,
            molsPerRow=1,
            subImgSize=(250, 250),
            legends=[self.smiles[0]],
            useSVG=svg
        )

        if svg:
            with open(dir_path, "wb") as f:
                f.write(img)
        else:
            img.save(dir_path, format="PNG")


    def draw_multiple_molecules(self, save_path: str, molsPerRow: int = 3, svg=True):
        ext = 'svg' if svg else 'png'
        # 디렉토리가 없으면 자동 생성
        os.makedirs(save_path, exist_ok=True)
        dir_path = os.path.join(save_path, f"multiple_molecules.{ext}")
        
        sub_width, sub_height = 250, 250
        img = Draw.MolsToGridImage(
            self.mols,
            molsPerRow=molsPerRow,
            subImgSize=(sub_width, sub_height),
            legends=self.smiles,
            useSVG=svg
        )
        
        if svg:
            # RDKit Bug: 첫 번째 셀(0,0)에만 250x250 크기의 흰색 배경 rect를 생성하는 버그가 있습니다.
            # 이를 해결하기 위해 첫 번째 rect의 크기를 전체 grid 크기(width, height)로 확장해 줍니다.
            cols = molsPerRow
            rows = (len(self.mols) + cols - 1) // cols
            total_width = cols * sub_width
            total_height = rows * sub_height
            
            old_rect = f"width='{sub_width}.0' height='{sub_height}.0'"
            new_rect = f"width='{total_width}.0' height='{total_height}.0'"
            img = img.replace(old_rect, new_rect, 1)

            with open(dir_path, "w", encoding="utf-8") as f:
                f.write(img)
        else:
            img.save(dir_path, format="PNG")

    
    def draw_3d_single_molecules(self, save_path: str):
        import py3Dmol
        os.makedirs(save_path, exist_ok=True)
        dir_path = os.path.join(save_path, f"{self.smiles[0]}_3d.html")

        mols_with_hs = Chem.AddHs(self.mol[0])                  # 3D 구조를 위한 수소 추가
        AllChem.EmbedMolecule(mols_with_hs, randomSeed=42)      # 3D 좌표 생성
        AllChem.MMFFOptimizeMolecule(mols_with_hs)              # 좌표 최적화
        mol_block = Chem.MolToMolBlock(mols_with_hs)            # mol block 생성


        viewer = py3Dmol.view(width=500, height=500)
        viewer.addModel(mol_block, 'mol')
        viewer.setStyle({
            "stick": {"radius": 0.15},
            "sphere": {"scale": 0.25}
        })
        viewer.zoomTo()

        # 수소를 제외한 원자번호 및 기호 라벨
        conf = mols_with_hs.GetConformer(0)

        for atom in mols_with_hs.GetAtoms():
            symbol = atom.GetSymbol()
            if symbol != 'H':
                idx = atom.GetIdx()
                pos = conf.GetAtomPosition(idx)
                viewer.addLabel(
                    f"{symbol} \n {idx}", 
                    {
                        "position": {"x": pos.x, "y": pos.y, "z": pos.z},
                        "backgroundColor": "white",
                        "backgroundOpacity": 0.7,
                        "fontColor": "black",
                        "fontSize": 9
                    }
                )

        # 좌측 상단 분자 정보 라벨 카드 고정
        viewer.addLabel(
            f"Mol Name: {self.smiles[0][:20]}",
            {
                "position": {"x": 10, "y": 10},
                "backgroundColor": "white",
                "backgroundOpacity": 0.7,
                "fontColor": "black",
                "fontSize": 9
            }
        )

        # 반투명 분자 표면 시각화
        # viewer.addSurface(py3Dmol.VDW,
        # {
        #     "opacity": 0.5,
        #     "color": "lightblue"
        # })

        # 자동 회전 적용
        viewer.spin(True)

        viewer.zoomTo()

        with open(dir_path, "w", encoding="utf-8") as f:
            f.write(viewer.write_html())
        

if __name__ == "__main__":
    """
    분자	SMILES	관찰 포인트
    Aspirin	CC(=O)Oc1ccccc1C(=O)O	방향족 고리 + branch carbonyl
    Caffeine	Cn1cnc2n(C)c(=O)n(C)c(=O)c12	fused aromatic/heterocycle + ring 번호 1,2
    Ibuprofen	CC(C)Cc1ccc(cc1)C(C)C(=O)O	branch 많은 alkyl + benzene ring
    Nicotine	CN1CCC[C@H]1c2cccnc2	포화 고리 + 방향족 pyridine + chirality
    Penicillin G	CC1(C)S[C@@H]2[C@H](NC(=O)Cc3ccccc3)C(=O)N2[C@H]1C(=O)O	fused ring + sulfur + amide + stereo
    Warfarin	CC(=O)CC(c1ccccc1)c1c(O)c2ccccc2oc1=O	여러 방향족 고리 + fused ring
    Atorvastatin fragment	CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccccc2)n(C[C@H](O)C[C@H](O)CC(=O)O)c1-c1ccc(F)cc1	매우 많은 branch + aromatic ring 여러 개 + stereo
    Cholesterol	C[C@H](CCC[C@@H](C)C)C1CCC2C1(CCC3C2CCC4=CC(O)CC[C@]34C)C	steroid fused ring + stereo 중심 다수
    """
    smile = "C[C@H](CCC[C@@H](C)C)C1CCC2C1(CCC3C2CCC4=CC(O)CC[C@]34C)C" # benzen
    smiles = ["CCO", "CC(=O)O", "c1ccccc1", "c1ccccc1O"]

    single_vis = MoleculeVisualization(smile)
    multi_vis = MoleculeVisualization(smiles)


    # single_vis.visualize_single_molecule()
    # multi_vis.visualize_multiple_molecules()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(current_dir, "images")

    # multi_vis.draw_multiple_molecules(save_dir, svg=True)
    single_vis.draw_3d_single_molecules(save_dir)
