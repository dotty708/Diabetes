import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 깨짐 방지 (스트림릿 클라우드에서는 영어 사용 권장)
plt.rcParams['axes.unicode_minus'] = False

# 나눔고딕 폰트 경로 지정
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
try:
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'NanumGothic'
except FileNotFoundError:
    pass  # 폰트가 없으면 기본값 사용
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------
# 페이지 기본 설정
# -------------------------------
st.set_page_config(page_title="당뇨병 환자 공통점 분석", layout="wide")
st.title("🩺 당뇨병 환자들의 공통점 분석")
st.write("Pima Indians Diabetes 데이터를 활용해 당뇨병 환자(Outcome=1)와 "
         "정상인(Outcome=0)의 특징을 비교합니다.")

# -------------------------------
# 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("diabetes.csv")
    return df

df = load_data()

# 컬럼 한글 설명
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

# -------------------------------
# 1. 데이터 미리보기
# -------------------------------
st.header("1️⃣ 데이터 미리보기")
st.dataframe(df.head())
st.write(f"전체 데이터 수: **{len(df)}명**")

diabetic = df[df["Outcome"] == 1]
healthy = df[df["Outcome"] == 0]
st.write(f"- 당뇨병 환자: **{len(diabetic)}명** "
         f"({len(diabetic)/len(df)*100:.1f}%)")
st.write(f"- 정상인: **{len(healthy)}명** "
         f"({len(healthy)/len(df)*100:.1f}%)")

# -------------------------------
# 2. 두 그룹의 평균 비교
# -------------------------------
st.header("2️⃣ 당뇨병 환자 vs 정상인 평균 비교")
mean_compare = df.groupby("Outcome").mean().T
mean_compare.columns = ["정상인(0)", "당뇨병(1)"]
mean_compare["차이"] = mean_compare["당뇨병(1)"] - mean_compare["정상인(0)"]
st.dataframe(mean_compare.style.format("{:.2f}"))

st.info("💡 '차이' 값이 클수록 당뇨병 환자에게서 두드러지는 특징이에요!")

# -------------------------------
# 3. 항목별 분포 비교 (사용자가 선택)
# -------------------------------
st.header("3️⃣ 항목별 분포 비교")
feature = st.selectbox(
    "비교하고 싶은 항목을 선택하세요",
    options=list(col_desc.keys()),
    format_func=lambda x: f"{x} ({col_desc[x]})"
)

fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(data=df, x=feature, hue="Outcome",
             kde=True, palette={0: "skyblue", 1: "salmon"}, ax=ax)
ax.set_title(f"{feature} ({col_desc[feature]}) Distribution")
ax.legend(title="Outcome", labels=["Diabetic(1)", "Healthy(0)"])
st.pyplot(fig)

# 평균값 안내
st.write(f"- 정상인 평균 {feature}: **{healthy[feature].mean():.1f}**")
st.write(f"- 당뇨병 환자 평균 {feature}: **{diabetic[feature].mean():.1f}**")

# -------------------------------
# 4. 상관관계 히트맵
# -------------------------------
st.header("4️⃣ 항목 간 상관관계 히트맵")
st.write("Outcome(당뇨 여부)과 가장 관련이 깊은 항목을 찾아보세요.")

fig2, ax2 = plt.subplots(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

st.success("✅ Glucose(혈당), BMI, Age 등이 Outcome과 "
           "높은 상관관계를 보이는지 확인해보세요!")
