import streamlit as st
import streamlit.components.v1 as components
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict_next_race import predict_next_race

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="F1 Prediction Engine", layout="wide", page_icon="🏎️")

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,300;0,400;0,600;0,700;0,800;0,900;1,700&family=Barlow:wght@300;400;500;600&display=swap');

/* ── Root variables ── */
:root {
    --f1-red:      #E8002D;
    --f1-red-dim:  #9B001E;
    --f1-white:    #F5F5F5;
    --f1-silver:   #9E9E9E;
    --carbon-900:  #0A0A0A;
    --carbon-800:  #111111;
    --carbon-700:  #1A1A1A;
    --carbon-600:  #222222;
    --carbon-500:  #2E2E2E;
    --stripe:      rgba(255,255,255,0.03);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: var(--carbon-900) !important;
    color: var(--f1-white) !important;
}

.stApp {
    background-color: var(--carbon-900) !important;
}

/* ── Remove Streamlit chrome ── */
header[data-testid="stHeader"],
footer,
#MainMenu { display: none !important; }

/* ── Hide default Streamlit padding ── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 1200px;
}

/* ════════════════════════════════════════
   HERO HEADER
════════════════════════════════════════ */
.f1-hero {
    position: relative;
    background: var(--carbon-800);
    border-bottom: 3px solid var(--f1-red);
    padding: 2.5rem 3rem 2rem;
    margin-bottom: 2rem;
    overflow: hidden;
}

/* diagonal speed stripe */
.f1-hero::before {
    content: '';
    position: absolute;
    top: 0; right: -40px;
    width: 220px; height: 100%;
    background: var(--f1-red);
    transform: skewX(-12deg);
    opacity: 0.08;
}

.f1-hero-eyebrow {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--f1-red);
    margin-bottom: 0.4rem;
}

.f1-hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    font-weight: 900;
    font-style: italic;
    line-height: 0.92;
    text-transform: uppercase;
    letter-spacing: -0.01em;
    color: var(--f1-white);
    margin: 0 0 0.6rem;
}

.f1-hero-title span {
    color: var(--f1-red);
}

.f1-hero-subtitle {
    font-size: 0.875rem;
    color: var(--f1-silver);
    font-weight: 300;
    letter-spacing: 0.04em;
    max-width: 520px;
    line-height: 1.6;
}

/* ── Red pill badge ── */
.f1-badge {
    display: inline-block;
    background: var(--f1-red);
    color: white;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
    margin-right: 6px;
    vertical-align: middle;
}

/* ════════════════════════════════════════
   STAT PILLS ROW
════════════════════════════════════════ */
.stat-row {
    display: flex;
    gap: 1px;
    margin-bottom: 2rem;
    background: var(--carbon-600);
    border: 1px solid var(--carbon-600);
    border-radius: 4px;
    overflow: hidden;
}

.stat-pill {
    flex: 1;
    background: var(--carbon-700);
    padding: 1rem 1.2rem;
    text-align: center;
}

.stat-pill-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--f1-silver);
    margin-bottom: 4px;
}

.stat-pill-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--f1-white);
    line-height: 1;
}

.stat-pill-value.red { color: var(--f1-red); }

/* ════════════════════════════════════════
   PREDICT BUTTON
════════════════════════════════════════ */
.stButton > button {
    background: var(--f1-red) !important;
    color: white !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    font-style: italic !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2.5rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    box-shadow: 0 4px 20px rgba(232,0,45,0.35) !important;
}

.stButton > button:hover {
    background: #c8001f !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(232,0,45,0.5) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ════════════════════════════════════════
   SECTION HEADERS
════════════════════════════════════════ */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--carbon-500);
}

.section-header-line {
    width: 4px;
    height: 1.4rem;
    background: var(--f1-red);
    border-radius: 1px;
    flex-shrink: 0;
}

.section-header-text {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--f1-silver);
}

/* ════════════════════════════════════════
   RACE INFO CARD
════════════════════════════════════════ */
.race-info-card {
    background: var(--carbon-700);
    border: 1px solid var(--carbon-500);
    border-left: 4px solid var(--f1-red);
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}

.race-info-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    font-style: italic;
    text-transform: uppercase;
    color: var(--f1-white);
    line-height: 1;
    margin-bottom: 4px;
}

