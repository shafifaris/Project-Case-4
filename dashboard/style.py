SIDEBAR_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── MAIN BACKGROUND ── */
.main { background-color: #FDF6EE !important; }
.block-container { padding: 2rem 2.5rem !important; background: #FDF6EE; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #5C0A1E !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(30,0,10,0.25);
}
[data-testid="stSidebar"] * { color: #FDF0DC !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: rgba(245,212,138,0.65) !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(245,212,138,0.2) !important;
    color: #FDF0DC !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #FDF0DC !important; }
[data-testid="stSidebar"] hr { border-color: rgba(245,212,138,0.15) !important; }

[data-testid="stSidebarNav"] { display: none !important; }

/* ── HIDE BRANDING ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── SECTION DIVIDER ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, #8B1A2E, #C9932A, transparent);
    margin: 28px 0 20px 0;
    border: none;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'DM Sans', sans-serif;
    color: #1A0A10;
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid #8B1A2E;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── KPI CARD ── */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(92,10,30,0.08);
    border: 1px solid #EBD9C0;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(92,10,30,0.15);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #8B1A2E, #C9932A);
}
.kpi-label {
    color: #8B7355;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    color: #1A0A10;
    font-size: 30px;
    font-weight: 400;
    line-height: 1.1;
}
.kpi-delta { font-size: 11px; margin-top: 6px; font-weight: 600; }
.kpi-green  { color: #1A7A4A; }
.kpi-yellow { color: #B45309; }
.kpi-red    { color: #B91C1C; }

/* ── CHART CARD ── */
.chart-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(92,10,30,0.06);
    border: 1px solid #EBD9C0;
    margin-bottom: 20px;
}

/* ── TOUCHPOINT CARD ── */
.tp-card {
    background: white;
    border: 1px solid #EBD9C0;
    border-radius: 10px;
    padding: 14px 10px;
    text-align: center;
    box-shadow: 0 1px 6px rgba(92,10,30,0.07);
    transition: transform 0.2s;
}
.tp-card:hover { transform: translateY(-2px); }
.tp-label {
    color: #8B7355;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
.tp-value {
    font-family: 'DM Serif Display', serif;
    font-size: 24px;
    font-weight: 400;
}
.tp-green  { color: #1A7A4A; }
.tp-yellow { color: #B45309; }
.tp-red    { color: #B91C1C; }
.tp-sub { color: #A0856A; font-size: 10px; margin-top: 4px; font-weight: 500; }

/* ── PAGE HEADER ── */
.page-header {
    background: linear-gradient(135deg, #5C0A1E 0%, #8B1A2E 100%);
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 24px;
    color: white;
    box-shadow: 0 4px 18px rgba(92,10,30,0.3);
}
.page-header-tag {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #C9932A;
    margin-bottom: 6px;
}
.page-header h2 {
    font-family: 'DM Serif Display', serif;
    color: #FDF0DC;
    font-size: 22px;
    font-weight: 400;
    margin: 0 0 4px 0;
}
.page-header p { color: rgba(253,240,220,0.6); font-size: 12px; margin: 0; }

/* ── HORIZONTAL TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 10px;
    padding: 5px;
    gap: 4px;
    box-shadow: 0 2px 10px rgba(92,10,30,0.08);
    border: 1px solid #EBD9C0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px !important;
    padding: 9px 18px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    color: #8B7355 !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: #8B1A2E !important;
    color: #FDF0DC !important;
    box-shadow: 0 2px 8px rgba(92,10,30,0.3) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #EBD9C0;
}
</style>
"""

PLOT_LIGHT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="DM Sans", color="#1A0A10", size=12),
)

MAROON_COLORS = [
    "#5C0A1E", "#8B1A2E", "#A82040", "#C9932A",
    "#E6B86A", "#F3D9A0", "#FDF0DC", "#EBD9C0",
]

ACCENT  = "#8B1A2E"   # maroon utama
GOLD    = "#C9932A"   # gold accent
SUCCESS = "#1A7A4A"   # hijau
WARNING = "#B45309"   # amber
DANGER  = "#B91C1C"   # merah