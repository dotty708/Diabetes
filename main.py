import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import numpy as np

# -------------------------------
# 데이터 전처리 함수
# -------------------------------
def preprocess_data(df):
    df = df.copy()
    cols_with_zero_missing = [
        "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"
    ]
    for col in cols_with_zero_missing:
        df[col] = df[col].replace(0, np.nan)
    for col in cols_with_zero_missing:
        df[col] = df.groupby("Outcome")[col].transform(
            lambda x: x.fillna(x.median())
        )
    return df

# -------------------------------
# 한글 폰트 설정
# -------------------------------
plt.rcParams['axes.unicode_minus'] = False
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
try:
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'NanumGothic'
except FileNotFoundError:
    pass
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------
# 페이지 기본 설정
# -------------------------------
st.set_page_config(page_title="당뇨병 환자 공통점 분석", layout="wide")
st.title("🩺 당뇨병 환자들의 공통점 분석")
st.write("Pima Indians Diabetes 데이터를 활용해 당뇨병 환자(Outcome=1)와 "
         "정상인(Outcome=0)의 특징을 비교합니다.")

# -------------------------------
# 데이터 불러오기 + 전처리
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("diabetes.csv")
    return df

df_raw = load_data()

# 사이드바: 전처리 선택
st.sidebar.header("⚙️ 설정")
use_preprocess = st.sidebar.checkbox("데이터 전처리 적용하기", value=True)
df = preprocess_data(df_raw) if use_preprocess else df_raw

col_desc = {
    "Pregnancies": "임신 횟수",
    "Glucose": "혈당 수치",
    "BloodPressure": "혈압",
    "SkinThickness": "피부 두께",
    "Insulin": "인슐린",
    "BMI": "체질량지수(BMI)",
    "DiabetesPedigreeFunction": "당뇨 유전 함수",
    "Age": "나이",
}

diabetic = df[df["Outcome"] == 1]
healthy = df[df["Outcome"] == 0]

# -------------------------------
# 1. 데이터 미리보기
# -------------------------------
st.header("1️⃣ 데이터 미리보기")
st.dataframe(df.head())

# ✅ 핵심 수치를 크게! (st.metric 활용)
col1, col2, col3 = st.columns(3)
col1.metric("전체 인원", f"{len(df)}명")
col2.metric("당뇨병 환자", f"{len(diabetic)}명",
            f"{len(diabetic)/len(df)*100:.1f}%")
col3.metric("정상인", f"{len(healthy)}명",
            f"{len(healthy)/len(df)*100:.1f}%")

# -------------------------------
# 2. 두 그룹의 평균 비교 (차이 큰 순 정렬)
# -------------------------------
st.header("2️⃣ 당뇨병 환자 vs 정상인 평균 비교")

mean_compare = df.groupby("Outcome").mean().T
mean_compare.columns = ["정상인(0)", "당뇨병(1)"]
mean_compare["차이"] = mean_compare["당뇨병(1)"] - mean_compare["정상인(0)"]

# ✅ 절댓값 기준 내림차순 정렬 (차이가 큰 요소가 위로!)
mean_compare["차이_절댓값"] = mean_compare["차이"].abs()
mean_compare = mean_compare.sort_values("차이_절댓값", ascending=False)
mean_compare = mean_compare.drop(columns="차이_절댓값")

st.dataframe(mean_compare.style.format("{:.2f}"), use_container_width=True)

# ✅ 가장 차이 큰 항목을 크고 직관적으로 강조!
top_feature = mean_compare.index[0]
top_diff = mean_compare.loc[top_feature, "차이"]
top_desc = col_desc.get(top_feature, top_feature)

st.markdown(
    f"<h2 style='text-align:center; color:#e74c3c;'>"
    f"🔍 가장 큰 차이를 보이는 항목은<br>"
    f"<span style='font-size:1.5em;'>'{top_desc}'</span> 입니다!"
    f"</h2>",
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='text-align:center; font-size:22px;'>"
    f"당뇨병 환자가 정상인보다 평균적으로 "
    f"<b style='color:#e74c3c;'>{abs(top_diff):.1f} 만큼 "
    f"{'높습니다 ⬆️' if top_diff > 0 else '낮습니다 ⬇️'}</b></p>",
    unsafe_allow_html=True
)

st.info("💡 위쪽에 있을수록 두 그룹의 차이가 큰 항목이에요. "
        "차이가 클수록 당뇨병과 관련이 깊을 가능성이 높아요!")

# -------------------------------
# 3. 항목별 분포 비교
# -------------------------------
st.header("3️⃣ 항목별 분포 비교")
feature = st.selectbox(
    "비교하고 싶은 항목을 선택하세요",
    options=list(col_desc.keys()),
    format_func=lambda x: f"{x} ({col_desc[x]})"
)

# ✅ 그래프를 가운데 컬럼에 배치해 크기 줄이기
left, center, right = st.columns([1, 3, 1])
with center:
    fig, ax = plt.subplots(figsize=(5, 3))   # ✅ figsize 축소
    sns.histplot(data=df, x=feature, hue="Outcome",
                 kde=True, palette={0: "skyblue", 1: "salmon"}, ax=ax)
    ax.set_title(f"{col_desc[feature]} 분포", fontsize=11)
    ax.tick_params(labelsize=8)
    st.pyplot(fig, use_container_width=True)

# ✅ 평균값을 metric으로 크게 비교
m1, m2, m3 = st.columns(3)
h_mean = healthy[feature].mean()
d_mean = diabetic[feature].mean()
m1.metric(f"정상인 평균", f"{h_mean:.1f}")
m2.metric(f"당뇨병 환자 평균", f"{d_mean:.1f}", f"{d_mean - h_mean:+.1f}")
m3.metric("차이", f"{abs(d_mean - h_mean):.1f}")

# -------------------------------
# 4. 상관관계 히트맵
# -------------------------------
st.header("4️⃣ 항목 간 상관관계 히트맵")
st.write("Outcome(당뇨 여부)과 가장 관련이 깊은 항목을 찾아보세요.")

# ✅ 히트맵도 가운데 컬럼에 배치해 크기 줄이기
left2, center2, right2 = st.columns([1, 4, 1])
with center2:
    fig2, ax2 = plt.subplots(figsize=(6, 5))   # ✅ figsize 축소
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm",
                annot_kws={"size": 7}, ax=ax2)
    ax2.tick_params(labelsize=8)
    st.pyplot(fig2, use_container_width=True)

st.success("✅ Glucose(혈당), BMI, Age 등이 Outcome과 "
           "높은 상관관계를 보이는지 확인해보세요!")
