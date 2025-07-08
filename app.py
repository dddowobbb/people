import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (matplotlib)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 제목
st.title("양주2동 나이대별 인구 변화 추이")

# CSV 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("data/population.csv", encoding="utf-8")

    # 데이터 전처리
    data_rows = df.iloc[::2].reset_index(drop=True)
    header_rows = df.iloc[1::2].reset_index(drop=True)
    data_rows.columns = header_rows.iloc[0].values
    melted = data_rows.melt(var_name="연령", value_name="인구수")
    melted.dropna(inplace=True)
    melted["인구수"] = melted["인구수"].str.replace(",", "").astype(int)

    def parse_year_age(s):
        year_part, age_part = s.split("/")
        year = 2000 + int(year_part)
        return pd.Series([year, age_part])

    melted[["연도", "나이대"]] = melted["연령"].apply(parse_year_age)
    melted.drop(columns="연령", inplace=True)
    return melted

df = load_data()

# 나이대 선택
age_groups = df["나이대"].unique().tolist()
selected_ages = st.multiselect("보고 싶은 나이대를 선택하세요", age_groups, default=["0~4?", "5~9?"])

# 필터링
filtered_df = df[df["나이대"].isin(selected_ages)]

# 그래프 그리기
fig, ax = plt.subplots()
for age in selected_ages:
    group = filtered_df[filtered_df["나이대"] == age]
    ax.plot(group["연도"], group["인구수"], marker='o', label=age)

ax.set_xlabel("연도")
ax.set_ylabel("인구 수")
ax.set_title("양주2동 나이대별 인구 변화")
ax.legend()
st.pyplot(fig)
