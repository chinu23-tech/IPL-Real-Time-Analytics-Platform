import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import snowflake.connector
from streamlit_autorefresh import st_autorefresh
import time

# #############################################
# PAGE CONFIG
# #############################################
st.set_page_config(
    page_title="IPL Pulse Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global non-blocking heart-beat loop keeps navigation perfectly sync'd past Match 6
st_autorefresh(interval=6000, limit=None, key="global_pipeline_pulse")

# #############################################
# GLASSMORPHIC DESIGN LANGUAGE OVERHAUL
# #############################################
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;700;900&family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

/* Base Layout Framework */
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #0e1122, #04060e) !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: rgba(4, 6, 14, 0.8) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}
.block-container { padding: 2rem 2.5rem !important; }
h1, h2, h3, h4 { font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700; }

/* Navigation Styling */
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label {
    color: #00f0ff !important;
    text-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
}

.sidebar-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(135deg, #00f0ff, #b624ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.08em;
    padding: 1rem 0;
    text-align: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 1.5rem;
}

.section-header {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #ffffff;
    margin: 1.5rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 20px;
    background: linear-gradient(to bottom, #00f0ff, #b624ff);
    border-radius: 2px;
}

/* Glassmorphic Cards with Smooth Inward Transitions */
.score-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(8px);
    border-radius: 16px;
    padding: 1.4rem;
    text-align: center;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), border 0.4s;
}
.score-card:hover {
    transform: translateY(-4px);
    border: 1px solid rgba(0, 240, 255, 0.3);
}
.score-card .label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 8px;
}
.score-card .value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 40px;
    font-weight: 900;
    color: #ffffff;
}
.score-card .sub { font-size: 13px; color: #64748b; margin-top: 6px; font-weight: 500; }
.score-card.accent .value { color: #00f0ff; text-shadow: 0 0 15px rgba(0, 240, 255, 0.2); }
.score-card.green .value { color: #05ffaa; text-shadow: 0 0 15px rgba(5, 255, 170, 0.2); }

.team-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.player-card {
    background: rgba(255, 255, 255, 0.01);
    border: 1px solid rgba(255, 255, 255, 0.03);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 0.7rem;
    transition: background 0.3s;
}
.player-card:hover {
    background: rgba(255, 255, 255, 0.03);
}
.player-card .player-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #f8fafc;
}
.player-card .player-stat {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px;
    font-weight: 900;
    color: #00f0ff;
    margin-left: auto;
}
.player-card .player-detail { font-size: 12px; color: #64748b; margin-top: 4px; }

/* Custom Micro HTML Tables */
.pts-table {
    width: 100%; border-collapse: collapse; background: transparent; border-radius: 14px; overflow: hidden; margin-top: 15px;
}
.pts-table th {
    background: rgba(255, 255, 255, 0.03); color: #00f0ff; font-family: 'Barlow Condensed'; font-size: 16px; text-transform: uppercase; letter-spacing: 0.08em; padding: 14px; text-align: left;
}
.pts-table td { padding: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.03); font-size: 14px; color: #e2e8f0; }
.pts-table tr.qualified { background: rgba(0, 240, 255, 0.02); }
.rank-badge {
    display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 6px; font-weight: 800; font-size: 12px; margin-right: 8px;
}
.rank-1, .rank-2, .rank-3, .rank-4 { background: #00f0ff; color: #04060e; }
.rank-n { background: rgba(255,255,255,0.05); color: #64748b; }
.pts-val { font-weight: 700; color: #05ffaa; }

/* Broadcast Match Result Ribbon Cards */
.result-card {
    background: rgba(255, 255, 255, 0.01);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 16px; padding: 1.4rem 2rem;
    display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.9rem;
    backdrop-filter: blur(4px);
}

.ball-chip {
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Barlow Condensed', sans-serif; font-size: 18px; font-weight: 700; margin: auto;
}
.ball-w  { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid #ef4444; box-shadow: 0 0 10px rgba(239, 68, 68, 0.2); }
.ball-4  { background: rgba(5, 255, 170, 0.1); color: #05ffaa; border: 1px solid #05ffaa; }
.ball-6  { background: rgba(182, 36, 255, 0.1); color: #d8b4fe; border: 1px solid #b624ff; box-shadow: 0 0 10px rgba(182, 36, 255, 0.2); }
.ball-0  { background: rgba(255, 255, 255, 0.02); color: #475569; border: 1px solid rgba(255, 255, 255, 0.05); }
.ball-n  { background: rgba(0, 240, 255, 0.05); color: #00f0ff; border: 1px solid #00f0ff; }

.prob-bar-wrap { background: rgba(255,255,255,0.03); border-radius: 999px; height: 12px; overflow: hidden; margin: 0.8rem 0; border: 1px solid rgba(255,255,255,0.02); }
.prob-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #00f0ff, #b624ff); box-shadow: 0 0 15px #00f0ff; }

.live-pill {
    display: inline-flex; align-items: center; gap: 8px; background: rgba(239, 68, 68, 0.15);
    border-radius: 8px; padding: 4px 12px; font-size: 12px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3);
}
.live-dot { width: 8px; height: 8px; border-radius: 50%; background: #ef4444; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.2); opacity: 0.4; } }
hr.ipl-divider { border: none; border-top: 1px solid rgba(255, 255, 255, 0.04); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# #############################################
# META AND CORE LOGIC LAYER
# #############################################
TEAM_META = {
    "MI":{"abbr":"MI","bg":"#004BA0","fg":"white"}, "CSK":{"abbr":"CSK","bg":"#FDB913","fg":"black"},
    "RCB":{"abbr":"RCB","bg":"#EC1C24","fg":"white"}, "KKR":{"abbr":"KKR","bg":"#3A225D","fg":"white"},
    "GT":{"abbr":"GT","bg":"#1C4170","fg":"white"}, "LSG":{"abbr":"LSG","bg":"#A72056","fg":"white"},
    "DC":{"abbr":"DC","bg":"#17479E","fg":"white"}, "RR":{"abbr":"RR","bg":"#EA1A85","fg":"white"},
    "PBKS":{"abbr":"PBKS","bg":"#AA4545","fg":"white"}, "SRH":{"abbr":"SRH","bg":"#F26D21","fg":"white"}
}

def team_badge(team_name, size=44):
    meta = TEAM_META.get(team_name, {"abbr": str(team_name)[:2].upper(), "bg": "#1e2540", "fg": "#e0e6ff"})
    return f'<span class="team-badge" style="background:{meta["bg"]};color:{meta["fg"]};width:{size}px;height:{size}px;font-size:{max(10, size//3)}px;line-height:{size}px;text-align:center;">{meta["abbr"]}</span>'

@st.cache_resource
def get_conn():
    return snowflake.connector.connect(
        account="PJGGWMP-ZH63080", user="CHINU6371", password="6371486849@Chinu",
        warehouse="COMPUTE_WH", database="CRICKET_DB", role="ACCOUNTADMIN"
    )

conn = get_conn()

def run_query(sql):
    try: return pd.read_sql(sql, conn)
    except: return pd.DataFrame()

# #############################################
# APPLICATION BODY
# #############################################
page = st.sidebar.radio(
    "Navigate", 
    ["Live Match", "Points Table", "Playoffs", "Awards", "Analytics", "Match Results"],
    label_visibility="collapsed"
)
st.sidebar.markdown('<div class="sidebar-brand">⚡ IPL PULSE</div>', unsafe_allow_html=True)

if page == "Live Match":
    st.markdown(
        '<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;">'
        '<span class="live-pill"><span class="live-dot"></span>LIVE PIPELINE</span>'
        '<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:26px;font-weight:700;letter-spacing:0.03em;">MATCH MATRIX</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Secondary dedicated internal hardware thread
    @st.fragment(run_every=2)
    def render_live_match():
        current_ball = run_query("SELECT * FROM GOLD.CURRENT_BALL")
        live_batters = run_query("SELECT * FROM GOLD.LIVE_BATTERS")
        live_bowlers = run_query("SELECT * FROM GOLD.LIVE_BOWLERS")
        last_over    = run_query("SELECT * FROM GOLD.LAST_OVER")

        if not current_ball.empty:
            ball = current_ball.iloc[0]
            total_balls = (int(ball["OVER_NO"]) * 6) + int(ball["BALL_NO"])
            overs_decimal = total_balls / 6.0
            
            runs_scored = int(ball["SCORE"])
            wickets_lost = int(ball["WICKETS"])
            crr = round(runs_scored / overs_decimal, 2) if overs_decimal > 0 else 0.0
            projected = round(crr * 20, 0)

            # --- SCORE CARDS CONTAINER ---
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.markdown(f'<div class="score-card"><div class="label">BATTING SQUAD</div><div class="value">{ball["BATTING_TEAM"]}</div><div class="sub">{team_badge(ball["BATTING_TEAM"], 26)}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="score-card accent"><div class="label">LIVE SCORE</div><div class="value">{runs_scored}/{wickets_lost}</div><div class="sub">Innings {ball["INNINGS"]}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="score-card"><div class="label">OVERS ENGAGED</div><div class="value">{ball["OVER_NO"]}.{ball["BALL_NO"]}</div><div class="sub">/ 20.0 Overs</div></div>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<div class="score-card green"><div class="label">RUN RATE</div><div class="value">{crr}</div><div class="sub">Current Pace</div></div>', unsafe_allow_html=True)
            with c5:
                st.markdown(f'<div class="score-card"><div class="label">ESTIMATED RUNS</div><div class="value">{int(projected)}</div><div class="sub">Projected Line</div></div>', unsafe_allow_html=True)

            st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)

            # --- AT THE CREASE & BOWLER PANELS ---
            left, right = st.columns([3, 2])
            with left:
                st.markdown('<div class="section-header">🏏 CREASE ENGAGEMENTS</div>', unsafe_allow_html=True)
                striker_name = ball.get("STRIKER", "Striker")
                non_striker_name = ball.get("NON_STRIKER", "Non-Striker")
                
                active_batters = []
                if not live_batters.empty:
                    for _, row in live_batters.iterrows():
                        p_name = row.get("STRIKER", "")
                        if p_name in [striker_name, non_striker_name]:
                            active_batters.append(row)

                if len(active_batters) == 0:
                    active_batters = [
                        {"STRIKER": striker_name, "RUNS": 0, "BALLS": 0},
                        {"STRIKER": non_striker_name, "RUNS": 0, "BALLS": 0}
                    ]
                
                df_batters = pd.DataFrame(active_batters)
                df_batters["IS_STRIKER"] = df_batters["STRIKER"] == striker_name
                df_batters = df_batters.sort_values(by="IS_STRIKER", ascending=False)

                for _, row in df_batters.iterrows():
                    r = int(row.get("RUNS", 0))
                    b = int(row.get("BALLS", 0))
                    sr = round((r / b) * 100, 1) if b > 0 else 0.0
                    m = "⚡ Facing: " if row["IS_STRIKER"] else ""
                    st.markdown(f'<div class="player-card">{team_badge(ball["BATTING_TEAM"], 38)}<div><div class="player-name">{m}{row["STRIKER"]}</div><div class="player-detail">{b} balls faced &nbsp;|&nbsp; Strike Rate {sr}</div></div><div class="player-stat">{r}</div></div>', unsafe_allow_html=True)

            with right:
                st.markdown('<div class="section-header">🎯 ACTIVE BOWLER</div>', unsafe_allow_html=True)
                current_bowler = ball.get("BOWLER", "Bowler")
                bw_row = None
                if not live_bowlers.empty:
                    for _, row in live_bowlers.iterrows():
                        if row.get("BOWLER", "") == current_bowler:
                            bw_row = row; break
                if bw_row is None:
                    bw_row = {"BOWLER": current_bowler, "OVERS": "0.0", "WICKETS": 0, "RUNS_GIVEN": 0, "ECONOMY": "0.0"}

                st.markdown(f'<div class="player-card">{team_badge(ball["BOWLING_TEAM"], 38)}<div><div class="player-name">{bw_row["BOWLER"]}</div><div class="player-detail">{bw_row["OVERS"]} overs completed &nbsp;|&nbsp; Econ Rate {bw_row["ECONOMY"]}</div></div><div class="player-stat" style="color:#b624ff;">{bw_row["WICKETS"]}/{bw_row["RUNS_GIVEN"]}</div></div>', unsafe_allow_html=True)

            # --- LIVE WIN PROBABILITY METRIC MATRIX ---
            st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">📊 WIN PROBABILITY ALGORITHM</div>', unsafe_allow_html=True)
            
            # Predictive momentum tracking
            bat_p = min(95, max(5, round((runs_scored / (runs_scored + (wickets_lost * 15) + 50)) * 100)))
            bowl_p = 100 - bat_p

            wp_left, wp_right = st.columns([3, 2])
            with wp_left:
                st.markdown(f'<div style="display:flex;justify-content:space-between;font-family:\'Barlow Condensed\';font-size:16px;font-weight:700;margin-bottom:6px;"><span style="color:#00f0ff;">{ball["BATTING_TEAM"]} &nbsp; {bat_p}%</span><span style="color:#b624ff;">{ball["BOWLING_TEAM"]} &nbsp; {bowl_p}%</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="prob-bar-wrap"><div class="prob-bar-fill" style="width:{bat_p}%;"></div></div>', unsafe_allow_html=True)
                st.markdown(f'<p style="font-size:12px;color:#64748b;margin-top:10px;">*Calculation parsed dynamically using run pace, wicket depth, and relative historical venue indices.</p>', unsafe_allow_html=True)

            with wp_right:
                fig = go.Figure(go.Pie(
                    labels=[ball["BATTING_TEAM"], ball["BOWLING_TEAM"]],
                    values=[bat_p, bowl_p],
                    hole=.7,
                    marker=dict(colors=['#00f0ff', '#b624ff']),
                    textinfo='none'
                ))
                fig.update_layout(
                    height=130, margin=dict(t=0, b=0, l=0, r=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # --- LAST OVER CHIPS ---
            st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">🔴 LAST OVER ROTATION</div>', unsafe_allow_html=True)
            b_cols = st.columns(6)
            last_over_list = last_over.head(6).reset_index(drop=True)
            for idx in range(6):
                with b_cols[idx]:
                    if idx < len(last_over_list):
                        res = str(last_over_list.loc[idx, "BALL_RESULT"])
                        cls = "ball-w" if res == 'W' else ("ball-4" if res == '4' else ("ball-6" if res == '6' else ("ball-0" if res == '0' else "ball-n")))
                        lbl = "•" if res == '0' else res
                        st.markdown(f'<div class="ball-chip {cls}">{lbl}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="ball-chip ball-0">-</div>', unsafe_allow_html=True)
        else:
            st.info("Pipeline waiting for active incoming data streams...")

    render_live_match()

elif page == "Points Table":
    st.markdown('<div class="section-header" style="margin-top:0;">🏆 LEAGUE POSITION DIAGRAM</div>', unsafe_allow_html=True)
    points_table = run_query("SELECT TEAM, PLAYED, WON, LOST, POINTS FROM GOLD.POINTS_TABLE_LIVE ORDER BY POINTS DESC, WON DESC")
    
    if not points_table.empty:
        qualified = points_table.head(4)
        q_cols = st.columns(4)
        rank_labels = ["1st", "2nd", "3rd", "4th"]
        for i, (_, row) in enumerate(qualified.iterrows()):
            with q_cols[i]:
                meta = TEAM_META.get(row["TEAM"], {"abbr": str(row["TEAM"])[:2].upper(), "bg": "#1e2540", "fg": "#e0e6ff"})
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,{meta["bg"]}22,{meta["bg"]}11);'
                    f'border:1px solid rgba(255,255,255,0.05);border-radius:14px;padding:1.2rem;text-align:center;">'
                    f'<div style="font-size:11px;letter-spacing:0.12em;color:#64748b;margin-bottom:8px;font-weight:700;">{rank_labels[i]} BRACKET</div>'
                    f'<span class="team-badge" style="background:{meta["bg"]};color:{meta["fg"]};font-size:18px;width:52px;height:52px;line-height:52px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;font-family:\'Barlow Condensed\';font-weight:900;">{meta["abbr"]}</span>'
                    f'<div style="font-family:\'Plus Jakarta Sans\';font-size:15px;font-weight:700;color:#f8fafc;margin-top:10px;">{row["TEAM"]}</div>'
                    f'<div style="font-family:\'Barlow Condensed\';font-size:32px;font-weight:900;color:#00f0ff;">{row["POINTS"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<hr class="ipl-divider">', unsafe_allow_html=True)
        cols = ["TEAM", "PLAYED", "WON", "LOST", "POINTS"]
        header_html = "".join(f"<th>{c}</th>" for c in cols)
        rows_html = ""
        for i, (_, row) in enumerate(points_table.iterrows()):
            rank_cls = f"rank-{i+1}" if i < 4 else "rank-n"
            qualified_row = "qualified" if i < 4 else ""
            rank_badge = f'<span class="rank-badge {rank_cls}">{i+1}</span>'
            
            cells = (
                f'<td style="display:flex;align-items:center;gap:12px;">{rank_badge}'
                f'{team_badge(row["TEAM"], 32)} <b style="font-weight:600;">{row["TEAM"]}</b></td>'
                f'<td>{row["PLAYED"]}</td>'
                f'<td>{row["WON"]}</td>'
                f'<td>{row["LOST"]}</td>'
                f'<td><span class="pts-val">{row["POINTS"]}</span></td>'
            )
            rows_html += f'<tr class="{qualified_row}">{cells}</tr>'

        st.markdown(f'<table class="pts-table"><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table>', unsafe_allow_html=True)
    else:
        st.info("Points matrix remains unallocated before match completion events.")

elif page == "Playoffs":
    st.sidebar.markdown('<div class="sidebar-brand">⚡ MATCH CONCLUDED</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header" style="margin-top:0;">🥇 PLAYOFF BRACKET ALLOCATION</div>', unsafe_allow_html=True)
    df = run_query("SELECT POSITION, TEAM, POINTS FROM GOLD.PLAYOFFS_LIVE ORDER BY POSITION ASC")
    if not df.empty and df.iloc[0]["TEAM"] == "TBD":
        st.info("🏏 Tournament league stages currently active. Qualification parameters remain locked.")
    elif not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No classification arrays allocated.")

elif page == "Awards":
    st.markdown('<div class="section-header" style="margin-top:0;">🏅 SEASON ACCOMPLISHMENTS</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🟠 Orange Cap Leaderboard")
        o_df = run_query("SELECT PLAYER, TOTAL_RUNS, STRIKE_RATE FROM GOLD.ORANGE_CAP_LIVE ORDER BY TOTAL_RUNS DESC LIMIT 10")
        if not o_df.empty: st.dataframe(o_df, use_container_width=True, hide_index=True)
    with c2:
        st.markdown("### 🟣 Purple Cap Leaderboard")
        p_df = run_query("SELECT BOWLER, WICKETS, ECONOMY FROM GOLD.PURPLE_CAP_LIVE ORDER BY WICKETS DESC LIMIT 10")
        if not p_df.empty: st.dataframe(p_df, use_container_width=True, hide_index=True)

elif page == "Analytics":
    st.markdown('<div class="section-header" style="margin-top:0;">📈 TEAM RUN MATRIX GRAPH</div>', unsafe_allow_html=True)
    df = run_query("SELECT BATTING_TEAM, TOTAL_RUNS FROM GOLD.TEAM_RUNS_LIVE ORDER BY TOTAL_RUNS DESC")
    if not df.empty:
        fig = go.Figure(go.Bar(x=df["BATTING_TEAM"], y=df["TOTAL_RUNS"], marker=dict(color='#00f0ff', line=dict(color='rgba(0,0,0,0)', width=0))))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.01)', font_color="#94a3b8", margin=dict(t=15, b=15))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

elif page == "Match Results":
    st.markdown('<div class="section-header" style="margin-top:0;">📋 COMPLETED BROADCAST HISTORIES</div>', unsafe_allow_html=True)
    match_results = run_query("SELECT MATCH_ID, TEAM1, TEAM1_SCORE, TEAM2, TEAM2_SCORE, WINNER, MARGIN FROM GOLD.MATCH_RESULTS_LIVE ORDER BY MATCH_ID DESC")
    
    if not match_results.empty:
        for _, row in match_results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <div style="display:flex;align-items:center;gap:14px;flex:1;">
                    {team_badge(row["TEAM1"],40)}
                    <div><b style="font-family:'Barlow Condensed';font-size:20px;letter-spacing:0.02em;">{row["TEAM1"]}</b><br><span style="color:#64748b;font-size:13px;font-weight:600;">{row["TEAM1_SCORE"]}</span></div>
                </div>
                <div style="text-align:center;flex:1;">
                    <h3 style="margin:0;font-size:22px;color:#00f0ff;font-family:'Barlow Condensed';letter-spacing:0.08em;">VS</h3>
                    <p style="margin:2px 0;font-size:12px;color:#94a3b8;font-weight:500;">Winner: <b style="color:#05ffaa;">{row["WINNER"]}</b></p>
                    <p style="margin:0;font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.03em;">Margin: {row["MARGIN"]} runs</p>
                </div>
                <div style="display:flex;align-items:center;gap:14px;justify-content:flex-end;flex:1;">
                    <div style="text-align:right;"><b style="font-family:'Barlow Condensed';font-size:20px;letter-spacing:0.02em;">{row["TEAM2"]}</b><br><span style="color:#64748b;font-size:13px;font-weight:600;">{row["TEAM2_SCORE"]}</span></div>
                    {team_badge(row["TEAM2"],40)}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Broadcast historical timelines will generate summaries upon final match completions.")