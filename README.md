# 🧠 치매, 당뇨병 환자들 각각의 공통점이 무엇일까?

> Kaggle 데이터로 치매 환자들, 그리고 당뇨병 환자들 각각의 공통점이 무엇이고
> 정상인과 어떤 수치에서 어떠한 차이가 발생하는지 알아보는 **데이터 분석 프로젝트**

🔗 **배포 링크** : https://araboza-alzheimer.streamlit.app/

📊 **치매 데이터 출처** : https://www.kaggle.com/datasets/rabieelkharoua/alzheimers-disease-dataset

📊 **당뇨병 데이터 출처** : https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

---

## ❓ 우리가 발견한 문제

> 많은 이들이 두려워 하는 **치매, 당뇨병**이 어떠한 사람들에게 많이 나타날까요?
>
> 저희 팀은 치매, 당뇨병 환자들에게 나타나는 **공통적인 차이점**을 비교하여
> 이를 알아보려고 했습니다.

---

## 👥 우리 조원

| 학번 | 이름 |
|------|------|
| 20110 | 류정현 | 깃허브, 스트림릿, AI를 활용하여 웹앱 구성 |
| 20409 | 김지우 | 데이터 찾아오기 |


---

## 📊 사용한 데이터

### 1) 당뇨병 데이터 (Pima Indians Diabetes)
- **파일명**: `diabetes.csv`
- **데이터 수**: 768명
- **주요 컬럼**: 혈당(Glucose), 혈압(BloodPressure), BMI, 나이(Age) 등 8개 지표
- **결과 컬럼**: `Outcome` (0 = 정상, 1 = 당뇨병)

### 2) 알츠하이머 데이터 (Alzheimer's Disease Data)
- **파일명**: `alzheimers_disease_data.csv`
- **데이터 수**: 2,149명
- **주요 컬럼**: 인지검사(MMSE), 기능평가(FunctionalAssessment),
  일상생활능력(ADL), 콜레스테롤, 혈압 등 30여 개 지표
- **결과 컬럼**: `Diagnosis` (0 = 정상, 1 = 알츠하이머)

---

## 🛠️ 사용 기술
- **Streamlit** : 웹앱 제작 및 배포
- **Pandas** : 데이터 처리 및 전처리
- **Matplotlib / Seaborn** : 데이터 시각화
- **NumPy** : 수치 계산

---

## 🚀 실행 방법
```bash
# 1. 필요한 라이브러리 설치
pip install -r requirements.txt

# 2. 앱 실행
streamlit run Home.py
