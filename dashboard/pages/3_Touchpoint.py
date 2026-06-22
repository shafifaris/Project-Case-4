import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ══════════════════════════════════════════════════════════════════════════════
# CSS — match exact Overview style
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #F8F4F0 !important; }
.block-container { padding: 1.5rem 2rem 3rem; background: #F8F4F0; max-width: 1400px; }

[data-testid="stSidebar"] {
    background: #3D0812 !important;
    border-right: none !important;
    box-shadow: 4px 0 32px rgba(20,0,8,0.35);
}
[data-testid="sidebar-collapse-button"] {
    display: none !important;
}

[data-testid="stSidebar"] button {
    display: none !important;
}
[data-testid="stSidebar"] * { color: #FDF0DC !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(245,212,138,0.18) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #FDF0DC !important; }
[data-testid="stSidebar"] hr { border-color: rgba(245,212,138,0.12) !important; }
[data-testid="stSidebarNav"] { display: none !important; }
#MainMenu { visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }

.nav-label {
    color: rgba(245,212,138,0.45);
    font-size: 9.5px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.12em;
    padding: 0 0 5px 0; margin-top: 10px;
}
.nav-pill {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 12px; border-radius: 8px;
    color: rgba(253,240,220,0.55); font-size: 12.5px; font-weight: 500;
    text-decoration: none; margin-bottom: 2px;
    transition: all 0.15s; cursor: pointer;
    border-left: 3px solid transparent;
}
.nav-pill:hover { background: rgba(255,255,255,0.06); color: #FDF0DC; }
.nav-pill.active {
    background: rgba(201,147,42,0.15);
    color: #F5D48A !important; font-weight: 600;
    border-left: 3px solid #C9932A;
}

.page-header {
    background: linear-gradient(135deg, #3D0812 0%, #6B1020 60%, #8B1A2E 100%);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(61,8,18,0.30);
    position: relative; overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(201,147,42,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.page-header-tag {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.14em; color: #C9932A; margin-bottom: 8px;
}
.page-header h2 {
    font-family: 'DM Serif Display', serif;
    color: #FDF0DC; font-size: 24px; font-weight: 400; margin: 0 0 6px 0;
}
.page-header p { color: rgba(253,240,220,0.50); font-size: 12px; margin: 0; }

.section-label {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px; margin-top: 24px;
}
.section-label-text {
    color: #3D0812; font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; white-space: nowrap;
}
.section-label-line {
    flex: 1; height: 1px; background: linear-gradient(90deg, #C4A882, transparent);
}

/* Card bubble — wrapper untuk setiap chart/tabel */
.chart-card {
    background: white;
    border-radius: 14px;
    padding: 20px 20px 16px;
    border: 1px solid #E8D9C8;
    box-shadow: 0 2px 12px rgba(61,8,18,0.06);
    margin-bottom: 0;
    height: 100%;
}
.chart-card-title {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.09em; color: #9B7B5A; margin-bottom: 4px;
}
.chart-card-sub {
    font-size: 11px; color: #B8977A; margin-bottom: 14px; line-height: 1.5;
}

/* Health ranking card */
.tp-rank-row {
    display: flex; align-items: center; gap: 12px;
    padding: 9px 0; border-bottom: 1px solid #F3EBE1;
}
.tp-rank-row:last-child { border-bottom: none; }
.tp-rank-num {
    font-family: 'DM Serif Display', serif;
    font-size: 18px; color: #C9932A; width: 28px; flex-shrink: 0; text-align: center;
}
.tp-rank-name { font-size: 13px; font-weight: 600; color: #1A0A10; flex: 1; }
.tp-rank-bar-wrap { flex: 2; height: 8px; background: #F3EBE1; border-radius: 99px; overflow: hidden; }
.tp-rank-bar { height: 100%; border-radius: 99px; }
.tp-rank-val { font-family: 'DM Serif Display', serif; font-size: 16px; width: 52px; text-align: right; }
.tp-rank-badge { font-size: 9.5px; font-weight: 700; padding: 2px 7px; border-radius: 20px; flex-shrink: 0; }

/* Quadrant label card */
.quad-legend {
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px;
}
.quad-item {
    padding: 8px 10px; border-radius: 8px; font-size: 11px; font-weight: 600;
}

/* Pain point row */
.pain-section { margin-bottom: 16px; }
.pain-title {
    font-size: 11px; font-weight: 700; color: #3D0812;
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 8px; padding-bottom: 5px;
    border-bottom: 2px solid #F3EBE1;
}
.pain-row {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 0; border-bottom: 1px solid #FAF4EE;
}
.pain-row:last-child { border-bottom: none; }
.pain-rank { font-size: 10px; font-weight: 700; color: #C9932A; width: 18px; }
.pain-name { font-size: 12px; color: #374151; flex: 1; }
.pain-val { font-size: 12px; font-weight: 700; }

/* Service blueprint */
.bp-step {
    display: flex; align-items: center; gap: 0;
    margin-bottom: 0;
}
.bp-node {
    background: white; border: 2px solid #E8D9C8;
    border-radius: 12px; padding: 14px 16px;
    flex: 1; position: relative;
    box-shadow: 0 2px 8px rgba(61,8,18,0.05);
}
.bp-node.best { border-color: #15803D; }
.bp-node.critical { border-color: #B91C1C; }
.bp-arrow {
    font-size: 18px; color: #C4A882; margin: 0 4px; flex-shrink: 0;
}
.bp-label { font-size: 10px; font-weight: 700; color: #9B7B5A;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2px; }
.bp-score { font-family: 'DM Serif Display', serif; font-size: 26px; line-height: 1; }
.bp-status { font-size: 10px; font-weight: 600; margin-top: 3px; }

/* Waiting time summary card */
.wt-summary { display: flex; gap: 12px; margin-bottom: 14px; }
.wt-box {
    flex: 1; background: #FDF6EE; border-radius: 10px;
    padding: 10px 14px; border: 1px solid #E8D9C8;
}
.wt-box-label { font-size: 9.5px; font-weight: 700; color: #9B7B5A;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.wt-box-val { font-family: 'DM Serif Display', serif; font-size: 22px; line-height: 1; }
.wt-box-unit { font-size: 10px; color: #9B7B5A; margin-top: 2px; }
.wt-gap-positive { color: #B91C1C; }
.wt-gap-negative { color: #15803D; }

/* Driver impact badge */
.driver-row {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 0; border-bottom: 1px solid #F3EBE1;
}
.driver-row:last-child { border-bottom: none; }
.driver-name { font-size: 13px; font-weight: 600; color: #1A0A10; flex: 1; }
.driver-bar-wrap { flex: 2; height: 6px; background: #F3EBE1; border-radius: 99px; overflow: hidden; }
.driver-bar { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #3D0812, #8B1A2E); }
.driver-corr { font-size: 12px; font-weight: 700; color: #3D0812; width: 48px; text-align: right; }
.driver-impact { font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 20px; flex-shrink: 0; }
.impact-high { background: #FEE2E2; color: #991B1B; }
.impact-mid  { background: #FEF9C3; color: #854D0E; }
.impact-low  { background: #F3F4F6; color: #374151; }

[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #E8D9C8; }
[data-testid="stTabs"] [data-baseweb="tab-list"] { background: transparent; gap: 4px; }
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: white; border-radius: 8px 8px 0 0;
    border: 1px solid #E8D9C8; border-bottom: none;
    color: #9B7B5A; font-size: 12px; font-weight: 600;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #3D0812 !important; color: #FDF0DC !important;
    border-color: #3D0812 !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "..", "df_new.xlsx"))

    def parse_nps(v):
        if pd.isna(v) or str(v).strip() == '': return np.nan
        try: return int(str(v).strip().split()[0])
        except: return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)
    df['nps_category'] = df['nps_num'].apply(
        lambda v: 'Promoter' if v >= 9 else ('Passive' if v >= 7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    # Overall touchpoints + CSI
    overall_cols = [
        'csi_xyz',
        'overall_teller_xyz',   'overall_teller_komp',
        'overall_cs_xyz',       'overall_cs_komp',
        'overall_atm_xyz',      'overall_atm_komp',
        'overall_banking_hall_xyz', 'overall_banking_hall_komp',
        'overall_sekuriti_xyz', 'overall_sekuriti_komp',
        'overall_operasional_xyz','overall_operasional_komp',
        'overall_parkir_xyz',   'overall_parkir_komp',
        'overall_toilet_xyz',   'overall_toilet_komp',
        'waktu_tunggu_teller_aktual','waktu_tunggu_teller_toleransi',
        'waktu_ideal_tambah_teller',
        'waktu_tunggu_cs_aktual','waktu_tunggu_cs_toleransi',
        'waktu_ideal_tambah_cs',
    ]

    # Brand image (Performance di IPA)
    img_cols = [
        'img_terkenal_xyz','img_rasa_aman_xyz','img_dihargai_xyz','img_reputasi_xyz',
        'img_produk_lengkap_xyz','img_investasi_xyz','img_kemudahan_transaksi_xyz',
        'img_teknologi_xyz','img_reward_xyz','img_echannel_xyz',
    ]
    # Importance
    imp_cols = [
        'imp_terkenal','imp_rasa_aman','imp_dihargai','imp_reputasi',
        'imp_produk_lengkap','imp_investasi','imp_kemudahan_transaksi',
        'imp_teknologi','imp_reward','imp_echannel',
    ]

    # Teller attrs
    teller_attrs = sorted([c for c in df.columns if c.startswith('tp_teller_') and c.endswith('_xyz')])
    cs_attrs     = sorted([c for c in df.columns if c.startswith('tp_cs_')     and c.endswith('_xyz')])
    atm_attrs    = sorted([c for c in df.columns if c.startswith('tp_atm_')    and c.endswith('_xyz')])
    bh_attrs     = sorted([c for c in df.columns if c.startswith('tp_bh_')     and c.endswith('_xyz')])
    satpam_attrs = sorted([c for c in df.columns if c.startswith('tp_satpam_') and c.endswith('_xyz')])
    ca_attrs     = sorted([c for c in df.columns if c.startswith('tp_ca_')     and c.endswith('_xyz')])

    all_tp_attrs = teller_attrs + cs_attrs + atm_attrs + bh_attrs + satpam_attrs + ca_attrs

    for c in overall_cols + img_cols + imp_cols + all_tp_attrs:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Convert scale 1-6 → 0-100 for overall + tp attrs
    scale6_cols = [c for c in overall_cols if c not in (
        'waktu_tunggu_teller_aktual','waktu_tunggu_teller_toleransi','waktu_ideal_tambah_teller',
        'waktu_tunggu_cs_aktual','waktu_tunggu_cs_toleransi','waktu_ideal_tambah_cs'
    )]
    for c in scale6_cols + all_tp_attrs:
        if c in df.columns:
            df[c + '_pct'] = (df[c] / 6 * 100).round(1)

    return df, teller_attrs, cs_attrs, atm_attrs, bh_attrs, satpam_attrs, ca_attrs, img_cols, imp_cols

df_raw, teller_attrs, cs_attrs, atm_attrs, bh_attrs, satpam_attrs, ca_attrs, img_cols, imp_cols = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 10px 14px;border-bottom:1px solid rgba(245,212,138,0.12);margin-bottom:14px;'>
        <div style='font-family:"DM Serif Display",serif;font-size:21px;color:#F5D48A;'>Bank XYZ</div>
        <div style='font-size:9.5px;color:rgba(245,212,138,0.45);margin-top:3px;
                    text-transform:uppercase;letter-spacing:0.1em;'>
            Customer Experience Intelligence
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='nav-label'>Menu</div>", unsafe_allow_html=True)
    pages = {
        "Overview":            "/Overview",
        "Branch Intelligence": "/Branch_Intelligence",
        "Touchpoint":          "/Touchpoint",
        "Customer Behaviour":  "/Customer_Behaviour",
        "Competitor":          "/Competitor",
    }
    icons = {"Overview":"◈","Branch Intelligence":"▣","Touchpoint":"◎",
             "Customer Behaviour":"◉","Competitor":"◆"}
    for name, path in pages.items():
        active = "active" if name == "Touchpoint" else ""
        st.markdown(
            f"<a href='{path}' target='_self' class='nav-pill {active}'>"
            f"<span>{icons[name]}</span><span>{name}</span></a>",
            unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(245,212,138,0.12);margin:16px 0;'>",
                unsafe_allow_html=True)
    st.markdown("<div class='nav-label'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.multiselect("Provinsi", prov_opts, placeholder="Semua Provinsi")

    if sel_prov:
        pool = df_raw[df_raw["provinsi"].isin(sel_prov)]
    else:
        pool = df_raw
    
    kota_opts = sorted(pool["kab_kota"].dropna().unique().tolist())
    sel_kota = st.multiselect("Kota/Kabupaten", kota_opts, placeholder="Semua Kota/Kab")
    if sel_kota:
        pool2 = pool[pool["kab_kota"].isin(sel_kota)]
    else:
        pool2 = pool
    

    branch_opts = sorted(pool["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect("Cabang", branch_opts, placeholder="Semua Cabang")

    panel_opts = ["Semua", "Teller", "CS"]
    sel_panel = st.selectbox("Panel", panel_opts)

    # ── UBAH MENJADI MULTISELECT ──
    usia_opts = sorted(df_raw["range_usia"].dropna().unique().tolist())
    sel_usia = st.multiselect("Usia", usia_opts, placeholder="Semua Usia")

    st.markdown("<hr style='border-color:rgba(245,212,138,0.12);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:9.5px;color:rgba(245,212,138,0.30);padding:0 4px;'>v3.1 · Bank XYZ Analytics</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov and "Semua" not in sel_prov:   
    df = df[df["provinsi"].isin(sel_prov)]
if sel_kota:
    df = df[df["kab_kota"].isin(sel_kota)]
if sel_branch:             df = df[df["nama_cabang"].isin(sel_branch)]
if sel_panel != "Semua":
    panel_map = {"Teller": "Teller (KUOTA 50%)", "CS": "CS (KUOTA 50%)"}
    df = df[df["panel_transaksi"] == panel_map[sel_panel]]
if sel_usia:
    df = df[df["range_usia"].isin(sel_usia)]

n = len(df)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0

def pct_label(v): return "Baik" if v >= 80 else ("Perlu Perhatian" if v >= 65 else "Kritis")
def pct_color(v): return "#15803D" if v >= 80 else ("#B45309" if v >= 65 else "#B91C1C")
def pct_bg(v):    return "#DCFCE7" if v >= 80 else ("#FEF9C3" if v >= 65 else "#FEE2E2")
def pct_txt(v):   return "#166534" if v >= 80 else ("#854D0E" if v >= 65 else "#991B1B")

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color="#5C3D2E", size=11),
)

# Clean label dari nama kolom
def clean_label(col, prefix):
    lbl = col.replace(prefix, "").replace("_xyz", "").replace("_", " ").title()
    return lbl

# ══════════════════════════════════════════════════════════════════════════════
# TOUCHPOINT DATA MASTER
# ══════════════════════════════════════════════════════════════════════════════
TOUCHPOINTS = [
    ("Sekuriti",     "overall_sekuriti_xyz",      "overall_sekuriti_komp",      "🛡️"),
    ("Banking Hall", "overall_banking_hall_xyz",  "overall_banking_hall_komp",  "🏛️"),
    ("Teller",       "overall_teller_xyz",        "overall_teller_komp",        "🏧"),
    ("Customer Svc", "overall_cs_xyz",            "overall_cs_komp",            "🎧"),
    ("ATM",          "overall_atm_xyz",           "overall_atm_komp",           "💳"),
    ("Operasional",  "overall_operasional_xyz",   "overall_operasional_komp",   "⚙️"),
    ("Parkir",       "overall_parkir_xyz",        "overall_parkir_komp",        "🅿️"),
    ("Toilet",       "overall_toilet_xyz",        "overall_toilet_komp",        "🚿"),
]

# Journey order untuk blueprint (sesuai urutan fisik nasabah)
BLUEPRINT_ORDER = [
    ("Parkir",       "overall_parkir_xyz"),
    ("Banking Hall", "overall_banking_hall_xyz"),
    ("Sekuriti",     "overall_sekuriti_xyz"),
    ("Teller",       "overall_teller_xyz"),
    ("Customer Svc", "overall_cs_xyz"),
    ("ATM",          "overall_atm_xyz"),
]

tp_data = []
for label, col_xyz, col_komp, icon in TOUCHPOINTS:
    val_xyz  = round(safe_mean(df[col_xyz])  / 6 * 100, 1) if col_xyz  in df.columns else 0.0
    val_komp = round(safe_mean(df[col_komp]) / 6 * 100, 1) if col_komp in df.columns else 0.0
    tp_data.append({
        "label": label, "icon": icon,
        "xyz": val_xyz, "komp": val_komp,
        "col_xyz": col_xyz, "col_komp": col_komp,
    })

tp_sorted = sorted(tp_data, key=lambda x: x["xyz"], reverse=True)

# IPA pairs: imp_ ↔ img_  (yang punya pasangan)
IPA_PAIRS = [
    ("Terkenal",             "imp_terkenal",             "img_terkenal_xyz"),
    ("Rasa Aman",            "imp_rasa_aman",            "img_rasa_aman_xyz"),
    ("Dihargai",             "imp_dihargai",             "img_dihargai_xyz"),
    ("Reputasi",             "imp_reputasi",             "img_reputasi_xyz"),
    ("Produk Lengkap",       "imp_produk_lengkap",       "img_produk_lengkap_xyz"),
    ("Investasi",            "imp_investasi",            "img_investasi_xyz"),
    ("Kemudahan Transaksi",  "imp_kemudahan_transaksi",  "img_kemudahan_transaksi_xyz"),
    ("Teknologi",            "imp_teknologi",            "img_teknologi_xyz"),
    ("Reward",               "imp_reward",               "img_reward_xyz"),
    ("E-Channel",            "imp_echannel",             "img_echannel_xyz"),
]

# Deep-dive per touchpoint
DEEPDIVE_MAP = {
    "Teller":       (teller_attrs,  "tp_teller_",  "_xyz"),
    "Customer Svc": (cs_attrs,      "tp_cs_",      "_xyz"),
    "ATM":          (atm_attrs,     "tp_atm_",     "_xyz"),
    "Banking Hall": (bh_attrs,      "tp_bh_",      "_xyz"),
    "Sekuriti":     (satpam_attrs,  "tp_satpam_",  "_xyz"),
    "CA":           (ca_attrs,      "tp_ca_",      "_xyz"),
}

# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">◎ Bank XYZ · Touchpoint Intelligence</div>
    <h2>Touchpoint Analysis</h2>
    <p>{n:,} responden &nbsp;·&nbsp; {df['nama_cabang'].nunique()} kantor cabang
       &nbsp;·&nbsp; {df['provinsi'].nunique()} provinsi</p>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — DRIVER ANALYSIS (korelasi vs NPS)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">§2 · Driver Analysis — Impact terhadap NPS</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_drv, col_ipa = st.columns([2, 3])

corr_rows = []
for tp in tp_data:
    col = tp["col_xyz"] + "_pct"
    if col in df.columns and "nps_num" in df.columns:
        sub = df[[col, "nps_num"]].dropna()
        if len(sub) > 10:
            c = sub.corr().iloc[0, 1]
            corr_rows.append({"label": tp["label"], "icon": tp["icon"],
                              "corr": round(c, 3), "xyz": tp["xyz"]})

corr_df = pd.DataFrame(corr_rows).sort_values("corr", ascending=False) if corr_rows else pd.DataFrame()

with col_drv:
    if not corr_df.empty:
        impact_labels = []
        for c in corr_df["corr"]:
            if c >= 0.35:
                impact_labels.append("Tinggi")
            elif c >= 0.15:
                impact_labels.append("Sedang")
            else:
                impact_labels.append("Rendah")

        fig_drv2 = go.Figure()

        # bubble background
        fig_drv2.add_trace(go.Scatter(
            x=corr_df["corr"],
            y=corr_df["label"],
            mode="markers",
            marker=dict(
                size=32,
                color=["rgba(139,26,46,0.12)" if c >= 0.35
                       else "rgba(201,147,42,0.12)" if c >= 0.15
                       else "rgba(209,213,219,0.15)"
                       for c in corr_df["corr"]],
                line=dict(width=0),
            ),
            hoverinfo="skip",
            showlegend=False,
        ))

        # stem (garis dari 0 ke titik)
        for i, (_, row) in enumerate(corr_df.iterrows()):
            clr = "#8B1A2E" if row["corr"] >= 0.35 else "#C9932A" if row["corr"] >= 0.15 else "#D1D5DB"
            fig_drv2.add_shape(
                type="line",
                x0=0, x1=row["corr"],
                y0=row["label"], y1=row["label"],
                line=dict(color=clr, width=2),
            )

        # lollipop dot
        fig_drv2.add_trace(go.Scatter(
            x=corr_df["corr"],
            y=corr_df["label"],
            mode="markers+text",
            marker=dict(
                size=14,
                color=["#8B1A2E" if c >= 0.35
                       else "#C9932A" if c >= 0.15
                       else "#D1D5DB"
                       for c in corr_df["corr"]],
                line=dict(color="white", width=2),
            ),
            text=[f"r={v:.3f}  {lbl}"
                  for v, lbl in zip(corr_df["corr"], impact_labels)],
            textposition="middle right",
            textfont=dict(size=10, color="#5C3D2E"),
            hovertemplate="<b>%{y}</b><br>Korelasi: %{x:.3f}<extra></extra>",
            showlegend=False,
        ))

        fig_drv2.add_vline(
            x=0.35, line_dash="dot",
            line=dict(color="#8B1A2E", width=1.5),
            annotation_text="Threshold Tinggi (0.35)",
            annotation_font=dict(size=9, color="#8B1A2E"),
        )

        fig_drv2.update_layout(
            **PLOT,
            xaxis=dict(
                title="Korelasi Pearson (r)",
                range=[-0.05, max(corr_df["corr"].max() + 0.25, 0.6)],
                gridcolor="#F3EBE1",
                tickfont=dict(color="#9B7B5A"),
                zeroline=True,
                zerolinecolor="#E8D9C8",
                zerolinewidth=1.5,
            ),
            yaxis=dict(tickfont=dict(color="#3D0812", size=12)),
            margin=dict(t=10, b=10, l=10, r=80),
            height=460,
        )

        st.markdown("""
        <div style="background:white;border:1px solid #E8D9C8;border-radius:14px;
                    padding:16px 20px 4px;box-shadow:0 2px 12px rgba(61,8,18,0.06);
                    height:88px;overflow:hidden;">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.09em;color:#9B7B5A;margin-bottom:2px;">
                Pengaruh Touchpoint → NPS
            </div>
            <div style="font-size:11px;color:#B8977A;margin-bottom:2px;">
                Korelasi Pearson · Merah = Tinggi · Emas = Sedang · Abu = Rendah
            </div>
        </div>""", unsafe_allow_html=True)
        st.plotly_chart(fig_drv2, use_container_width=True, key="drv_left")

ipa_rows = []
for label, imp_col, perf_col in IPA_PAIRS:
    imp_val  = round(safe_mean(df[imp_col])  / 6 * 100, 1) if imp_col  in df.columns else None
    perf_val = round(safe_mean(df[perf_col]) / 6 * 100, 1) if perf_col in df.columns else None
    if imp_val is not None and perf_val is not None:
        ipa_rows.append({
            "Atribut": label,
            "Importance": imp_val,
            "Performance": perf_val,
        })

with col_ipa:
    if ipa_rows:
        ipa_df = pd.DataFrame(ipa_rows)
        avg_i = ipa_df["Importance"].mean()
        avg_p = ipa_df["Performance"].mean()

        def get_quadrant(row):
            if row["Importance"] >= avg_i and row["Performance"] < avg_p:
                return "Priority Improvement", "#FEE2E2", "#991B1B"
            elif row["Importance"] >= avg_i and row["Performance"] >= avg_p:
                return "Maintain Performance", "#DCFCE7", "#166534"
            elif row["Importance"] < avg_i and row["Performance"] >= avg_p:
                return "Possible Overkill", "#FEF9C3", "#854D0E"
            else:
                return "Low Priority", "#F3F4F6", "#6B7280"

        ipa_df[["Quadrant","QBG","QTX"]] = ipa_df.apply(
            lambda r: pd.Series(get_quadrant(r)), axis=1)

        QCOLORS = {
            "Priority Improvement": "#991B1B",
            "Maintain Performance": "#166534",
            "Possible Overkill":    "#92400E",
            "Low Priority":         "#374151",
        }

        fig_ipa = go.Figure()

        # Quadrant background shading
        # shading lebih tegas
        fig_ipa.add_shape(type="rect", x0=0, x1=avg_p, y0=avg_i, y1=110,
                          fillcolor="rgba(185,28,28,0.10)", line_width=0)
        fig_ipa.add_shape(type="rect", x0=avg_p, x1=110, y0=avg_i, y1=110,
                          fillcolor="rgba(21,128,61,0.10)", line_width=0)
        fig_ipa.add_shape(type="rect", x0=0, x1=avg_p, y0=0, y1=avg_i,
                          fillcolor="rgba(107,114,128,0.10)", line_width=0)
        fig_ipa.add_shape(type="rect", x0=avg_p, x1=110, y0=0, y1=avg_i,
                          fillcolor="rgba(146,64,14,0.10)", line_width=0)

        for q, clr in QCOLORS.items():
            sub = ipa_df[ipa_df["Quadrant"] == q]
            if sub.empty: continue
            fig_ipa.add_trace(go.Scatter(
                x=sub["Performance"], y=sub["Importance"],
                mode="markers+text",
                name=q,
                marker=dict(
                    size=18, color=clr,
                    line=dict(color="white", width=2),
                    symbol="circle",
                ),
                text=sub["Atribut"],
                textposition="top center",
                textfont=dict(size=10, color="#3D0812"),
            ))

        fig_ipa.add_vline(x=avg_p, line_dash="dash",
                          line=dict(color="#C4A882", width=1.5))
        fig_ipa.add_hline(y=avg_i, line_dash="dash",
                          line=dict(color="#C4A882", width=1.5))

        for lbl, xf, yf, clr in [
            ("PRIORITY\nIMPROVEMENT", 0.20, 0.93, "#B91C1C"),
            ("MAINTAIN\nPERFORMANCE", 0.78, 0.93, "#15803D"),
            ("LOW PRIORITY",           0.20, 0.07, "#6B7280"),
            ("POSSIBLE OVERKILL",      0.78, 0.07, "#B45309"),
        ]:
            fig_ipa.add_annotation(
                xref="paper", yref="paper", x=xf, y=yf,
                text=lbl.replace("\n","<br>"),
                showarrow=False,
                font=dict(size=8, color=clr, family="Inter"),
                opacity=0.6,
            )

        fig_ipa.update_layout(
            **PLOT,
            xaxis=dict(
                title="Performance — Brand Image Score (%)",
                range=[94, 100],
                gridcolor="#F3EBE1",
                ticksuffix="%",
                tickfont=dict(color="#9B7B5A"),
            ),
            yaxis=dict(
                title="Importance Score (%)",
                range=[94, 100],
                gridcolor="#F3EBE1",
                ticksuffix="%",
                tickfont=dict(color="#9B7B5A"),
            ),
            legend=dict(
                orientation="h", y=-0.18, x=0.5, xanchor="center",
                font=dict(size=10, color="#5C3D2E"),
                bgcolor="rgba(0,0,0,0)",
            ),
            margin=dict(t=10, b=60, l=10, r=10),
            height=460,  # sama dengan lollipop
        )
        st.markdown('''<div class="chart-card" style="height:88px;overflow:hidden;">
                    <div class="chart-card-title">IPA Matrix — Importance vs Performance</div>
                    <div class="chart-card-sub">
                    Importance: rata-rata skor imp_ (skala 1-6→%). 
                    Performance: rata-rata skor img_xyz (skala 1-6→%). 
                    Garis putus = rata-rata masing-masing sumbu.
                    </div>
                    </div>''', unsafe_allow_html=True)
        st.plotly_chart(fig_ipa, use_container_width=True, key="ipa_matrix")
# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — WAITING TIME ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">§4 · Waiting Time Analysis</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_wt1, col_wt2 = st.columns(2)

def render_waiting_card(col_obj, service, col_aktual, col_toleransi, col_ideal,
                        bar_color, chart_key):
    aktual_mean    = round(safe_mean(df[col_aktual]),   1)  if col_aktual    in df.columns else 0.0
    toleransi_mean = round(safe_mean(df[col_toleransi]),1)  if col_toleransi in df.columns else 0.0
    ideal_mean     = round(safe_mean(df[col_ideal]),    1)  if col_ideal     in df.columns else 0.0
    gap = round(aktual_mean - toleransi_mean, 1)
    gap_sign = "+" if gap >= 0 else ""
    gap_cls  = "wt-gap-positive" if gap > 0 else "wt-gap-negative"
    gap_label = f"Melebihi toleransi {abs(gap)} mnt" if gap > 0 else f"<=toleransi {abs(gap)} mnt"

    with col_obj:
        st.markdown(f"""
        <div class="chart-card">
            <div class="chart-card-title">⏱ Waiting Time · {service}</div>
            <div class="chart-card-sub">Aktual vs Toleransi nasabah</div>
            <div class="wt-summary">
                <div class="wt-box">
                    <div class="wt-box-label">Aktual</div>
                    <div class="wt-box-val" style="color:#B91C1C;">{aktual_mean}</div>
                    <div class="wt-box-unit">menit</div>
                </div>
                <div class="wt-box">
                    <div class="wt-box-label">Toleransi</div>
                    <div class="wt-box-val" style="color:#15803D;">{toleransi_mean}</div>
                    <div class="wt-box-unit">menit</div>
                </div>
                <div class="wt-box">
                    <div class="wt-box-label">Gap</div>
                    <div class="wt-box-val {gap_cls}">{gap_sign}{gap}</div>
                    <div class="wt-box-unit">{gap_label}</div>
                </div>
                <div class="wt-box">
                    <div class="wt-box-label">Ideal Tambah Staf</div>
                    <div class="wt-box-val" style="color:#C9932A;">{ideal_mean}</div>
                    <div class="wt-box-unit">menit</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Chart per cabang
        wt_sub = df[["nama_cabang", col_aktual, col_toleransi]].dropna()
        if len(wt_sub) > 0:
            wt_grp = wt_sub.groupby("nama_cabang").mean().reset_index()
            wt_grp = wt_grp.sort_values(col_aktual, ascending=False).head(15)
            marker_clrs = [
                "#B91C1C" if a > t else "#15803D"
                for a, t in zip(wt_grp[col_aktual], wt_grp[col_toleransi])
            ]
            fig_wt = go.Figure()
            fig_wt.add_trace(go.Bar(
                name="Aktual", x=wt_grp["nama_cabang"], y=wt_grp[col_aktual],
                marker=dict(color=marker_clrs, line=dict(color="white", width=1)),
            ))
            fig_wt.add_trace(go.Scatter(
                name="Toleransi", x=wt_grp["nama_cabang"], y=wt_grp[col_toleransi],
                mode="lines+markers",
                line=dict(color="#C9932A", dash="dash", width=2),
                marker=dict(size=6, color="#C9932A"),
            ))
            fig_wt.update_layout(
                **PLOT,
                xaxis=dict(
                    tickangle=-35, tickfont=dict(size=9, color="#9B7B5A"),
                    gridcolor="#F3EBE1",
                ),
                yaxis=dict(
                    title="Menit",
                    gridcolor="#F3EBE1",
                    tickfont=dict(color="#9B7B5A"),
                ),
                legend=dict(
                    orientation="h", y=-0.3, x=0.5, xanchor="center",
                    font=dict(size=10, color="#5C3D2E"),
                ),
                margin=dict(t=10, b=80, l=10, r=10),
                height=300,
            )
            st.markdown('<div class="chart-card" style="margin-top:10px;">'
                        f'<div class="chart-card-title">Per Cabang — {service} (Top 15 Tunggu Terlama)</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(fig_wt, use_container_width=True, key=chart_key)
            st.markdown('</div>', unsafe_allow_html=True)

render_waiting_card(col_wt1, "Teller",
                    "waktu_tunggu_teller_aktual", "waktu_tunggu_teller_toleransi",
                    "waktu_ideal_tambah_teller", "#8B1A2E", "wt_teller")
render_waiting_card(col_wt2, "Customer Service",
                    "waktu_tunggu_cs_aktual", "waktu_tunggu_cs_toleransi",
                    "waktu_ideal_tambah_cs", "#C9932A", "wt_cs")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — PAIN POINT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def render_html(html: str, container=None):
    """
    Helper untuk fix bug Streamlit: HTML multi-baris BERINDENTASI di dalam
    st.markdown() bisa dibaca parser Markdown sebagai code-block (rule: baris
    yang diawali >=4 spasi = preformatted text), sehingga HTML-nya muncul
    sebagai teks mentah, bukan dirender.

    Fix: strip leading whitespace di SETIAP baris sebelum dikirim ke st.markdown.
    Ini lebih aman daripada textwrap.dedent() karena tetap berfungsi walau
    string HTML-nya disusun dari potongan f-string bersarang (seperti rows_html
    di bawah) yang level indentasinya tidak konsisten.
    """
    cleaned = "\n".join(line.lstrip() for line in html.strip().split("\n"))
    target = container if container is not None else st
    target.markdown(cleaned, unsafe_allow_html=True)


render_html("""<div class="section-label">
<span class="section-label-text">§5 · Pain Point Analysis — 5 Atribut Terendah per Touchpoint</span>
<div class="section-label-line"></div>
</div>""")

PAIN_MAP = {
    "ATM":          (atm_attrs,     "tp_atm_",     "💳"),
    "Customer Svc": (cs_attrs,      "tp_cs_",      "🎧"),
    "Teller":       (teller_attrs,  "tp_teller_",  "🏧"),
    "Banking Hall": (bh_attrs,      "tp_bh_",      "🏛️"),
    "Sekuriti":     (satpam_attrs,  "tp_satpam_",  "🛡️"),
    "CA":           (ca_attrs,      "tp_ca_",      "🧑‍💼"),
}

pain_cols = st.columns(6)

for col_pain, (tp_label, (attrs_list, prefix_str, icon)) in zip(pain_cols, PAIN_MAP.items()):
    avail = [c for c in attrs_list if c in df.columns]
    if not avail:
        render_html("""
        <div style="background:white;border:1px solid #E8D9C8;border-radius:14px;
                    padding:16px 14px;box-shadow:0 2px 12px rgba(61,8,18,0.06);
                    min-height:260px;display:flex;align-items:center;justify-content:center;">
            <div style="text-align:center;color:#C4A882;font-size:11px;">Tidak ada data</div>
        </div>""", container=col_pain)
        continue

    pain_rows = []
    for col in avail:
        pct_col = col + "_pct"
        val = round(
            safe_mean(df[pct_col]) if pct_col in df.columns
            else safe_mean(df[col]) / 6 * 100, 1
        )
        lbl = clean_label(col, prefix_str).replace(" Xyz", "").strip()
        pain_rows.append({"attr": lbl, "val": val})

    pain_df_plot = pd.DataFrame(pain_rows).sort_values("val").head(5).reset_index(drop=True)
    max_v = pain_df_plot["val"].max() if len(pain_df_plot) > 0 else 1

    rows_html = ""
    for i, row in pain_df_plot.iterrows():
        v       = row["val"]
        bar_w   = int(v / 100 * 100)
        bar_clr = pct_color(v)
        bg_lbl  = pct_bg(v)
        tx_lbl  = pct_txt(v)
        badge_cls = "top1" if i == 0 else ("top2" if i == 1 else ("top3" if i == 2 else ""))
        rank_style = (
            "background:#B91C1C;color:white;" if i == 0 else
            "background:#B45309;color:white;" if i == 1 else
            "background:#F3EBE1;color:#9B7B5A;"
        )
        rows_html += f"""
        <tr style="height: 48px;"> <td style="padding:4px 4px 4px 0;vertical-align:middle;width:20px;">
                <span style="display:inline-flex;align-items:center;justify-content:center;
                             width:18px;height:18px;border-radius:50%;font-size:9px;
                             font-weight:700;flex-shrink:0;{rank_style}">
                    {i+1}
                </span>
            </td>
            <td style="padding:4px 4px;vertical-align:middle;">
                <div style="font-size:10.5px;font-weight:{'700' if i==0 else '500'};
                            color:#1A0A10;line-height:1.2; min-height: 26px; display: flex; align-items: center;">
                    {row['attr']}
                </div>
                <div style="margin-top:4px;height:4px;background:#F3EBE1;
                            border-radius:99px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:{bar_clr};
                                border-radius:99px;"></div>
                </div>
            </td>
            <td style="padding:4px 0 4px 4px;vertical-align:middle;
                       text-align:right;white-space:nowrap;width:45px;">
                <span style="font-family:'DM Serif Display',serif;font-size:13px;
                             color:{bar_clr};font-weight:700;">
                    {v}%
                </span>
            </td>
        </tr>"""

    render_html(f"""
    <div style="background:white;border:1px solid #E8D9C8;border-radius:14px;
                padding:16px 14px 10px;box-shadow:0 2px 12px rgba(61,8,18,0.06);
                height:100%;">
        <div style="font-size:16px;margin-bottom:4px;">{icon}</div>
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.09em;color:#3D0812;margin-bottom:2px;">
            {tp_label}
        </div>
        <div style="font-size:10px;color:#C4A882;margin-bottom:10px;
                    padding-bottom:8px;border-bottom:1px solid #F3EBE1;">
            5 atribut terendah
        </div>
        <table style="width:100%;border-collapse:collapse;table-layout:fixed;">
            {rows_html}
        </table>
    </div>""", container=col_pain)
# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — SERVICE BLUEPRINT (Customer Journey)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">§6 · Service Blueprint — Customer Journey</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

bp_data = []
for label, col in BLUEPRINT_ORDER:
    val = round(safe_mean(df[col]) / 6 * 100, 1) if col in df.columns else 0.0
    bp_data.append({"label": label, "val": val, "col": col})

best_val  = max(d["val"] for d in bp_data) if bp_data else 100
worst_val = min(d["val"] for d in bp_data) if bp_data else 0

# Horizontal journey bar
fig_bp = go.Figure()
bp_colors = []
for d in bp_data:
    if d["val"] == best_val:   bp_colors.append("#15803D")
    elif d["val"] == worst_val: bp_colors.append("#B91C1C")
    elif d["val"] < 65:        bp_colors.append("#B91C1C")
    elif d["val"] < 80:        bp_colors.append("#B45309")
    else:                      bp_colors.append("#15803D")

fig_bp.add_trace(go.Bar(
    x=[d["label"] for d in bp_data],
    y=[d["val"]   for d in bp_data],
    marker=dict(
        color=bp_colors,
        line=dict(color="white", width=2),
        cornerradius=6,
    ),
    text=[f"<b>{d['val']}%</b><br><span style='font-size:9px'>{pct_label(d['val'])}</span>"
          for d in bp_data],
    textposition="inside",
    textfont=dict(size=11, color="white"),
    width=0.55,
))
fig_bp.add_hline(y=80, line_dash="dot", line_color="#15803D",
                 annotation_text="Target 80%",
                 annotation_font=dict(size=9, color="#15803D"))
fig_bp.add_hline(y=65, line_dash="dot", line_color="#B45309",
                 annotation_text="Batas Kritis 65%",
                 annotation_font=dict(size=9, color="#B45309"))

# Arrow annotations between bars
for i in range(len(bp_data) - 1):
    fig_bp.add_annotation(
        x=i + 0.5, y=max(bp_data[i]["val"], bp_data[i+1]["val"]) + 4,
        text="→", showarrow=False,
        font=dict(size=20, color="#C4A882"),
    )

fig_bp.update_layout(
    **PLOT,
    xaxis=dict(
        tickfont=dict(size=12, color="#3D0812", family="Inter"),
        gridcolor="rgba(0,0,0,0)",
    ),
    yaxis=dict(
        range=[0, 115], ticksuffix="%",
        gridcolor="#F3EBE1",
        tickfont=dict(color="#9B7B5A"),
        title="Skor (%)",
    ),
    margin=dict(t=20, b=10, l=10, r=10),
    height=360,
)

st.markdown('<div class="chart-card"><div class="chart-card-title">Perjalanan Nasabah — Skor per Tahap</div>'
            '<div class="chart-card-sub">'
            'Urutan berdasarkan journey fisik nasabah dari parkir hingga ATM. '
            'Identifikasi bottleneck di mana pengalaman mulai menurun.'
            '</div>', unsafe_allow_html=True)
st.plotly_chart(fig_bp, use_container_width=True, key="blueprint")


# Journey insight text
st.markdown("<br>", unsafe_allow_html=True)
bp_sorted_insight = sorted(bp_data, key=lambda x: x["val"])
worst_bp = bp_sorted_insight[0]
best_bp  = bp_sorted_insight[-1]

# Find where score drops
drop_point = None
for i in range(1, len(bp_data)):
    if bp_data[i]["val"] < bp_data[i-1]["val"] - 5:
        drop_point = bp_data[i]
        break

insight_html = f"""
<div style="background:white;border:1px solid #E8D9C8;border-radius:12px;
            padding:16px 20px;display:flex;gap:24px;flex-wrap:wrap;
            box-shadow:0 2px 8px rgba(61,8,18,0.05);">
    <div style="flex:1;min-width:200px;">
        <div style="font-size:9.5px;font-weight:700;color:#9B7B5A;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
            🏆 Touchpoint Terbaik
        </div>
        <div style="font-family:'DM Serif Display',serif;font-size:20px;color:#15803D;">
            {best_bp['label']}
        </div>
        <div style="font-size:12px;color:#15803D;font-weight:600;">{best_bp['val']}%</div>
    </div>
    <div style="flex:1;min-width:200px;">
        <div style="font-size:9.5px;font-weight:700;color:#9B7B5A;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">
            ⚠️ Touchpoint Terlemah
        </div>
        <div style="font-family:'DM Serif Display',serif;font-size:20px;color:#B91C1C;">
            {worst_bp['label']}
        </div>
        <div style="font-size:12px;color:#B91C1C;font-weight:600;">{worst_bp['val']}%</div>
    </div>
    {"<div style='flex:2;min-width:280px;'><div style='font-size:9.5px;font-weight:700;color:#9B7B5A;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>📉 Drop Signifikan Ditemukan</div><div style='font-size:13px;color:#3D0812;font-weight:500;'>Skor turun tajam di tahap <b>" + drop_point['label'] + f"</b> ({drop_point['val']}%). Ini titik di mana pengalaman nasabah mulai rusak.</div></div>" if drop_point else ''}
</div>"""
# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — BRANCH × TOUCHPOINT CRISIS TABLE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">§8 · Branch × Touchpoint Heatmap</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

crisis_map = {
    "CSI":         "csi_xyz_pct",
    "Teller":      "overall_teller_xyz_pct",
    "CS":          "overall_cs_xyz_pct",
    "ATM":         "overall_atm_xyz_pct",
    "Banking Hall":"overall_banking_hall_xyz_pct",
    "Sekuriti":    "overall_sekuriti_xyz_pct",
    "Operasional": "overall_operasional_xyz_pct",
    "Parkir":      "overall_parkir_xyz_pct",
    "Toilet":      "overall_toilet_xyz_pct",
}
avail_crisis = {k: v for k, v in crisis_map.items() if v in df.columns}

if avail_crisis:
    crisis_df = (
        df.groupby("nama_cabang")[list(avail_crisis.values())]
        .mean().round(1).reset_index()
    )
    crisis_df.columns = ["Cabang"] + list(avail_crisis.keys())
    num_sort = list(avail_crisis.keys())[0]
    crisis_df = crisis_df.sort_values(num_sort)

    def color_cell(val):
        if isinstance(val, (int, float)):
            if val < 65:   return "background-color:#FEE2E2;color:#991B1B;"
            elif val < 80: return "background-color:#FEF9C3;color:#854D0E;"
            else:          return "background-color:#DCFCE7;color:#166534;"
        return ""

    numeric_cols = [c for c in crisis_df.columns if c != "Cabang"]
    styled = crisis_df.style.map(color_cell, subset=numeric_cols)

    st.markdown('<div class="chart-card"><div class="chart-card-title">'
                'Heatmap Performa Cabang per Touchpoint</div>'
                '<div class="chart-card-sub">'
                'Merah &lt; 65% (Kritis) · Kuning 65–79% (Perhatian) · Hijau ≥ 80% (Baik)'
                '</div>', unsafe_allow_html=True)
    st.dataframe(styled, use_container_width=True, height=320)