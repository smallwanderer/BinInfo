# Dataset
from tdc.single_pred import ADME

"""
What is ADME?
- 약동학, 약물이 투여된 후 체내에서 이루어지는 약물의 변화과정
- 약동학의 ADME가 기준에 미치지 못하는 경우 신약 개발이 중단될 수 있다.

A(흡수, Absorption): 약물이 체내로 흡수되는 과정. 대부분 위나 장에서 흡수된다.
D(분포, Distribution): 약물이 흡수 후 표적 조직으로 분포되는 과정
M(대사, Metabolism): 간 등에서 약물이 대사되는 과정
E(배설, Excretion): 약물이 대사 후 체내에서 배설되는 과정


"""

data = ADME(name="Solubility_AqSolDB") # 약물의 분자 구조를 바탕으로, 수용성 값을 예측하는 회귀 모델용 데이터셋
"""
Y = 수용성(Aqueous Solubility)을 LogS 단위로 변환한 값.
Logs: 물 1리터에 녹는 약물의 양을 몰 농도(mol/L)로 변환한 값에 상용로그를 취한 값
* -10에서 2 사이의 수치로 표현됩니다.
X = 분자 구조(SMILES)
"""

from eda import analyze_dataframe
import os

df = data.get_data()
if not os.path.exists("./ml_snippets/aqueous_solubility_eda"):
    analyze_dataframe(df, output_dir="./ml_snippets/aqueous_solubility_eda", show=True)

"""
split method
- random: 무작위 분할, 유사 분자가 양쪽에 섞입니다
- scaffold: 같은 뼈대 구조를 가진 분자는 같은 셋으로 묶입니다.
- cold_drug: 특정 약물 그룹은 test, 나머지는 train/valid로 분할 (신약 개발에서 못보던 새로운 약물에 대한 예측 성능을 확인)
"""
split = data.get_split(method="scaffold", seed=42)

train = split['train']
valid = split['valid']
test = split['test']

print("============= Train HEAD =============\n", train.head())
print("Train shape", train.shape, "Valid shape", valid.shape, "Test shape", test.shape)

# Descriptor

import pandas as pd
import numpy as np

from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors


def smiles_to_descriptors_lipinski(smiles):
    """
    SMILES 문자열을 받아 RDKit descriptor dictionary로 변환합니다.
    Lipinski's Rule of Five를 기반으로, 경구 투여 시 채네 흡수율과 투과 가능성을 예측할 때 이용하는 기준입니다.
    1. 분자량이 500Da 이하
    2. LogP가 5 이하
    3. 수소결합 주개(donor) 수가 5개 이하
    4. 수소결합 받개(acceptor) 수가 10개 이하
ㅇ
    Descriptor           | 의미                                                   | 직관
    -------------------------------------------------------------------------------------------------------------------
    MolWt                | 분자량                                                | 약물의 크기
    LogP                 | 지용성/수소성                                           | 물보다 기름에 더 잘녹는가?
    TPSA                 | polar surface area                                      | 극성 표면적이 어느정도인가?
    HBD                  | hydrogend bond doner 수                               | 수소 결합을 줄 수 있는가?
    HBA                  | hydrogen bond acceptor 수                             | 수소 결합을 받을 수 있는가?
    RotatableBonds       | 회전 가능 결합                                        | 구조가 유연한가?

    변환 실패 시 None을 반환합니다.
    """
    mol = Chem.MolFromSmiles(smiles)
    
    if mol is None:
        return None
    
    return {
        "MolWt": Descriptors.MolWt(mol),
        "LogP": Crippen.MolLogP(mol),
        "TPSA": rdMolDescriptors.CalcTPSA(mol),
        "HBD": rdMolDescriptors.CalcNumHBD(mol),
        "HBA": rdMolDescriptors.CalcNumHBA(mol),
        "RotatableBonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
    }