.race-info-subtitle {
    font-size: 0.78rem;
    color: var(--f1-silver);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ════════════════════════════════════════
   WINNER PODIUM CARD
════════════════════════════════════════ */
.winner-card {
    background: linear-gradient(135deg, var(--carbon-700) 0%, #1a0505 100%);
    border: 1px solid rgba(232,0,45,0.4);
    border-top: 3px solid var(--f1-red);
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.winner-card::after {
    content: '🏆';
    position: absolute;
    right: 1.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 3rem;
    opacity: 0.15;
}

.winner-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--f1-red);
    margin-bottom: 0.4rem;
}

.winner-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.6rem;
    font-weight: 900;
    font-style: italic;
    text-transform: uppercase;
    color: var(--f1-white);
    line-height: 0.95;
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}

.winner-prob {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--f1-red);
    letter-spacing: 0.05em;
}

/* ════════════════════════════════════════
   LEADERBOARD TABLE
════════════════════════════════════════ */

/* Override Streamlit dataframe container */
[data-testid="stDataFrame"] {
    border: 1px solid var(--carbon-500) !important;
    border-radius: 4px !important;
    overflow: hidden !important;
    background: var(--carbon-700) !important;
}

div[data-testid="stDataFrame"] > div {
    background: var(--carbon-700) !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--f1-red) !important;
}

/* ── Info boxes (remove default streamlit boxes) ── */
.stAlert {
    background: var(--carbon-700) !important;
    border: 1px solid var(--carbon-500) !important;
    border-radius: 4px !important;
    color: var(--f1-white) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--carbon-800); }
::-webkit-scrollbar-thumb { background: var(--carbon-500); border-radius: 3px; }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--carbon-500) !important;
    margin: 2rem 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════
