import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ 한글 폰트 설정 (로컬에서는 잘 작동, Cloud는 시스템 폰트 따라 다를 수 있음)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.title("양주2동 나이대별 인구 변화 추이")

# ✅ 데이터 전처리 함수
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="utf-8")

    all_records = []

    # 짝수행: 값 / 홀수행: 열 이름
    for i in range(0, len(df), 2):
        value_row = df.iloc[i]
        header_row = df.iloc[i + 1]

        # 열 이름을 해당 행의 값으로 설정
        value_row.index = header_row.values

        # 각 열을 연도/나이대로 분해하고 값 추출
        for col, val in zip(value_row.index, value_row.values):
            if "/" not in col or pd.isna(val):
                continue
            try:
                year_part, age_range = col.split("/")
                year = 2000 + int(year_part)
                count = int(str(val).replace(",", ""))
                all_records.append({"연도": year, "나이대": age_range, "인구수": count})
            except:
                continue

    return pd.DataFrame(all_records)

# ✅ 데이터 로딩
df = load_data()

# ✅ 유저 선택: 나이대
age_groups = sorted(df["나이대"].unique().tolist())
selected_ages = st.multiselect("보고 싶은 나이대를 선택하세요", age_groups, default=["0~4?"])

# ✅ 선택된 나이대만 필터링
filtered_df = df[df["나이대"].isin(selected_ages)]

# ✅ 꺾은선 그래프 그리기
fig, ax = plt.subplots(figsize=(8, 5))

for age in selected_ages:
    group = filtered_df[filtered_df["나이대"] == age]
    group = group.sort_values("연도")
    ax.plot(group["연도"], group["인구수"], marker='o', label=age)

ax.set_xlabel("연도")
ax.set_ylabel("인구 수")
ax.set_title("양주2동 나이대별 인구 변화")
ax.legend()
ax.set_xticks(sorted(df["연도"].unique()))  # 연도 눈금 지정

st.pyplot(fig)

