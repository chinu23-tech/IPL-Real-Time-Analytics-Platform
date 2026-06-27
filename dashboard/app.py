import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="IPL Live Analytics Platform",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🏏 IPL Analytics")
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Team Analysis", "Live Match Center", "About"]
)

# -----------------------------
# HEADER
# -----------------------------
st.title("🏏 IPL Live Analytics Platform")
st.markdown("### Powered by Snowflake Cloud | TCS Xcelerate Project")

st.divider()

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Ball Records", "283,678")

with col2:
    st.metric("🏏 Teams", "19")

with col3:
    st.metric("📅 Seasons", "18")

with col4:
    st.metric("⚡ Total Runs", "4,50,000+")

st.divider()

# -----------------------------
# OVERVIEW PAGE
# -----------------------------
if page == "Overview":

    st.subheader("📈 Team Performance")

    team_runs = pd.DataFrame({
        "Team": [
            "Mumbai Indians",
            "Kolkata Knight Riders",
            "Chennai Super Kings",
            "Rajasthan Royals",
            "Royal Challengers Bangalore"
        ],
        "Runs": [
            46014,
            42080,
            42017,
            38210,
            37692
        ]
    })

    fig = px.bar(
        team_runs,
        x="Team",
        y="Runs",
        text="Runs",
        title="Top Teams by Total Runs"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Team Run Share")

    pie = px.pie(
        team_runs,
        names="Team",
        values="Runs",
        hole=0.4
    )

    st.plotly_chart(pie, use_container_width=True)

# -----------------------------
# TEAM ANALYSIS
# -----------------------------
elif page == "Team Analysis":

    st.subheader("🏆 Top Teams")

    st.dataframe(team_runs)

# -----------------------------
# LIVE MATCH CENTER
# -----------------------------
elif page == "Live Match Center":

    st.subheader("⚡ Live Match Simulator")

    st.metric("Current Score", "128/3")

    st.metric("Current Over", "15.2")

    st.metric("Run Rate", "8.35")

    st.success("Last Ball: FOUR!")

    st.markdown("### Recent Balls")

    st.write("1 | 4 | 0 | W | 2 | 6")

# -----------------------------
# ABOUT PAGE
# -----------------------------
else:

    st.subheader("ℹ About Project")

    st.write("""
    This project demonstrates:

    - Snowflake Data Warehouse
    - RAW / SILVER / GOLD Architecture
    - IPL Historical Analytics
    - Match Replay Simulator
    - Interactive Dashboard

    Developed as part of TCS Xcelerate.
    """)