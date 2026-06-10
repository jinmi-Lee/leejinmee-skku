import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Korean Variety Show Trend Dashboard",
    page_icon="📺",
    layout="wide"
)

# -----------------------------
# Sample Data
# -----------------------------
data = pd.DataFrame({
    "Show": [
        "Running Man", "Knowing Bros", "I Live Alone", "You Quiz on the Block",
        "2 Days & 1 Night", "Running Man", "Knowing Bros", "I Live Alone",
        "You Quiz on the Block", "2 Days & 1 Night"
    ],
    "Platform": [
        "YouTube", "YouTube", "TV", "YouTube", "TV",
        "Social Media", "Social Media", "YouTube", "TV", "YouTube"
    ],
    "Cast Member": [
        "Yoo Jae-suk", "Kang Ho-dong", "Park Na-rae", "Yoo Jae-suk",
        "Kim Jong-min", "Haha", "Lee Soo-geun", "Kian84",
        "Jo Se-ho", "DinDin"
    ],
    "Year": [2023, 2023, 2023, 2023, 2023, 2024, 2024, 2024, 2024, 2024],
    "Views": [1200000, 950000, 880000, 1100000, 720000, 1500000, 1050000, 980000, 1300000, 760000],
    "Likes": [85000, 62000, 54000, 77000, 43000, 98000, 69000, 60000, 90000, 45000],
    "Comments": [12000, 8800, 7600, 10300, 5200, 15000, 9700, 8100, 13000, 5600],
    "Popularity Score": [92, 84, 78, 88, 70, 96, 86, 81, 91, 73],
    "Keyword": [
        "legend episode", "funny talk", "daily life", "celebrity interview", "travel",
        "meme", "reaction", "healing", "trend", "challenge"
    ]
})

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📌 Filter Collection")

show_filter = st.sidebar.multiselect(
    "Select Variety Shows",
    options=data["Show"].unique(),
    default=data["Show"].unique()
)

platform_filter = st.sidebar.multiselect(
    "Select Platform",
    options=data["Platform"].unique(),
    default=data["Platform"].unique()
)

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=data["Year"].unique(),
    default=data["Year"].unique()
)

filtered_data = data[
    (data["Show"].isin(show_filter)) &
    (data["Platform"].isin(platform_filter)) &
    (data["Year"].isin(year_filter))
]

# -----------------------------
# Header
# -----------------------------
st.title("📺 Korean Variety Show Trend Dashboard")
st.write("Film and Media · SKKU · AI & Data Visualization Project")

st.markdown("""
This Streamlit dashboard analyzes the popularity, audience engagement, and online trends of Korean variety shows.
It focuses on how Korean variety content becomes popular through YouTube, social media, and online communities.
""")

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Shows", filtered_data["Show"].nunique())
col2.metric("Total Views", f"{filtered_data['Views'].sum():,}")
col3.metric("Total Likes", f"{filtered_data['Likes'].sum():,}")
col4.metric("Avg Popularity", round(filtered_data["Popularity Score"].mean(), 1))

st.divider()

# -----------------------------
# Popularity Trend
# -----------------------------
st.header("01 — Popularity Trend Analysis")

trend_fig = px.line(
    filtered_data,
    x="Year",
    y="Popularity Score",
    color="Show",
    markers=True,
    title="Popularity Score Changes Over Time"
)
st.plotly_chart(trend_fig, use_container_width=True)

# -----------------------------
# Cast Ranking
# -----------------------------
st.header("02 — Cast Member Ranking")

ranking_data = filtered_data.groupby("Cast Member", as_index=False)["Popularity Score"].mean()
ranking_data = ranking_data.sort_values("Popularity Score", ascending=False)

ranking_fig = px.bar(
    ranking_data,
    x="Popularity Score",
    y="Cast Member",
    orientation="h",
    title="Cast Member Popularity Ranking"
)
st.plotly_chart(ranking_fig, use_container_width=True)

# -----------------------------
# Keyword Analysis
# -----------------------------
st.header("03 — Keyword & Meme Analysis")

keyword_data = filtered_data["Keyword"].value_counts().reset_index()
keyword_data.columns = ["Keyword", "Frequency"]

keyword_fig = px.bar(
    keyword_data,
    x="Keyword",
    y="Frequency",
    title="Trending Keywords and Memes"
)
st.plotly_chart(keyword_fig, use_container_width=True)

# -----------------------------
# Viewer Engagement
# -----------------------------
st.header("04 — Viewer Engagement Analysis")

engagement_data = filtered_data.groupby("Show", as_index=False)[["Views", "Likes", "Comments"]].sum()

engagement_fig = px.bar(
    engagement_data,
    x="Show",
    y=["Views", "Likes", "Comments"],
    barmode="group",
    title="Views, Likes, and Comments by Show"
)
st.plotly_chart(engagement_fig, use_container_width=True)

# -----------------------------
# Show Comparison
# -----------------------------
st.header("05 — Interactive Show Comparison")

comparison_fig = px.scatter(
    filtered_data,
    x="Views",
    y="Likes",
    size="Comments",
    color="Show",
    hover_data=["Cast Member", "Platform", "Keyword"],
    title="Show Comparison: Views vs Likes"
)
st.plotly_chart(comparison_fig, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------
st.header("06 — Raw Data")
st.dataframe(filtered_data, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.write("Built with Python, Streamlit, Pandas, Plotly, and AI-generated code.")
