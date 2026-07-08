"""
eda_visualizer.py
==================
어떤 pandas DataFrame이 들어와도 기본적인 구조 파악 + 시각화를 자동으로
수행해주는 범용 EDA(탐색적 데이터 분석) 모듈.

사용법
------
    from eda_visualizer import analyze_dataframe

    analyze_dataframe(df)                      # 콘솔 출력 + 그림 파일 저장
    analyze_dataframe(df, output_dir="eda_out") # 저장 경로 지정
    analyze_dataframe(df, show=True)            # plt.show()로 즉시 표시 (스크립트 실행 환경)

주요 기능
---------
1. 기본 정보 요약   : shape, dtypes, head, info, describe
2. 결측치 시각화     : 컬럼별 결측 비율 막대그래프 + 결측 위치 히트맵
3. 수치형 분포       : 히스토그램 + KDE, 박스플롯(이상치 확인)
4. 범주형 분포       : 상위 카테고리 빈도 막대그래프
5. 상관관계          : 수치형 컬럼 간 상관관계 히트맵
6. 자동 요약 리포트  : 위 내용을 종합한 텍스트 요약 반환
"""

from __future__ import annotations

import os
import math
import warnings
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", font_scale=0.95)


# --------------------------------------------------------------------------- #
# 내부 유틸
# --------------------------------------------------------------------------- #
def _save_or_show(fig, path: Optional[str], show: bool):
    if path:
        fig.savefig(path, dpi=140, bbox_inches="tight")
    if show:
        plt.show()
    plt.close(fig)


