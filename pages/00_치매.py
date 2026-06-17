import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import numpy as np

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
# 페이지 설정
# -------------------------------
st.set_page_config(page_title="알츠하이머 분석", layout="wide")
st.title("🧠 알츠하이머 환자들의 공통점 분석")
st.write("Alzheimer's Disease 데이터를 활용해 치매 환자(Diagnosis=1)와 "
         "정상인(Diagnosis=0)의 특징을 비교합니다.")

# -------------------------------
# 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("alzheimers_disease_data.csv")
    # 분석에 의미 없는 컬럼 제거
    df = df.drop(columns=["PatientID", "DoctorInCharge"], errors="ignore")
    return df

df = load_data()
TARGET = "Diagnosis"   # 결과 컬럼 (당뇨병의 Outcome에 해당)

# 분석할 숫자형 컬럼 한글 설명
col_desc = {
    "Age": "나이",
    "BMI": "체질량지수(BMI)",
    "AlcoholConsumption": "음주량",
    "PhysicalActivity": "신체 활동량",
    "DietQuality": "식습관 점수",
    "SleepQuality": "수면의 질",
    "SystolicBP": "수축기 혈압",
    "DiastolicBP": "이완기 혈압",
    "CholesterolTotal": "총 콜레스테롤",
    "CholesterolLDL": "LDL 콜레스테롤",
    "CholesterolHDL": "HDL 콜레스테롤",
    "CholesterolTriglycerides": "중성지방",
    "MMSE": "인지검사 점수(MMSE)",
    "FunctionalAssessment": "기능 평가 점수",
    "ADL": "일상생활 수행능력(ADL)",
}

patient = df[df[TARGET] == 1]
healthy = df[df[TARGET] == 0]

# -------------------------------
# 1. 데이터 미리보기
# -------------------------------
st.header("1️⃣ 데이터 미리보기")
st.dataframe(df.head())

c1, c2, c3 = st.columns(3)
c1.metric("전체 인원", f"{len(df)}명")
c2.metric("알츠하이머 환자", f"{len(patient)}명",
          f"{len(patient)/len(df)*100:.1f}%")
c3.metric("정상인", f"{len(healthy)}명",
          f"{len(healthy)/len(df)*100:.1f}%")

# -------------------------------
# 2. 두 그룹의 평균 비교 (차이 큰 순)
# -------------------------------
st.header("2️⃣ 알츠하이머 환자 vs 정상인 평균 비교")

analysis_cols = list(col_desc.keys())
mean_compare = df.groupby(TARGET)[analysis_cols].mean().T
mean_compare.columns = ["정상인(0)", "환자(1)"]
mean_compare["차이"] = mean_compare["환자(1)"] - mean_compare["정상인(0)"]

# 절댓값 기준 내림차순 정렬
mean_compare["차이_절댓값"] = mean_compare["차이"].abs()
mean_compare = mean_compare.sort_values("차이_절댓값", ascending=False)
mean_compare = mean_compare.drop(columns="차이_절댓값")

st.dataframe(mean_compare.style.format("{:.2f}"), use_container_width=True)

top_feature = mean_compare.index[0]
top_diff = mean_compare.loc[top_feature, "차이"]
top_desc = col_desc.get(top_feature, top_feature)

st.markdown(
    f"<h2 style='text-align:center; color:#8e44ad;'>"
    f"🔍 가장 큰 차이를 보이는 항목은<br>"
    f"<span style='font-size:1.5em;'>'{top_desc}'</span> 입니다!</h2>",
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='text-align:center; font-size:22px;'>"
    f"알츠하이머 환자가 정상인보다 평균적으로 "
    f"<b style='color:#8e44ad;'>{abs(top_diff):.2f} 만큼 "
    f"{'높습니다 ⬆️' if top_diff > 0 else '낮습니다 ⬇️'}</b></p>",
    unsafe_allow_html=True
)
st.info("💡 위쪽에 있을수록 두 그룹의 차이가 큰 항목이에요!")

# -------------------------------
# 3. 항목별 분포 비교
# -------------------------------
st.header("3️⃣ 항목별 분포 비교")
feature = st.selectbox(
    "비교하고 싶은 항목을 선택하세요",
    options=list(col_desc.keys()),
    format_func=lambda x: f"{x} ({col_desc[x]})"
)

left, center, right = st.columns([1, 3, 1])
with center:
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.histplot(data=df, x=feature, hue=TARGET,
                 kde=True, palette={0: "skyblue", 1: "salmon"}, ax=ax)
    ax.set_title(f"{col_desc[feature]} 분포", fontsize=11)
    ax.tick_params(labelsize=8)
    st.pyplot(fig, use_container_width=True)

m1, m2, m3 = st.columns(3)
h_mean = healthy[feature].mean()
p_mean = patient[feature].mean()
m1.metric("정상인 평균", f"{h_mean:.2f}")
m2.metric("환자 평균", f"{p_mean:.2f}", f"{p_mean - h_mean:+.2f}")
m3.metric("차이", f"{abs(p_mean - h_mean):.2f}")

# -------------------------------
# 4. 상관관계 히트맵
# -------------------------------
st.header("4️⃣ 항목 간 상관관계 히트맵")
st.write("Diagnosis(치매 여부)와 가장 관련이 깊은 항목을 찾아보세요.")

heatmap_cols = analysis_cols + [TARGET]
left2, center2, right2 = st.columns([1, 5, 1])
with center2:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.heatmap(df[heatmap_cols].corr(), annot=True, fmt=".2f",
                cmap="coolwarm", annot_kws={"size": 6}, ax=ax2)
    ax2.tick_params(labelsize=7)
    st.pyplot(fig2, use_container_width=True)

st.success("✅ MMSE(인지검사), ADL(일상생활능력) 등이 "
           "Diagnosis와 관련이 깊은지 확인해보세요!")
