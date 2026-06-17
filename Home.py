import streamlit as st

st.set_page_config(page_title="질병 데이터 분석", layout="wide")

st.title("🏥 질병 데이터 분석 프로젝트")
st.write("---")
st.header("환영합니다! 👋")
st.write("**왼쪽 사이드바**에서 분석하고 싶은 페이지를 선택하세요!")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🩺 당뇨병 분석")
    st.write("Pima Indians Diabetes 데이터로 환자와 정상인을 비교합니다.")
with col2:
    st.subheader("🧠 알츠하이머 분석")
    st.write("Alzheimer's Disease 데이터로 환자와 정상인을 비교합니다.")