def _split_columns(df: pd.DataFrame):
    """수치형 / 범주형 / 날짜형 컬럼을 분리."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64", "datetimetz"]).columns.tolist()
    categorical_cols = [
        c for c in df.columns
        if c not in numeric_cols and c not in datetime_cols
    ]
    return numeric_cols, categorical_cols, datetime_cols


# --------------------------------------------------------------------------- #
# 1. 기본 정보 요약
# --------------------------------------------------------------------------- #
def print_basic_info(df: pd.DataFrame):
    print("=" * 70)
    print("1. 기본 정보 (Shape / Dtypes)")
    print("=" * 70)
    print(f"행(row) 수 : {df.shape[0]:,}")
    print(f"열(col) 수 : {df.shape[1]:,}")
    print()
    print("컬럼별 데이터 타입:")
    print(df.dtypes)
    print()

    print("=" * 70)
    print("2. 상위 5개 행 (head)")
    print("=" * 70)
    print(df.head())
    print()

    print("=" * 70)
    print("3. info()")
    print("=" * 70)
    df.info()
    print()

    print("=" * 70)
    print("4. describe() - 수치형 + 범주형 모두 포함")
    print("=" * 70)
    try:
        print(df.describe(include="all").T)
    except Exception:
        print(df.describe().T)
    print()


# --------------------------------------------------------------------------- #
# 2. 결측치 시각화
# --------------------------------------------------------------------------- #
def plot_missing_values(df: pd.DataFrame, output_dir: Optional[str], show: bool):
    missing = df.isna().sum()
    missing_ratio = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({"missing_count": missing, "missing_pct": missing_ratio})
    missing_df = missing_df[missing_df["missing_count"] > 0].sort_values(
        "missing_pct", ascending=False
    )

    print("=" * 70)
    print("5. 결측치 현황")
    print("=" * 70)
    if missing_df.empty:
        print("결측치가 없습니다.")
        print()
        return
    print(missing_df)
    print()

    fig, axes = plt.subplots(1, 2, figsize=(13, max(3, 0.35 * len(missing_df) + 2)))

    # 막대그래프: 컬럼별 결측 비율
    axes[0].barh(missing_df.index.astype(str), missing_df["missing_pct"], color="#e07a5f")
    axes[0].set_xlabel("결측 비율 (%)")
    axes[0].set_title("Missing Rate by Columns")
    axes[0].invert_yaxis()

    # 히트맵: 결측 위치 패턴 (샘플링해서 표시, 너무 크면 다운샘플)
    sample_df = df if len(df) <= 500 else df.sample(500, random_state=0).sort_index()
    sns.heatmap(sample_df.isna(), cbar=False, cmap="rocket_r", ax=axes[1])
    axes[1].set_title("Missing Value Pattern" + (" (500 rows sample)" if len(df) > 500 else ""))
    axes[1].set_yticks([])

    fig.tight_layout()
    path = os.path.join(output_dir, "missing_values.png") if output_dir else None
    _save_or_show(fig, path, show)


# --------------------------------------------------------------------------- #
# 3. 수치형 분포
# --------------------------------------------------------------------------- #
def plot_numeric_distributions(
    df: pd.DataFrame, numeric_cols: list, output_dir: Optional[str], show: bool, max_cols: int = 12
):
    print("=" * 70)
    print("6. 수치형 컬럼 분포")
    print("=" * 70)
    if not numeric_cols:
        print("수치형 컬럼이 없습니다.")
        print()
        return

    cols = numeric_cols[:max_cols]
    if len(numeric_cols) > max_cols:
        print(f"수치형 컬럼이 {len(numeric_cols)}개라 상위 {max_cols}개만 시각화합니다.")

    n = len(cols)
    ncols = min(3, n)
    nrows = math.ceil(n / ncols)

    # 히스토그램 + KDE
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 3.5 * nrows))
    axes = np.atleast_1d(axes).flatten()
    for i, col in enumerate(cols):
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i], color="#3d5a80")
        axes[i].set_title(f"{col} distribution")
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")
    fig.tight_layout()
    path = os.path.join(output_dir, "numeric_distributions.png") if output_dir else None
    _save_or_show(fig, path, show)

    # 박스플롯 (이상치 확인)
    fig2, ax2 = plt.subplots(figsize=(max(6, n * 1.2), 4.5))
    normalized = (df[cols] - df[cols].mean()) / df[cols].std(ddof=0)
    sns.boxplot(data=normalized, ax=ax2, palette="Set2")
    ax2.set_title("Boxplots of Numeric Columns (Standardized, for Outlier Detection)")
    ax2.tick_params(axis="x", rotation=30)
    fig2.tight_layout()
    path2 = os.path.join(output_dir, "numeric_boxplots.png") if output_dir else None
    _save_or_show(fig2, path2, show)

    print(df[cols].describe().T)
    print()


# --------------------------------------------------------------------------- #
# 4. 범주형 분포
# --------------------------------------------------------------------------- #
def plot_categorical_distributions(
    df: pd.DataFrame, categorical_cols: list, output_dir: Optional[str], show: bool,
    max_cols: int = 8, top_n: int = 10,
):
    print("=" * 70)
    print("7. 범주형 컬럼 분포")
    print("=" * 70)
    if not categorical_cols:
        print("범주형 컬럼이 없습니다.")
        print()
        return

    # 카디널리티 너무 높은(예: ID성) 컬럼은 제외
    usable_cols = [c for c in categorical_cols if df[c].nunique(dropna=True) <= max(50, len(df) * 0.5)]
    skipped = set(categorical_cols) - set(usable_cols)
    if skipped:
        print(f"고유값이 지나치게 많아 시각화에서 제외된 컬럼: {sorted(skipped)}")

    cols = usable_cols[:max_cols]
    if not cols:
        print("시각화 가능한 범주형 컬럼이 없습니다 (전부 고카디널리티).")
        print()
        return
    if len(usable_cols) > max_cols:
        print(f"범주형 컬럼이 {len(usable_cols)}개라 상위 {max_cols}개만 시각화합니다.")

    n = len(cols)
    ncols = min(2, n)
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(7 * ncols, 4 * nrows))
    axes = np.atleast_1d(axes).flatten()

    for i, col in enumerate(cols):
        vc = df[col].value_counts(dropna=False).head(top_n)
        sns.barplot(x=vc.values, y=vc.index.astype(str), ax=axes[i], color="#81b29a")
        axes[i].set_title(f"{col} Top {min(top_n, len(vc))} Values Frequency")
        axes[i].set_xlabel("count")
        print(f"[{col}] 고유값 개수: {df[col].nunique(dropna=True)}")
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    fig.tight_layout()
    path = os.path.join(output_dir, "categorical_distributions.png") if output_dir else None
    _save_or_show(fig, path, show)
    print()


# --------------------------------------------------------------------------- #
# 5. 상관관계
# --------------------------------------------------------------------------- #
def plot_correlation_heatmap(
    df: pd.DataFrame, numeric_cols: list, output_dir: Optional[str], show: bool
):
    print("=" * 70)
    print("8. 수치형 컬럼 간 상관관계")
    print("=" * 70)
    if len(numeric_cols) < 2:
        print("상관관계를 계산할 수치형 컬럼이 2개 미만입니다.")
        print()
        return

    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(max(5, 0.6 * len(numeric_cols) + 2), max(4, 0.6 * len(numeric_cols) + 2)))
    sns.heatmap(corr, annot=len(numeric_cols) <= 15, fmt=".2f", cmap="coolwarm", center=0, ax=ax, square=True)
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()
    path = os.path.join(output_dir, "correlation_heatmap.png") if output_dir else None
    _save_or_show(fig, path, show)

    # 상관관계 높은 상위 쌍 출력
    corr_pairs = (
        corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .dropna()
        .sort_values(key=lambda s: s.abs(), ascending=False)
    )
    if not corr_pairs.empty:
        print("상관관계 절댓값 기준 상위 조합:")
        print(corr_pairs.head(10))
    print()


# --------------------------------------------------------------------------- #
# 메인 엔트리 포인트
# --------------------------------------------------------------------------- #
def analyze_dataframe(
    df: pd.DataFrame,
    output_dir: Optional[str] = "eda_output",
    show: bool = False,
    max_numeric_cols: int = 12,
    max_categorical_cols: int = 8,
) -> dict:
    """
    DataFrame 하나를 받아 기본 정보 출력 + 각종 시각화를 자동으로 수행한다.

    Parameters
    ----------
    df : pd.DataFrame
        분석 대상 데이터프레임.
    output_dir : str | None
        시각화 결과(png)를 저장할 디렉터리. None이면 저장하지 않음(콘솔/화면 출력만).
    show : bool
        True면 plt.show()로 화면에 표시 (Jupyter/로컬 환경용). 기본 False.
    max_numeric_cols, max_categorical_cols : int
        시각화할 최대 컬럼 수 (컬럼이 너무 많을 때 과도한 그림 생성을 방지).

    Returns
    -------
    dict
        분석 요약 정보 (shape, dtypes, missing 등)를 담은 딕셔너리.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df는 pandas.DataFrame이어야 합니다. 현재 타입: {type(df)}")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    numeric_cols, categorical_cols, datetime_cols = _split_columns(df)

    print_basic_info(df)
    plot_missing_values(df, output_dir, show)
    plot_numeric_distributions(df, numeric_cols, output_dir, show, max_cols=max_numeric_cols)
    plot_categorical_distributions(df, categorical_cols, output_dir, show, max_cols=max_categorical_cols)
    plot_correlation_heatmap(df, numeric_cols, output_dir, show)

    summary = {
        "shape": df.shape,
        "columns": list(df.columns),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
        "missing_total": int(df.isna().sum().sum()),
        "duplicated_rows": int(df.duplicated().sum()),
    }

    print("=" * 70)
    print("9. 요약")
    print("=" * 70)
    for k, v in summary.items():
        print(f"{k}: {v}")

    if output_dir:
        print(f"\n생성된 그래프는 '{output_dir}/' 폴더에 저장되었습니다.")

    return summary


# --------------------------------------------------------------------------- #
# 스크립트로 직접 실행 시 데모
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    rng = np.random.default_rng(42)
    n = 300
    demo_df = pd.DataFrame({
        "age": rng.normal(35, 10, n).round(1),
        "income": rng.exponential(50000, n).round(0),
        "score": rng.uniform(0, 100, n).round(2),
        "gender": rng.choice(["M", "F"], n),
        "city": rng.choice(["Seoul", "Busan", "Jeju", "Incheon"], n, p=[0.4, 0.3, 0.2, 0.1]),
        "signup_date": pd.date_range("2023-01-01", periods=n, freq="D"),
    })
    # 결측치 임의 삽입
    demo_df.loc[rng.choice(n, 20, replace=False), "income"] = np.nan
    demo_df.loc[rng.choice(n, 10, replace=False), "city"] = np.nan

    analyze_dataframe(demo_df, output_dir="/home/claude/eda_output_demo", show=False)