#  HERO
# ════════════════════════════════════════
st.markdown("""
<div class="f1-hero">
    <div class="f1-hero-eyebrow">&#9632; Formula 1 · AI Prediction Engine</div>
    <div class="f1-hero-title">Race Winner<br><span>Prediction</span></div>
    <div class="f1-hero-subtitle">
        Powered by historical race data, driver form, constructor dominance,
        circuit performance &amp; grid position analysis.
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════
#  STAT PILLS
# ════════════════════════════════════════
st.markdown("""
<div class="stat-row">
    <div class="stat-pill">
        <div class="stat-pill-label">Data Sources</div>
        <div class="stat-pill-value red">5</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-label">Model Type</div>
        <div class="stat-pill-value" style="font-size:1rem;padding-top:4px;">ML Ensemble</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-label">Live Data</div>
        <div class="stat-pill-value red">✓</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-label">Coverage</div>
        <div class="stat-pill-value" style="font-size:1rem;padding-top:4px;">Full Grid</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════
#  PREDICT BUTTON
# ════════════════════════════════════════
col_btn, col_gap = st.columns([1, 3])
with col_btn:
    run = st.button("⚡  Run Prediction")


# ════════════════════════════════════════
#  RESULTS
# ════════════════════════════════════════
if run:
    with st.spinner("Fetching live race data and running model..."):
        leaderboard = predict_next_race()

    race_info = leaderboard.iloc[0]
    winner    = leaderboard.iloc[0]

    # ── Race info ──
    st.markdown("""
    <div class="section-header">
        <div class="section-header-line"></div>
        <div class="section-header-text">Next Race</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="race-info-card">
        <div class="race-info-subtitle">Round · {int(race_info['year'])}</div>
        <div class="race-info-title">{race_info['race_name']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Winner ──
    st.markdown("""
    <div class="section-header">
        <div class="section-header-line"></div>
        <div class="section-header-text">Predicted Race Winner</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="winner-card">
        <div class="winner-label">&#9632; Pole Position Favourite</div>
        <div class="winner-name">{winner['driverId']}</div>
        <div class="winner-prob">{winner['win_probability']:.2%} win probability</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Leaderboard ──
    st.markdown("""
    <div class="section-header">
        <div class="section-header-line"></div>
        <div class="section-header-text">Full Prediction Leaderboard</div>
    </div>
    """, unsafe_allow_html=True)

    # Constructor color map (F1 2024 livery palette)
    CONSTRUCTOR_COLORS = {
        "red_bull":     "#3671C6",
        "mclaren":      "#FF8000",
        "ferrari":      "#E8002D",
        "mercedes":     "#27F4D2",
        "aston_martin": "#229971",
        "alpine":       "#FF87BC",
        "williams":     "#64C4FF",
        "rb":           "#6692FF",
        "haas":         "#B6BABD",
        "sauber":       "#52E252",
        "kick_sauber":  "#52E252",
    }

    display_cols = ["driverId", "constructorId", "grid_position", "win_probability"]
    df = leaderboard[display_cols].copy().reset_index(drop=True)
    max_prob = df["win_probability"].max()

    def pos_medal(i):
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}
        return medals.get(i, f"P{i+1}")

    rows_html = ""
    for i, row in df.iterrows():
        is_winner = (i == 0)
        row_bg    = "background:linear-gradient(90deg,#1a0505 0%,#160303 100%);" if is_winner else "background:#111111;"
        row_border = "border-left:3px solid #E8002D;" if is_winner else "border-left:3px solid transparent;"
        driver    = row["driverId"].replace("_", " ").upper()
        medal     = pos_medal(i)
        c_color   = CONSTRUCTOR_COLORS.get(row["constructorId"].lower(), "#888888")
        c_label   = row["constructorId"].replace("_", " ").upper()
        d_color   = "#FFFFFF" if is_winner else "#CCCCCC"

        prob      = row["win_probability"]
        pct       = (prob / max_prob) * 100 if max_prob > 0 else 0
        heat      = "#E8002D" if pct > 66 else "#FF6B35" if pct > 33 else "#888888"
        prob_str  = f"{prob:.2%}"

        rows_html += f"""
        <tr style="{row_bg}{row_border}">
            <td class="pos">{medal}</td>
            <td><span class="driver" style="color:{d_color};">{driver}</span></td>
            <td>
                <span class="team">
                    <span class="team-pip" style="background:{c_color};"></span>
                    <span style="color:{c_color};">{c_label}</span>
                </span>
            </td>
            <td class="grid">P{int(row['grid_position'])}</td>
            <td>
                <div class="prob-wrap">
                    <div class="prob-track">
                        <div class="prob-fill" style="width:{pct:.1f}%;background:{heat};"></div>
                    </div>
                    <span class="prob-val" style="color:{heat};">{prob_str}</span>
                </div>
            </td>
        </tr>
        """

    table_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;0,900;1,700;1,800&family=Barlow:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            background: transparent;
            font-family: 'Barlow', sans-serif;
        }}
        .wrap {{
            border: 1px solid #2E2E2E;
            border-radius: 6px;
            overflow: hidden;
            background: #111111;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        thead tr {{
            background: #1A1A1A;
            border-bottom: 2px solid #E8002D;
        }}
        thead th {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: #9E9E9E;
            padding: 0.85rem 1rem;
            text-align: left;
        }}
        thead th:first-child {{ text-align: center; width: 56px; }}
        thead th:nth-child(4) {{ text-align: center; }}
        tbody tr {{
            border-bottom: 1px solid #222222;
            transition: background 0.12s;
        }}
        tbody tr:hover {{ background: #1c1c1c !important; }}
        tbody td {{
            padding: 0.95rem 1rem;
            color: #F5F5F5;
            vertical-align: middle;
        }}
        .pos {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.15rem;
            font-weight: 800;
            color: #888;
            text-align: center;
        }}
        .driver {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            font-style: italic;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }}
        .team {{
            display: inline-flex;
            align-items: center;
            gap: 7px;
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}
        .team-pip {{
            width: 3px;
            height: 1.1em;
            border-radius: 1px;
            flex-shrink: 0;
            display: inline-block;
        }}
        .grid {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.2rem;
            font-weight: 700;
            color: #888;
            text-align: center;
        }}
        .prob-wrap {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .prob-track {{
            flex: 1;
            background: #2a2a2a;
            border-radius: 3px;
            height: 7px;
            min-width: 90px;
            overflow: hidden;
        }}
        .prob-fill {{
            height: 100%;
            border-radius: 3px;
        }}
        .prob-val {{
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            min-width: 56px;
            text-align: right;
        }}
    </style>
    </head>
    <body>
    <div class="wrap">
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Driver</th>
                    <th>Constructor</th>
                    <th>Grid</th>
                    <th>Win Probability</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    </body>
    </html>
    """

    n_rows = len(df)
    table_height = 60 + (n_rows * 62)
    components.html(table_html, height=table_height, scrolling=False)