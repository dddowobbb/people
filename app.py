import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.title("양주2동 나이대별 인구 변화 추이")

@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="utf-8")
    df = df.rename(columns={"Unnamed: 0": "연도"})

    # 쉼표 제거 및 숫자 변환 (문자열인 경우만)
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: int(str(x).replace(",", "")) if pd.notna(x) else 0)

    # wide → long 변환
    df_long = df.melt(id_vars=["연도"], var_name="나이대", value_name="인구수")
    df_long["연도"] = df_long["연도"].astype(int)
    return df_long


df = load_data()

# 나이대 선택
age_groups = sorted(df["나이대"].unique().tolist())
selected_ages = st.multiselect("보고 싶은 나이대를 선택하세요", age_groups, default=["0~4?"])

# 필터링
filtered_df = df[df["나이대"].isin(selected_ages)]

# 그래프
fig, ax = plt.subplots(figsize=(8, 5))
for age in selected_ages:
    group = filtered_df[filtered_df["나이대"] == age]
    ax.plot(group["연도"], group["인구수"], marker='o', label=age)

ax.set_xlabel("연도")
ax.set_ylabel("인구 수")
ax.set_title("양주2동 나이대별 인구 변화")
ax.legend()
ax.set_xticks(sorted(df["연도"].unique()))

st.pyplot(fig)
