import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import snowflake.connector

# #############################################
# AUTO-REFRESH
# #############################################
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=3000, key="live_refresh")
except Exception:
    pass

# #############################################
# PAGE CONFIG
# #############################################
st.set_page_config(
    page_title="IPL Live Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# #############################################
# GLOBAL CSS  — IPL Broadcast Dark Theme
# #############################################
st.markdown("""
<style>
/* ---------- FONTS ---------- */
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Inter:wght@300;400;500;600&display=swap');

/* ---------- BASE ---------- */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background: #080c18 !important;
    border-right: 1px solid #1e2540;
}
[data-testid="stSidebar"] .stRadio label {
    color: #a0a8c0 !important;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 15px;
    letter-spacing: 0.04em;
}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label {
    color: #ffd700 !important;
}
.block-container { padding: 1.4rem 2rem 2rem 2rem !important; }
h1, h2, h3, h4 { font-family: 'Barlow Condensed', sans-serif !important; }

/* ---------- SIDEBAR LOGO ---------- */
.sidebar-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 26px;
    font-weight: 900;
    color: #ffd700;
    letter-spacing: 0.06em;
    padding: 0.8rem 0 1.2rem 0;
    text-align: center;
    border-bottom: 1px solid #1e2540;
    margin-bottom: 1.2rem;
}

/* ---------- SECTION HEADER ---------- */
.section-header {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #ffd700;
    border-left: 4px solid #ffd700;
    padding-left: 10px;
    margin: 1.4rem 0 0.9rem 0;
}
.section-sub {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8892b0;
    margin: 1rem 0 0.5rem 0;
}

/* ---------- SCORECARD ---------- */
.score-card {
    background: linear-gradient(135deg, #0d1429 0%, #131b35 100%);
    border: 1px solid #1e2c50;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    text-align: center;
}
.score-card .label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a6480;
    margin-bottom: 6px;
}
.score-card .value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 36px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1;
}
.score-card .sub {
    font-size: 12px;
    color: #5a6480;
    margin-top: 4px;
}
.score-card.accent .value { color: #ffd700; }
.score-card.green  .value { color: #4cef9f; }

/* ---------- TEAM BADGE ---------- */
.team-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 14px;
    font-weight: 900;
    flex-shrink: 0;
}

/* ---------- PLAYER CARD ---------- */
.player-card {
    background: #0d1429;
    border: 1px solid #1e2540;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.6rem;
}
.player-card .player-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #e0e6ff;
}
.player-card .player-stat {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px;
    font-weight: 900;
    color: #ffd700;
    margin-left: auto;
}
.player-card .player-detail {
    font-size: 12px;
    color: #5a6480;
    margin-top: 2px;
}

/* ---------- BALL CHIP ---------- */
.ball-chip {
    width: 46px; height: 46px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px; font-weight: 900;
    margin: auto;
}
.ball-w  { background: #7f1d1d; color: #fca5a5; border: 2px solid #ef4444; }
.ball-4  { background: #14532d; color: #86efac; border: 2px solid #22c55e; }
.ball-6  { background: #1e3a5f; color: #93c5fd; border: 2px solid #3b82f6; }
.ball-0  { background: #1e2540; color: #475569; border: 2px solid #334155; }
.ball-n  { background: #1c1f30; color: #e0e6ff; border: 2px solid #334155; }

/* ---------- POINTS TABLE ---------- */
.pts-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.pts-table th {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5a6480;
    padding: 10px 12px;
    border-bottom: 1px solid #1e2540;
    text-align: left;
}
.pts-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #111827;
    color: #c8d0e8;
    vertical-align: middle;
}
.pts-table tr:hover td { background: #0f1628; }
.pts-table .qualified td { color: #ffd700; }
.pts-table .pts-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #ffd700;
}
.pts-table .rank-badge {
    display: inline-block;
    width: 24px; height: 24px;
    border-radius: 50%;
    text-align: center; line-height: 24px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 13px; font-weight: 700;
}
.rank-1 { background: #ffd700; color: #000; }
.rank-2 { background: #c0c0c0; color: #000; }
.rank-3 { background: #cd7f32; color: #fff; }
.rank-4 { background: #1e2540; color: #a0a8c0; }
.rank-n { background: #0d1020; color: #5a6480; }

/* ---------- PLAYOFF BRACKET ---------- */
.bracket-card {
    background: #0d1429;
    border: 1px solid #1e2540;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.bracket-card .round-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5a6480;
    margin-bottom: 8px;
}
.bracket-card .team-a {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 19px;
    font-weight: 700;
    color: #e0e6ff;
}
.bracket-card .vs { color: #5a6480; font-size: 12px; margin: 3px 0; }
.bracket-card .team-b {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 19px;
    font-weight: 700;
    color: #e0e6ff;
}
.bracket-card .result {
    font-size: 12px;
    color: #4cef9f;
    margin-top: 6px;
}

/* ---------- CHAMPION BANNER ---------- */
.champion-banner {
    background: linear-gradient(135deg, #1a1200 0%, #2a1e00 50%, #1a1200 100%);
    border: 2px solid #ffd700;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
}
.champion-banner .trophy { font-size: 52px; margin-bottom: 0.4rem; }
.champion-banner .title {
    font-size: 13px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #a08020;
}
.champion-banner .team {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 48px;
    font-weight: 900;
    color: #ffd700;
    line-height: 1.1;
}

/* ---------- AWARD CARD ---------- */
.award-card {
    background: #0d1429;
    border: 1px solid #1e2540;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 0.5rem;
}
.award-card .rnk {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px;
    font-weight: 900;
    color: #2a3050;
    width: 28px;
    text-align: center;
    flex-shrink: 0;
}
.award-card .rnk.top { color: #ffd700; }
.award-card .name { flex: 1; }
.award-card .pname {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #e0e6ff;
}
.award-card .team-tag {
    font-size: 11px;
    color: #5a6480;
}
.award-card .stat {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 26px;
    font-weight: 900;
}
.stat-orange { color: #f97316; }
.stat-purple { color: #a855f7; }

/* ---------- RESULT CARD ---------- */
.result-card {
    background: #0d1429;
    border: 1px solid #1e2540;
    border-radius: 10px;
    padding: 1.2rem 1.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    margin-bottom: 0.8rem;
}

/* ---------- PROGRESS BAR ---------- */
.prob-bar-wrap {
    background: #1e2540;
    border-radius: 999px;
    height: 14px;
    overflow: hidden;
    margin: 0.6rem 0;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #16a34a, #4cef9f);
    transition: width 0.6s ease;
}

/* ---------- LIVE DOT ---------- */
.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #7f1d1d;
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #fca5a5;
}
.live-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #ef4444;
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ---------- DIVIDER ---------- */
hr.ipl-divider {
    border: none;
    border-top: 1px solid #1e2540;
    margin: 1.2rem 0;
}

/* ---------- HIDE STREAMLIT CHROME ---------- */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# #############################################
# TEAM META
# #############################################
TEAM_META = {
    "MI":{"abbr":"MI","bg":"#004BA0","fg":"white"},
    "CSK":{"abbr":"CSK","bg":"#FDB913","fg":"black"},
    "RCB":{"abbr":"RCB","bg":"#EC1C24","fg":"white"},
    "KKR":{"abbr":"KKR","bg":"#3A225D","fg":"white"},
    "GT":{"abbr":"GT","bg":"#1C4170","fg":"white"},
    "LSG":{"abbr":"LSG","bg":"#A72056","fg":"white"},
    "DC":{"abbr":"DC","bg":"#17479E","fg":"white"},
    "RR":{"abbr":"RR","bg":"#EA1A85","fg":"white"},
    "PBKS":{"abbr":"PBKS","bg":"#AA4545","fg":"white"},
    "SRH":{"abbr":"SRH","bg":"#F26D21","fg":"white"}
}

def team_badge(team_name, size=44):
    meta = TEAM_META.get(team_name, {"abbr": team_name[:2].upper(), "bg": "#1e2540", "fg": "#e0e6ff"})
    return (
        f'<span class="team-badge" '
        f'style="background:{meta["bg"]};color:{meta["fg"]};width:{size}px;height:{size}px;font-size:{max(10, size//3)}px;">'
        f'{meta["abbr"]}</span>'
    )

# #############################################
# SNOWFLAKE CONNECTION
# #############################################
@st.cache_resource
def get_conn():
    return snowflake.connector.connect(
        account="PJGGWMP-ZH63080",
        user="CHINU6371",
        password="6371486849@Chinu",
        warehouse="COMPUTE_WH",
        database="CRICKET_DB",
        role="ACCOUNTADMIN",
    )

conn = get_conn()

# #############################################
# SIDEBAR
# #############################################
st.sidebar.markdown('<div class="sidebar-brand">🏏 IPL LIVE</div>', unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigate",
    ["Live Match", "Points Table", "Playoffs", "Awards", "Analytics", "Match Results"],
    label_visibility="collapsed",
)

# #############################################
# DATA LOADING
# #############################################
@st.cache_data(ttl=3)
def load_data():
    def q(sql):
        try:
            return pd.read_sql(sql, conn)
        except Exception:
            return pd.DataFrame()

    return {
        "current_ball":  q("SELECT * FROM GOLD.CURRENT_BALL"),
        "points_table":  q("SELECT * FROM GOLD.POINTS_TABLE_LIVE"),
        "playoffs":      q("SELECT * FROM GOLD.PLAYOFFS_LIVE"),
        "champion":      q("SELECT * FROM GOLD.CHAMPION_LIVE"),
        "orange_cap":    q("SELECT * FROM GOLD.ORANGE_CAP_LIVE ORDER BY TOTAL_RUNS DESC LIMIT 10"),
        "purple_cap":    q("SELECT * FROM GOLD.PURPLE_CAP_LIVE ORDER BY WICKETS DESC LIMIT 10"),
        "team_runs":     q("SELECT * FROM GOLD.TEAM_RUNS_LIVE"),
        "match_results": q("SELECT * FROM GOLD.MATCH_RESULTS_LIVE ORDER BY MATCH_ID DESC"),
        "live_batters":  q("SELECT * FROM GOLD.LIVE_BATTERS"),
        "live_bowlers":  q("SELECT * FROM GOLD.LIVE_BOWLERS"),
        "last_over":     q("SELECT * FROM GOLD.LAST_OVER"),
    }

data = load_data()

# #############################################################################
# PAGE 1 — LIVE MATCH
# #############################################################################
if page == "Live Match":

    current_ball  = data["current_ball"]
    live_batters  = data["live_batters"]
    live_bowlers  = data["live_bowlers"]
    last_over     = data["last_over"]

    st.markdown(
        '<div style="display:flex;align-items:center;gap:12px;margin-bottom:0.2rem;">'
        '<span class="live-pill"><span class="live-dot"></span>LIVE</span>'
        '<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:24px;font-weight:700;color:#e0e6ff;">Match Centre</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not current_ball.empty:
        ball = current_ball.iloc[0]
        overs = ball["OVER_NO"] + (ball["BALL_NO"] / 6)
        crr = round(ball["SCORE"] / overs, 2) if overs > 0 else 0.0
        projected = round(crr * 20, 0)

        # ── SCORECARDS ──────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        cards = [
            (c1, "BATTING", ball["BATTING_TEAM"], f'{team_badge(ball["BATTING_TEAM"], 28)} {ball["BATTING_TEAM"]}', ""),
            (c2, "SCORE",   f'{ball["SCORE"]}/{ball["WICKETS"]}', "", "accent"),
            (c3, "OVERS",   f'{ball["OVER_NO"]}.{ball["BALL_NO"]}', "/20", ""),
            (c4, "CRR",     crr, "", "green"),
            (c5, "PROJECTED", int(projected), "runs", ""),
        ]
        for col, label, val, sub, cls in cards:
            with col:
                st.markdown(
                    f'<div class="score-card {cls}">'
                    f'<div class="label">{label}</div>'
                    f'<div class="value">{val}</div>'
                    f'<div class="sub">{sub}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)

        # ── BATTING + BOWLING ────────────────────────
        left, right = st.columns([3, 2])

        with left:
            st.markdown('<div class="section-header">🏏 At The Crease</div>', unsafe_allow_html=True)
            for _, row in live_batters.head(2).iterrows():
                sr = round((row["RUNS"] / row["BALLS"]) * 100, 1) if row["BALLS"] > 0 else 0
                st.markdown(
                    f'<div class="player-card">'
                    f'{team_badge(ball["BATTING_TEAM"], 38)}'
                    f'<div class="name"><div class="player-name">{row["STRIKER"]}</div>'
                    f'<div class="player-detail">{row["BALLS"]} balls &nbsp;|&nbsp; SR {sr}</div></div>'
                    f'<div class="player-stat">{row["RUNS"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        with right:
            st.markdown('<div class="section-header">🎯 Bowling</div>', unsafe_allow_html=True)
            if not live_bowlers.empty:
                for _, row in live_bowlers.head(2).iterrows():
                    st.markdown(
                        f'<div class="player-card">'
                        f'{team_badge(ball["BOWLING_TEAM"], 38)}'
                        f'<div class="name"><div class="player-name">{row["BOWLER"]}</div>'
                        f'<div class="player-detail">{row["OVERS"]} overs &nbsp;|&nbsp; Econ {row["ECONOMY"]}</div></div>'
                        f'<div class="player-stat" style="color:#c084fc;">{row["WICKETS"]}/{row["RUNS_GIVEN"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)

        # ── LAST OVER ────────────────────────────────
        st.markdown('<div class="section-header">🔴 Last Over</div>', unsafe_allow_html=True)
        ball_cols = st.columns(6)
        for i, (_, row) in enumerate(last_over.iterrows()):
            res = str(row["BALL_RESULT"])
            if res == "W":   chip_cls, label = "ball-w", "W"
            elif res == "4": chip_cls, label = "ball-4", "4"
            elif res == "6": chip_cls, label = "ball-6", "6"
            elif res == "0": chip_cls, label = "ball-0", "•"
            else:             chip_cls, label = "ball-n", res
            with ball_cols[i % 6]:
                st.markdown(
                    f'<div class="ball-chip {chip_cls}">{label}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)

        # ── WIN PROBABILITY ───────────────────────────
        st.markdown('<div class="section-header">📊 Win Probability</div>', unsafe_allow_html=True)
        bat_prob = min(95, max(5, round((ball["SCORE"] / 300) * 100)))
        bowl_prob = 100 - bat_prob

        st.markdown(
            f'<div style="display:flex;justify-content:space-between;font-family:\'Barlow Condensed\',sans-serif;font-size:14px;font-weight:600;margin-bottom:4px;">'
            f'<span style="color:#4cef9f;">{ball["BATTING_TEAM"]}  {bat_prob}%</span>'
            f'<span style="color:#f87171;">{ball["BOWLING_TEAM"]}  {bowl_prob}%</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="prob-bar-wrap"><div class="prob-bar-fill" style="width:{bat_prob}%;"></div></div>',
            unsafe_allow_html=True,
        )

        # ── WIN PROB GAUGE (Plotly) ───────────────────
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bat_prob,
            number={"suffix": "%", "font": {"color": "#ffd700", "size": 36, "family": "Barlow Condensed"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#334155", "tickfont": {"color": "#5a6480"}},
                "bar": {"color": "#4cef9f"},
                "bgcolor": "#0d1429",
                "bordercolor": "#1e2540",
                "steps": [
                    {"range": [0, 40],  "color": "#1a0a0a"},
                    {"range": [40, 60], "color": "#1a1a0a"},
                    {"range": [60, 100],"color": "#0a1a0a"},
                ],
                "threshold": {"line": {"color": "#ffd700", "width": 2}, "thickness": 0.75, "value": bat_prob},
            },
        ))
        fig.update_layout(
            height=220,
            margin=dict(l=20, r=20, t=30, b=10),
            paper_bgcolor="#0a0e1a",
            font_color="#e8eaf0",
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No live match data available. Check back soon.")


# #############################################################################
# PAGE 2 — POINTS TABLE
# #############################################################################
elif page == "Points Table":

    points_table = data["points_table"]

    st.markdown('<div class="section-header" style="margin-top:0">🏆 Points Table</div>', unsafe_allow_html=True)

    if not points_table.empty:
        # ── Qualified cards ───────────────────────────
        qualified = points_table.head(4)
        q_cols = st.columns(4)
        rank_labels = ["1st", "2nd", "3rd", "4th"]
        for i, (_, row) in enumerate(qualified.iterrows()):
            with q_cols[i]:
                meta = TEAM_META.get(row["TEAM"], {"abbr": row["TEAM"][:2].upper(), "bg": "#1e2540", "fg": "#e0e6ff"})
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{meta["bg"]}22,{meta["bg"]}11);'
                    f'border:1px solid {meta["bg"]}66;border-radius:10px;padding:1rem;text-align:center;">'
                    f'<div style="font-size:11px;letter-spacing:0.12em;color:#5a6480;margin-bottom:6px;">{rank_labels[i]} PLACE</div>'
                    f'<span class="team-badge" style="background:{meta["bg"]};color:{meta["fg"]};font-size:18px;width:50px;height:50px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;font-family:\'Barlow Condensed\',sans-serif;font-weight:900;">{meta["abbr"]}</span>'
                    f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:16px;font-weight:700;color:#e0e6ff;margin-top:8px;">{row["TEAM"]}</div>'
                    f'<div style="font-family:\'Barlow Condensed\',sans-serif;font-size:28px;font-weight:900;color:#ffd700;">{row.get("PTS", row.get("POINTS",""))}</div>'
                    f'<div style="font-size:11px;color:#5a6480;">POINTS</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)

        # ── Full styled table ─────────────────────────
        cols = list(points_table.columns)
        header_html = "".join(f"<th>{c}</th>" for c in cols)
        rows_html = ""
        for i, (_, row) in enumerate(points_table.iterrows()):
            rank_class = f"rank-{i+1}" if i < 4 else "rank-n"
            qualified_cls = "qualified" if i < 4 else ""
            rank_badge = f'<span class="rank-badge {rank_class}">{i+1}</span>'
            cells = ""
            for j, col in enumerate(cols):
                val = row[col]
                if j == 0:
                    meta = TEAM_META.get(str(val), {"abbr": str(val)[:2].upper(), "bg": "#1e2540", "fg": "#e0e6ff"})
                    cells += (
                        f'<td style="display:flex;align-items:center;gap:8px;">'
                        f'{rank_badge}'
                        f'<span class="team-badge" style="background:{meta["bg"]};color:{meta["fg"]};width:30px;height:30px;font-size:11px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;font-family:\'Barlow Condensed\',sans-serif;font-weight:900;">{meta["abbr"]}</span>'
                        f'{val}</td>'
                    )
                elif str(col).upper() in ("PTS", "POINTS", "PT"):
                    cells += f'<td><span class="pts-val">{val}</span></td>'
                else:
                    cells += f'<td>{val}</td>'
            rows_html += f'<tr class="{qualified_cls}">{cells}</tr>'

        st.markdown(
            f'<table class="pts-table"><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Points table not available.")


# #############################################################################
# PAGE 3 — PLAYOFFS
# #############################################################################
elif page == "Playoffs":

    playoffs = data["playoffs"]
    champion = data["champion"]

    st.markdown(
        '<div class="section-header" style="margin-top:0">🥇 Playoff Bracket</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------
    # PLAYOFFS
    # ---------------------------------

    if playoffs.empty:
        st.info("🏏 Tournament In Progress")
    else:
        cols_needed = min(len(playoffs), 4)
        bracket_cols = st.columns(cols_needed)

        for i, (_, row) in enumerate(playoffs.iterrows()):
            with bracket_cols[i % cols_needed]:
                round_name = row.get("ROUND", row.get("STAGE", f"Match {i+1}"))
                team_a = row.get("TEAM1", row.get("TEAM_A", "TBD"))
                team_b = row.get("TEAM2", row.get("TEAM_B", "TBD"))
                result = row.get("WINNER", row.get("RESULT", ""))

                st.markdown(
                    f'<div class="bracket-card">'
                    f'<div class="round-label">{round_name}</div>'
                    f'<div class="team-a">{team_badge(str(team_a),26)} {team_a}</div>'
                    f'<div class="vs">vs</div>'
                    f'<div class="team-b">{team_badge(str(team_b),26)} {team_b}</div>'
                    f'{"<div class=\'result\'>🏆 " + str(result) + "</div>" if result else ""}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.markdown(
        '<hr class="ipl-divider">',
        unsafe_allow_html=True
    )

    # ---------------------------------
    # CHAMPION
    # ---------------------------------

    st.markdown(
        '<div class="section-header">👑 IPL Champion</div>',
        unsafe_allow_html=True
    )

    if champion.empty:
        st.info("🏏 Tournament In Progress")
    else:
        champ_name = champion.iloc[0]["CHAMPION"]
        if champ_name == "Tournament In Progress":
            st.info("🏏 Tournament In Progress")
        else:
            st.markdown(
                f'<div class="champion-banner">'
                f'<div class="trophy">🏆</div>'
                f'<div class="title">Champions</div>'
                f'<div class="team">{champ_name}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# #############################################################################
# PAGE 4 — AWARDS
# #############################################################################
elif page == "Awards":

    orange_cap = data["orange_cap"]
    purple_cap = data["purple_cap"]

    st.markdown('<div class="section-header" style="margin-top:0">🏅 Season Awards</div>', unsafe_allow_html=True)

    col_o, col_p = st.columns(2)

    # ── Orange Cap ──────────────────────────────
    with col_o:
        st.markdown('<div class="section-sub">🟠 Orange Cap — Top Run Scorers</div>', unsafe_allow_html=True)
        if not orange_cap.empty:
            for i, (_, row) in enumerate(orange_cap.iterrows()):
                player_col = next((c for c in row.index if "PLAYER" in c.upper() or "BATTER" in c.upper() or "NAME" in c.upper()), orange_cap.columns[0])
                runs_col   = next((c for c in row.index if "RUN" in c.upper()), orange_cap.columns[1])
                team_col   = next((c for c in row.index if "TEAM" in c.upper()), None)
                team_tag   = f'<div class="team-tag">{row[team_col]}</div>' if team_col else ""
                rnk_cls    = "top" if i == 0 else ""
                st.markdown(
                    f'<div class="award-card">'
                    f'<div class="rnk {rnk_cls}">{i+1}</div>'
                    f'<div class="name"><div class="pname">{row[player_col]}</div>{team_tag}</div>'
                    f'<div class="stat stat-orange">{row[runs_col]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with st.expander("📊 Runs Distribution Chart"):
                fig = px.bar(
                    orange_cap,
                    x=orange_cap.columns[0],
                    y=orange_cap.columns[1],
                    color_discrete_sequence=["#f97316"],
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="#0a0e1a",
                    plot_bgcolor="#0d1429",
                    font_color="#e8eaf0",
                    xaxis_title="",
                    yaxis_title="Runs",
                    showlegend=False,
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=60),
                )
                fig.update_xaxes(tickangle=-30, tickfont=dict(size=11))
                st.plotly_chart(fig, use_container_width=True)

    # ── Purple Cap ──────────────────────────────
    with col_p:
        st.markdown('<div class="section-sub">🟣 Purple Cap — Top Wicket Takers</div>', unsafe_allow_html=True)
        if not purple_cap.empty:
            for i, (_, row) in enumerate(purple_cap.iterrows()):
                player_col  = next((c for c in row.index if "PLAYER" in c.upper() or "BOWLER" in c.upper() or "NAME" in c.upper()), purple_cap.columns[0])
                wicket_col  = next((c for c in row.index if "WICKET" in c.upper()), purple_cap.columns[1])
                team_col    = next((c for c in row.index if "TEAM" in c.upper()), None)
                team_tag    = f'<div class="team-tag">{row[team_col]}</div>' if team_col else ""
                rnk_cls     = "top" if i == 0 else ""
                st.markdown(
                    f'<div class="award-card">'
                    f'<div class="rnk {rnk_cls}">{i+1}</div>'
                    f'<div class="name"><div class="pname">{row[player_col]}</div>{team_tag}</div>'
                    f'<div class="stat stat-purple">{row[wicket_col]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with st.expander("📊 Wickets Distribution Chart"):
                fig = px.bar(
                    purple_cap,
                    x=purple_cap.columns[0],
                    y=purple_cap.columns[1],
                    color_discrete_sequence=["#a855f7"],
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="#0a0e1a",
                    plot_bgcolor="#0d1429",
                    font_color="#e8eaf0",
                    xaxis_title="",
                    yaxis_title="Wickets",
                    showlegend=False,
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=60),
                )
                fig.update_xaxes(tickangle=-30, tickfont=dict(size=11))
                st.plotly_chart(fig, use_container_width=True)


# #############################################################################
# PAGE 5 — ANALYTICS
# #############################################################################
elif page == "Analytics":

    team_runs = data["team_runs"]

    st.markdown('<div class="section-header" style="margin-top:0">📈 Team Analytics</div>', unsafe_allow_html=True)

    if not team_runs.empty:
        team_col = "BATTING_TEAM"
        runs_col = "TOTAL_RUNS"

        team_runs_sorted = team_runs.sort_values(runs_col, ascending=True)
        colors = [
            TEAM_META.get(t, {}).get("bg", "#3b82f6")
            for t in team_runs_sorted[team_col]
        ]

        # ── Horizontal bar chart ──────────────────────
        fig = go.Figure(go.Bar(
            x=team_runs_sorted[runs_col],
            y=team_runs_sorted[team_col],
            orientation="h",
            marker=dict(color=colors, line=dict(color="#0a0e1a", width=0.5)),
            text=team_runs_sorted[runs_col],
            textposition="outside",
            textfont=dict(color="#e0e6ff", family="Barlow Condensed", size=14),
        ))
        fig.update_layout(
            title=dict(text="Total Runs Scored by Team", font=dict(color="#ffd700", family="Barlow Condensed", size=18)),
            paper_bgcolor="#0a0e1a",
            plot_bgcolor="#0d1429",
            font_color="#e8eaf0",
            height=420,
            margin=dict(l=10, r=60, t=50, b=20),
            xaxis=dict(gridcolor="#1e2540", showgrid=True, color="#5a6480"),
            yaxis=dict(gridcolor="#0d1429", color="#c8d0e8"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Radar / pie chart ─────────────────────────
        col_a, col_b = st.columns(2)

        with col_a:
            fig2 = px.pie(
                team_runs,
                names=team_col,
                values=runs_col,
                color_discrete_sequence=[TEAM_META.get(t, {}).get("bg", "#334155") for t in team_runs[team_col]],
                template="plotly_dark",
                hole=0.42,
            )
            fig2.update_traces(textfont_color="#e0e6ff", textfont_family="Barlow Condensed")
            fig2.update_layout(
                title=dict(text="Run Share", font=dict(color="#ffd700", family="Barlow Condensed", size=16)),
                paper_bgcolor="#0a0e1a",
                height=380,
                margin=dict(l=10, r=10, t=50, b=10),
                legend=dict(font=dict(color="#8892b0", size=11)),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col_b:
            fig3 = px.scatter(
                team_runs,
                x=team_col,
                y=runs_col,
                size=runs_col,
                color=team_col,
                color_discrete_sequence=[TEAM_META.get(t, {}).get("bg", "#334155") for t in team_runs[team_col]],
                template="plotly_dark",
            )
            fig3.update_layout(
                title=dict(text="Run Volume Bubble", font=dict(color="#ffd700", family="Barlow Condensed", size=16)),
                paper_bgcolor="#0a0e1a",
                plot_bgcolor="#0d1429",
                height=380,
                showlegend=False,
                margin=dict(l=10, r=10, t=50, b=10),
                xaxis=dict(showticklabels=False, gridcolor="#1e2540"),
                yaxis=dict(gridcolor="#1e2540", color="#5a6480"),
            )
            st.plotly_chart(fig3, use_container_width=True)

    else:
        st.info("Analytics data not available.")


# #############################################################################
# PAGE 6 — MATCH RESULTS
# #############################################################################
elif page == "Match Results":

    match_results = data["match_results"]

    st.markdown(
        '<div class="section-header">📋 Match Results</div>',
        unsafe_allow_html=True
    )

    for _, row in match_results.iterrows():
        st.markdown(f"""
        <div class="result-card">
            <div style="display:flex;align-items:center;gap:10px;flex:1;">
                {team_badge(row["TEAM1"],36)}
                <div>
                    <b>{row["TEAM1"]}</b><br>
                    {row["TEAM1_SCORE"]}
                </div>
            </div>
            <div style="text-align:center;flex:1;">
                <h3 style="margin:0;font-size:24px;color:#ffd700;">VS</h3>
                <p style="margin:2px 0;font-size:13px;">Winner : <b style="color:#4cef9f;">{row["WINNER"]}</b></p>
                <p style="margin:0;font-size:12px;color:#a0a8c0;">Margin : {row["MARGIN"]} runs</p>
            </div>
            <div style="display:flex;align-items:center;gap:10px;justify-content:flex-end;flex:1;">
                <div style="text-align:right;">
                    <b>{row["TEAM2"]}</b><br>
                    {row["TEAM2_SCORE"]}
                </div>
                {team_badge(row["TEAM2"],36)}
            </div>
        </div>
        """, unsafe_allow_html=True)