import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Population Trend by Age Group - Yangju 2-dong")

@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="utf-8")
    df = df.rename(columns={"Unnamed: 0": "Year"})

    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: int(str(x).replace(",", "")) if pd.notna(x) else 0)

    df_long = df.melt(id_vars=["Year"], var_name="Age Group", value_name="Population")
    df_long["Year"] = df_long["Year"].astype(int)
    
    # Format year to last two digits
    df_long["Year (YY)"] = df_long["Year"].astype(str).str[-2:]
    return df_long

df = load_data()

# Age group selector
age_groups = sorted(df["Age Group"].unique())
selected_ages = st.multiselect("Select age group(s):", age_groups, default=["0~4?"])

# Filter data
filtered_df = df[df["Age Group"].isin(selected_ages)]

# Draw interactive line chart
fig = px.line(
    filtered_df,
    x="Year (YY)",
    y="Population",
    color="Age Group",
    markers=True,
    title="Population Change by Age Group (2008–2024)",
    labels={"Population": "Population", "Year (YY)": "Year"},
    hover_data={"Year": True, "Population": True}
)

st.plotly_chart(fig)