def smiles_to_descriptors_morgan(smiles):
    """
    SMILES 문자열을 받아 RDKit morgan fingerprint(분자 구조의 2진 벡터 표현)로 변환합니다.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    

    # Morgan Fingerprint 생성(원자 주변의 2~3개 원자 환경을 해시하여 2048비트의 2진 벡터로 표현) - 분자의 부분 구조 정보 인코딩
    
    fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
    fp_array = np.array(fp)
    
    desc = {
        "MolWt": Descriptors.MolWt(mol),
        "LogP": Crippen.MolLogP(mol),
        "TPSA": rdMolDescriptors.CalcTPSA(mol),
        "HBD": rdMolDescriptors.CalcNumHBD(mol),
        "HBA": rdMolDescriptors.CalcNumHBA(mol),
        "RotatableBonds": rdMolDescriptors.CalcNumRotatableBonds(mol),
        "RingCount": rdMolDescriptors.CalcNumRings(mol),                # 고리 수: 많을수록 난용성
        "AromaticRings": rdMolDescriptors.CalcNumAromaticRings(mol),    # 방향족 고리: 소수성 기여
        "FractionCSP3": rdMolDescriptors.CalcFractionCSP3(mol),         # sp3 탄소 비율: 높을수록 유연하고 용해도 ↑
    }
    
    # Fingerprint + descriptor 합치기
    fp_dict = {f"fp_{i}": v for i, v in enumerate(fp_array)}
    
    return {**desc, **fp_dict}


    
def featurize_dataframe(df):
    """
    TDC DataFrame의 Drug 컬럼에 있는 SMILES를 descriptor로 변환합니다.
    """
    descriptor_list = []
    valid_indices = []
    
    for idx, smiles in df["Drug"].items():
        desc = smiles_to_descriptors_morgan(smiles)
        
        if desc is not None:
            descriptor_list.append(desc)
            valid_indices.append(idx)
    
    X = pd.DataFrame(descriptor_list, index=valid_indices)
    y = df.loc[valid_indices, "Y"]
    
    return X, y


# featruize
X_train, y_train = featurize_dataframe(train)
X_valid, y_valid = featurize_dataframe(valid)
X_test, y_test = featurize_dataframe(test)

print(X_train.head())


# Model-Train

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

best_mae, best_params = np.inf, {}
for params in ParameterGrid({
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20]
    }):

        model = RandomForestRegressor(
            **params,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)
        mae = mean_absolute_error(y_valid, model.predict(X_valid))

        if mae < best_mae:
            best_mae = mae
            best_params = params


print(f"Best Hyperparameters: {best_params}, Best MAE: {best_mae}")        

model = RandomForestRegressor(
    **best_params,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

train_pred = model.predict(X_train)
valid_pred = model.predict(X_valid)
test_pred = model.predict(X_test)



# Model Evaluatation

def evaluate_regression(y_true, y_pred, name="set"):
    """
    결과 요약:

    지표 | 의미 
    MAE(Mean Abolute Error) | 예측값과 실제값의 차이를 절댓값으로 평균낸 값
    RMSE(Root Mean Squared Error) | 예측값과 실제값의 차이를 제곱하여 평균낸 후 제곱근을 씌운 값
    R2(R-squared) | 예측값과 실제값의 관계를 설명하는 비율

    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    print(f"[{name}]")
    print(f"MAE : {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2  : {r2:.4f}")
    print()

evaluate_regression(y_train, train_pred, "Train")
evaluate_regression(y_valid, valid_pred, "Validation")
evaluate_regression(y_test, test_pred, "Test")


# Model Prediction
"""
Lipinski 결괴:
[Test]
MAE : 0.9283
RMSE: 1.2710
R2  : 0.6968

Morgan Fingerprint 결과:
[Test]
MAE : 0.8525
RMSE: 1.1873
R2  : 0.7354
"""


result = pd.DataFrame({
    "SMILES": test.loc[X_test.index, "Drug"],
    "Actual_Y": y_test,
    "Predicted_Y": test_pred,
    "Error": y_test - test_pred
})

print(result.head(10))


# Feature Importance
"""
Lipinski:
          feature  importance
1            LogP    0.742856
0           MolWt    0.109869
2            TPSA    0.056350
5  RotatableBonds    0.041079
4             HBA    0.035941
3             HBD    0.013905
-> 지용성/수소성이 분자의 수용성에 가장 큰 영향을 미친다는 것을 의미합니다.

Morgan:
           feature    importance
1             LogP  6.177194e-01
0            MolWt  5.544682e-02
8     FractionCSP3  5.020180e-02
2             TPSA  2.696185e-02
744         fp_735  1.254622e-02
"""
feature_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print(feature_importance)


# Feature Importance Visualization

import matplotlib.pyplot as plt
# 1. 예측값 vs 실제값 scatter plot
plt.figure(figsize=(6, 6))
plt.scatter(y_test, test_pred, alpha=0.4)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label="perfect")
plt.xlabel("Actual LogS")
plt.ylabel("Predicted LogS")
plt.title("Actual vs Predicted Solubility (Test Set)")
plt.legend()
plt.tight_layout()
plt.savefig("./ml_snippets/aqueous_solubility_eda/pred_vs_actual.png")
# 2. Feature Importance Bar Chart
feature_importance.head(15).plot(x="feature", y="importance", kind="barh", figsize=(8, 6))
plt.title("Top 15 Feature Importances")
plt.tight_layout()
plt.savefig("./ml_snippets/aqueous_solubility_eda/feature_importance.png")