import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ── CSS & STYLE (matches Overview) ───────────────────────────────────────────
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

/* Page Header */
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

/* Section label */
.section-label {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px; margin-top: 4px;
}
.section-label-text {
    color: #3D0812; font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; white-space: nowrap;
}
.section-label-line {
    flex: 1; height: 1px; background: linear-gradient(90deg, #C4A882, transparent);
}

/* Generic white card with bubble shadow */
.card {
    background: white;
    border-radius: 14px; padding: 20px 20px 16px;
    border: 1px solid #E8D9C8;
    box-shadow: 0 2px 12px rgba(61,8,18,0.06);
    position: relative; overflow: hidden;
    height: 100%;
}
.card-accent-maroon::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #3D0812, #8B1A2E);
}
.card-accent-gold::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #C9932A, #E6B86A);
}
.card-accent-teal::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #0F5E5A, #2D9B96);
}
.card-accent-red::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #991B1B, #EF4444);
}

/* KPI exec cards */
.exec-card {
    background: white;
    border-radius: 14px; padding: 20px 18px 16px;
    border: 1px solid #E8D9C8;
    box-shadow: 0 2px 12px rgba(61,8,18,0.06);
    position: relative; overflow: hidden;
    transition: transform 0.18s, box-shadow 0.18s;
    height: 100%;
}
.exec-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(61,8,18,0.12); }
.exec-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.exec-card.maroon::before { background: linear-gradient(90deg, #3D0812, #8B1A2E); }
.exec-card.gold::before   { background: linear-gradient(90deg, #C9932A, #E6B86A); }
.exec-card.teal::before   { background: linear-gradient(90deg, #0F5E5A, #2D9B96); }
.exec-card.red::before    { background: linear-gradient(90deg, #991B1B, #EF4444); }
.exec-icon  { font-size: 22px; margin-bottom: 10px; display: block; line-height: 1; }
.exec-label { color: #9B7B5A; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
.exec-value { font-family: 'DM Serif Display', serif; font-size: 36px; font-weight: 400; line-height: 1; margin-bottom: 6px; }
.exec-sub   { font-size: 11px; color: #9B7B5A; font-weight: 500; }
.exec-badge { display: inline-block; padding: 3px 8px; border-radius: 20px; font-size: 10px; font-weight: 700; margin-top: 8px; }
.badge-green  { background: #DCFCE7; color: #166534; }
.badge-yellow { background: #FEF9C3; color: #854D0E; }
.badge-red    { background: #FEE2E2; color: #991B1B; }

/* Rank table */
.rank-table { width: 100%; border-collapse: collapse; }
.rank-table th {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #9B7B5A; padding: 8px 10px;
    border-bottom: 2px solid #E8D9C8; text-align: left;
}
.rank-table th.right { text-align: right; }
.rank-table td { padding: 10px 10px; border-bottom: 1px solid #F3EBE1; font-size: 13px; color: #374151; }
.rank-table tr:last-child td { border-bottom: none; }
.rank-table tr:hover td { background: #FDF6EE; }
.rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 50%;
    font-family: 'DM Serif Display', serif; font-size: 14px;
    background: #F3EBE1; color: #3D0812; font-weight: 700;
}
.rank-badge.top1 { background: #3D0812; color: #F5D48A; }
.rank-badge.top2 { background: #6B1020; color: #FDF0DC; }
.rank-badge.top3 { background: #C9932A; color: white; }

/* Gap items */
.gap-item { display: flex; align-items: center; justify-content: space-between; padding: 9px 0; border-bottom: 1px solid #F3EBE1; }
.gap-item:last-child { border-bottom: none; }
.gap-label { font-size: 12.5px; color: #374151; font-weight: 500; }
.gap-bar-wrap { flex: 1; margin: 0 14px; }
.gap-val-pos { font-size: 12px; font-weight: 700; color: #15803D; min-width: 46px; text-align: right; }
.gap-val-neg { font-size: 12px; font-weight: 700; color: #B91C1C; min-width: 46px; text-align: right; }
.gap-val-neu { font-size: 12px; font-weight: 700; color: #3D0812; min-width: 46px; text-align: right; }

/* Opportunity matrix */
.opp-item {
    display: flex; align-items: center; gap: 14px;
    padding: 12px 14px; border-radius: 10px; margin-bottom: 8px;
    border: 1px solid #E8D9C8;
    background: white;
    box-shadow: 0 1px 4px rgba(61,8,18,0.04);
}
.opp-item:hover { background: #FDF6EE; }
.opp-rank {
    font-family: 'DM Serif Display', serif; font-size: 24px;
    color: #C9932A; min-width: 28px; text-align: center;
}
.opp-body { flex: 1; }
.opp-area { font-size: 13px; font-weight: 600; color: #1A0A10; }
.opp-meta { font-size: 11px; color: #9B7B5A; margin-top: 2px; }
.opp-pill {
    padding: 4px 12px; border-radius: 20px;
    font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
}
.pill-high   { background: #FEE2E2; color: #991B1B; }
.pill-med    { background: #FEF9C3; color: #854D0E; }
.pill-low    { background: #DCFCE7; color: #166534; }

/* Reason cards */
.reason-card { background: white; border-radius: 14px; padding: 16px 18px; border: 1px solid #E8D9C8; box-shadow: 0 2px 12px rgba(61,8,18,0.06); margin-bottom: 12px; }
.reason-title { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; margin-bottom: 10px; }
.reason-pos-title { color: #166534; }
.reason-neg-title { color: #991B1B; }
.reason-item { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #FAF4EE; font-size: 12px; color: #374151; }
.reason-item:last-child { border-bottom: none; }
.reason-count { font-weight: 700; color: #3D0812; }

/* Action cards */
.action-card { background: white; border-radius: 14px; padding: 18px 20px; border: 1px solid #E8D9C8; box-shadow: 0 2px 12px rgba(61,8,18,0.06); }
.action-item { display: flex; align-items: flex-start; gap: 12px; padding: 9px 10px; border-radius: 8px; margin-bottom: 6px; }
.action-item:hover { background: #FDF6EE; }
.action-item:last-child { margin-bottom: 0; }
.action-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 5px; }
.dot-red    { background: #EF4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.15); }
.dot-yellow { background: #F59E0B; box-shadow: 0 0 0 3px rgba(245,158,11,0.15); }
.dot-blue   { background: #3B82F6; box-shadow: 0 0 0 3px rgba(59,130,246,0.15); }
.dot-green  { background: #22C55E; box-shadow: 0 0 0 3px rgba(34,197,94,0.15); }
.action-title { font-size: 12.5px; font-weight: 600; color: #1A0A10; line-height: 1.4; }
.action-meta  { font-size: 10.5px; color: #9B7B5A; margin-top: 2px; }

[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #E8D9C8; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "..", "df_new.xlsx"))

    def parse_nps(val):
        if pd.isna(val) or str(val).strip() == '': return np.nan
        try: return int(str(val).strip().split()[0])
        except: return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)
    df['nps_komp_num'] = df['nps_kompetitor'].apply(parse_nps)

    num_cols = [
        'csi_xyz','cli_xyz','csi_kompetitor','cli_kompetitor',
        'overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
        'overall_banking_hall_xyz','overall_sekuriti_xyz',
        'overall_teller_komp','overall_cs_komp','overall_atm_komp',
        'overall_banking_hall_komp','overall_sekuriti_komp',
        'img_terkenal_xyz','img_rasa_aman_xyz','img_dihargai_xyz','img_reputasi_xyz',
        'img_produk_lengkap_xyz','img_investasi_xyz','img_kemudahan_transaksi_xyz',
        'img_teknologi_xyz','img_reward_xyz','img_echannel_xyz',
        'img_terkenal_komp','img_rasa_aman_komp','img_dihargai_komp','img_reputasi_komp',
        'img_produk_lengkap_komp','img_investasi_komp','img_kemudahan_transaksi_komp',
        'img_teknologi_komp','img_reward_komp','img_echannel_komp',
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    tp_pct_cols = [
        'csi_xyz','cli_xyz','csi_kompetitor','cli_kompetitor',
        'overall_teller_xyz','overall_cs_xyz','overall_atm_xyz',
        'overall_banking_hall_xyz','overall_sekuriti_xyz',
        'overall_teller_komp','overall_cs_komp','overall_atm_komp',
        'overall_banking_hall_komp','overall_sekuriti_komp',
    ]
    for c in tp_pct_cols:
        if c in df.columns:
            df[c + '_pct'] = (df[c] / 6 * 100).round(1)

    # Kompetitor touchpoint blank fix
    for c in ['overall_teller_komp','overall_cs_komp','overall_atm_komp',
              'overall_banking_hall_komp','overall_sekuriti_komp']:
        if c in df.columns:
            df[c] = df[c].replace(' ', np.nan)
            df[c] = pd.to_numeric(df[c], errors='coerce')
            df[c + '_pct'] = (df[c] / 6 * 100).round(1)

    return df

df_raw = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 10px 14px;border-bottom:1px solid rgba(245,212,138,0.12);margin-bottom:14px;'>
        <div style='font-family:"DM Serif Display",serif;font-size:21px;color:#F5D48A;'>Bank XYZ</div>
        <div style='font-size:9.5px;color:rgba(245,212,138,0.45);margin-top:3px;text-transform:uppercase;letter-spacing:0.1em;'>
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
    icons = {"Overview":"◈","Branch Intelligence":"▣","Touchpoint":"◎","Customer Behaviour":"◉","Competitor":"◆"}
    for name, path in pages.items():
        active = "active" if name == "Competitor" else ""
        st.markdown(
            f"<a href='{path}' target='_self' class='nav-pill {active}'>"
            f"<span>{icons[name]}</span><span>{name}</span></a>",
            unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(245,212,138,0.12);margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-label'>Filter Data</div>", unsafe_allow_html=True)

    prov_opts = sorted(df_raw["provinsi"].dropna().unique().tolist())
    sel_prov = st.multiselect("Provinsi", prov_opts,
                              placeholder="Semua Provinsi")

    if sel_prov:
        pool = df_raw[df_raw["provinsi"].isin(sel_prov)]
    else:
        pool = df_raw

    kota_opts = sorted(pool["kab_kota"].dropna().unique().tolist())
    sel_kota = st.multiselect(
        "Kota/Kabupaten", kota_opts, placeholder="Semua Kota/Kab")
    if sel_kota:
        pool2 = pool[pool["kab_kota"].isin(sel_kota)]
    else:
        pool2 = pool

    branch_opts = sorted(pool2["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect(
        "Cabang", branch_opts, placeholder="Semua Cabang")

    panel_opts = ["Semua", "Teller", "CS"]
    sel_panel = st.selectbox("Panel", panel_opts)

    usia_opts = sorted(df_raw["range_usia"].dropna().unique().tolist())
    sel_usia = st.multiselect("Usia", usia_opts, placeholder="Semua Usia")

    st.markdown("<hr style='border-color:rgba(245,212,138,0.12);margin:16px 0;'>",
                unsafe_allow_html=True)
    st.markdown("<div style='font-size:9.5px;color:rgba(245,212,138,0.30);padding:0 4px;'>v3.1 · Bank XYZ Analytics</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()

if sel_prov:
    df = df[df["provinsi"].isin(sel_prov)]
if sel_kota:
    df = df[df["kab_kota"].isin(sel_kota)]
if sel_branch:
    df = df[df["nama_cabang"].isin(sel_branch)]
if sel_panel != "Semua":
    panel_map = {"Teller": "Teller (KUOTA 50%)", "CS": "CS (KUOTA 50%)"}
    df = df[df["panel_transaksi"] == panel_map[sel_panel]]
if sel_usia:
    df = df[df["range_usia"].isin(sel_usia)]

n = len(df)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0

def pct_color(v): return "#15803D" if v >= 80 else ("#B45309" if v >= 65 else "#B91C1C")
def pct_label(v): return "Baik" if v >= 80 else ("Perlu Perhatian" if v >= 65 else "Kritis")
def badge_cls(v, hi, mid): return "badge-green" if v >= hi else ("badge-yellow" if v >= mid else "badge-red")

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color="#5C3D2E", size=11),
)

# ════════════════════════════════════════════════════════════════════════════
# COMPUTED METRICS
# ════════════════════════════════════════════════════════════════════════════

# NPS
nps_n    = int(df["nps_num"].notna().sum())
nps_komp_n = int(df["nps_komp_num"].notna().sum())
nps_xyz  = round(((df["nps_num"] >= 9).sum() - (df["nps_num"] <= 6).sum()) / max(nps_n, 1) * 100, 1)
nps_komp = round(((df["nps_komp_num"] >= 9).sum() - (df["nps_komp_num"] <= 6).sum()) / max(nps_komp_n, 1) * 100, 1)
nps_gap  = round(nps_xyz - nps_komp, 1)

# CSI / CLI
csi_xyz_val  = round(safe_mean(df["csi_xyz"]) / 6 * 100, 1)  if "csi_xyz"         in df.columns else 0.0
csi_komp_val = round(safe_mean(df["csi_kompetitor"]) / 6 * 100, 1) if "csi_kompetitor" in df.columns else 0.0
cli_xyz_val  = round(safe_mean(df["cli_xyz"]) / 6 * 100, 1)  if "cli_xyz"         in df.columns else 0.0
cli_komp_val = round(safe_mean(df["cli_kompetitor"]) / 6 * 100, 1) if "cli_kompetitor" in df.columns else 0.0

# Touchpoints
TOUCHPOINTS = [
    ("Teller",       "overall_teller_xyz",      "overall_teller_komp"),
    ("Customer Svc", "overall_cs_xyz",           "overall_cs_komp"),
    ("ATM",          "overall_atm_xyz",          "overall_atm_komp"),
    ("Banking Hall", "overall_banking_hall_xyz", "overall_banking_hall_komp"),
    ("Sekuriti",     "overall_sekuriti_xyz",     "overall_sekuriti_komp"),
]
tp_data = []
for label, col_xyz, col_komp in TOUCHPOINTS:
    v_xyz  = round(safe_mean(df[col_xyz + "_pct"])  if col_xyz  + "_pct" in df.columns else safe_mean(df[col_xyz]) / 6 * 100, 1) if col_xyz in df.columns else 0.0
    v_komp = round(safe_mean(df[col_komp + "_pct"]) if col_komp + "_pct" in df.columns else safe_mean(df[col_komp]) / 6 * 100, 1) if col_komp in df.columns else 0.0
    tp_data.append({"label": label, "xyz": v_xyz, "komp": v_komp, "gap": round(v_xyz - v_komp, 1)})

# Brand Image Gap
IMG_PAIRS = [
    ("Terkenal",             "img_terkenal_xyz",             "img_terkenal_komp"),
    ("Rasa Aman",            "img_rasa_aman_xyz",            "img_rasa_aman_komp"),
    ("Dihargai",             "img_dihargai_xyz",             "img_dihargai_komp"),
    ("Reputasi",             "img_reputasi_xyz",             "img_reputasi_komp"),
    ("Produk Lengkap",       "img_produk_lengkap_xyz",       "img_produk_lengkap_komp"),
    ("Investasi",            "img_investasi_xyz",            "img_investasi_komp"),
    ("Kemudahan Transaksi",  "img_kemudahan_transaksi_xyz",  "img_kemudahan_transaksi_komp"),
    ("Teknologi",            "img_teknologi_xyz",            "img_teknologi_komp"),
    ("Reward",               "img_reward_xyz",               "img_reward_komp"),
    ("E-Channel",            "img_echannel_xyz",             "img_echannel_komp"),
]
img_gap_data = []
for label, cxyz, ckomp in IMG_PAIRS:
    vx = safe_mean(df[cxyz])  if cxyz  in df.columns else 0.0
    vk = safe_mean(df[ckomp]) if ckomp in df.columns else 0.0
    img_gap_data.append({"label": label, "xyz": round(vx, 2), "komp": round(vk, 2), "gap": round(vx - vk, 2)})
img_gap_data.sort(key=lambda x: x["gap"])   # ascending — worst gap first

# Competitor landscape
def get_bank_list(col):
    series = df[col].dropna() if col in df.columns else pd.Series([], dtype=str)
    series = series[series.astype(str).str.strip() != ""]
    banks = []
    for val in series:
        for b in str(val).split(";"):
            b = b.strip()
            if b: banks.append(b)
    return pd.Series(banks).value_counts()

bank_aktif_counts = get_bank_list("bank_aktif_selain_xyz")
komp_dana_counts  = get_bank_list("kompetitor_simpan_dana")
komp_trx_counts   = get_bank_list("kompetitor_transaksi")

# Market share dominant
def top_bank(col):
    if col not in df.columns: return "N/A"
    s = df[col].dropna().astype(str).str.strip()
    s = s[s != ""]
    return s.value_counts().index[0] if len(s) > 0 else "N/A"

dominant_dana = top_bank("bank_utama_simpan_dana")
dominant_trx  = top_bank("bank_utama_transaksi")

def xyz_pct(col):
    if col not in df.columns: return 0.0
    s = df[col].dropna().astype(str).str.strip()
    if len(s) == 0: return 0.0
    return round((s == "Bank XYZ").mean() * 100, 1)

pct_dana = xyz_pct("bank_utama_simpan_dana")
pct_trx  = xyz_pct("bank_utama_transaksi")

# ════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">◆ Bank XYZ · Competitor Intelligence</div>
    <h2>Competitor Intelligence</h2>
    <p>{n:,} responden terfilter &nbsp;·&nbsp; Benchmarking vs kompetitor utama</p>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 1 — KPI SUMMARY (4 cards)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">KPI Summary — XYZ vs Kompetitor</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    sign = "+" if nps_gap >= 0 else ""
    bc = "badge-green" if nps_gap >= 0 else "badge-red"
    lbl = "Unggul" if nps_gap >= 0 else "Tertinggal"
    c1.markdown(f"""<div class="exec-card maroon">
        <span class="exec-icon">📊</span>
        <div class="exec-label">NPS Gap</div>
        <div class="exec-value" style="color:#3D0812;">{sign}{nps_gap}</div>
        <div class="exec-sub">XYZ {nps_xyz} · Komp {nps_komp}</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)

with c2:
    csi_gap = round(csi_xyz_val - csi_komp_val, 1)
    sign = "+" if csi_gap >= 0 else ""
    bc = "badge-green" if csi_gap >= 0 else "badge-red"
    lbl = "Unggul" if csi_gap >= 0 else "Tertinggal"
    c2.markdown(f"""<div class="exec-card gold">
        <span class="exec-icon">⭐</span>
        <div class="exec-label">CSI Gap (%)</div>
        <div class="exec-value" style="color:#7A5100;">{sign}{csi_gap}</div>
        <div class="exec-sub">XYZ {csi_xyz_val}% · Komp {csi_komp_val}%</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)

with c3:
    cli_gap = round(cli_xyz_val - cli_komp_val, 1)
    sign = "+" if cli_gap >= 0 else ""
    bc = "badge-green" if cli_gap >= 0 else "badge-red"
    lbl = "Unggul" if cli_gap >= 0 else "Tertinggal"
    c3.markdown(f"""<div class="exec-card teal">
        <span class="exec-icon">🔁</span>
        <div class="exec-label">CLI Gap (%)</div>
        <div class="exec-value" style="color:#0F5E5A;">{sign}{cli_gap}</div>
        <div class="exec-sub">XYZ {cli_xyz_val}% · Komp {cli_komp_val}%</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)

with c4:
    worst_img = img_gap_data[0]  # most negative gap
    sign = "+" if worst_img["gap"] >= 0 else ""
    bc = "badge-red" if worst_img["gap"] < 0 else "badge-green"
    c4.markdown(f"""<div class="exec-card red">
        <span class="exec-icon">⚠️</span>
        <div class="exec-label">Biggest Brand Gap</div>
        <div class="exec-value" style="color:#991B1B;font-size:28px;">{worst_img['label']}</div>
        <div class="exec-sub">Gap {sign}{worst_img['gap']}/6 vs kompetitor</div>
        <span class="exec-badge {bc}">Prioritas</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 2 — COMPETITOR LANDSCAPE (siapa kompetitor utama)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">1 · Competitor Landscape — Peta Kompetitor Utama</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_l1, col_l2, col_l3 = st.columns(3)

def render_rank_table(col, counts, title, subtitle):
    top = counts.head(8).reset_index()
    top.columns = ["bank", "count"]
    max_c = top["count"].max() if len(top) > 0 else 1
    rows = ""
    for i, row in top.iterrows():
        badge_cls = "top1" if i == 0 else ("top2" if i == 1 else ("top3" if i == 2 else ""))
        bar_w = int(row["count"] / max_c * 100)
        rows += f"""<tr>
            <td><span class="rank-badge {badge_cls}">{i+1}</span></td>
            <td style="font-weight:{'700' if i<3 else '500'};color:#1A0A10;">{row['bank']}</td>
            <td style="text-align:right;">
                <div style="display:flex;align-items:center;gap:8px;justify-content:flex-end;">
                    <div style="width:60px;height:6px;background:#F3EBE1;border-radius:99px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;background:{'#3D0812' if i==0 else '#C9932A' if i==1 else '#0F5E5A' if i==2 else '#D1D5DB'};border-radius:99px;"></div>
                    </div>
                    <span style="font-family:'DM Serif Display',serif;font-size:15px;color:#3D0812;">{row['count']}</span>
                </div>
            </td>
        </tr>"""

    col.markdown(f"""
    <div class="card card-accent-maroon">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#9B7B5A;margin-bottom:2px;">{title}</div>
        <div style="font-size:11px;color:#C4A882;margin-bottom:14px;">{subtitle}</div>
        <table class="rank-table">{rows}</table>
    </div>""", unsafe_allow_html=True)

with col_l1:
    render_rank_table(col_l1, bank_aktif_counts, "Bank Aktif Digunakan", "Selain Bank XYZ")
with col_l2:
    render_rank_table(col_l2, komp_dana_counts, "Kompetitor Simpan Dana", "Bank lain untuk menyimpan dana")
with col_l3:
    render_rank_table(col_l3, komp_trx_counts, "Kompetitor Transaksi", "Bank lain untuk bertransaksi")

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# BARIS 4 — BRAND ATTRIBUTE GAP RANKING
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">3 · Brand Attribute Gap Ranking — Dimana Kita Tertinggal?</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_bg1, col_bg2 = st.columns([3, 2])

with col_bg1:
    gap_labels  = [d["label"] for d in img_gap_data]
    gap_vals    = [d["gap"]   for d in img_gap_data]
    bar_colors  = ["#15803D" if g >= 0 else "#B91C1C" for g in gap_vals]

    fig_brand_gap = go.Figure(go.Bar(
        x=gap_vals, y=gap_labels, orientation="h",
        marker_color=bar_colors,
        text=[f"{'+' if g >= 0 else ''}{g:.2f}" for g in gap_vals],
        textposition="outside",
        textfont=dict(color="#5C3D2E", size=11, family="Inter"),
    ))
    fig_brand_gap.add_vline(x=0, line_color="#E8D9C8", line_width=1.5)
    fig_brand_gap.update_layout(
        **PLOT,
        xaxis=dict(color="#9B7B5A", gridcolor="#F3EBE1", title="Gap (XYZ − Kompetitor, skala /6)"),
        yaxis=dict(color="#374151", tickfont=dict(size=11, family="Inter"), autorange="reversed"),
        margin=dict(t=10, b=20, l=10, r=70), height=500,
    )

    st.markdown("""<div class="card card-accent-maroon">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#9B7B5A;margin-bottom:12px;">
            Gap per Atribut Brand — Merah = XYZ tertinggal
        </div>""", unsafe_allow_html=True)
    st.plotly_chart(fig_brand_gap, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_bg2:
    neg_gaps = [d for d in img_gap_data if d["gap"] < 0]
    pos_gaps = [d for d in img_gap_data if d["gap"] >= 0]

    neg_rows = "".join([
        f"""<div class="gap-item">
            <span class="gap-label">{d['label']}</span>
            <span class="gap-val-neg">{d['gap']:+.2f}</span>
        </div>""" for d in neg_gaps
    ])
    pos_rows = "".join([
        f"""<div class="gap-item">
            <span class="gap-label">{d['label']}</span>
            <span class="gap-val-pos">{d['gap']:+.2f}</span>
        </div>""" for d in pos_gaps
    ])

    st.markdown(f"""
    <div class="card card-accent-red" style="margin-bottom:12px;">
        <div class="reason-title reason-neg-title">▼ Atribut Tertinggal dari Kompetitor</div>
        {neg_rows if neg_rows else '<div style="font-size:12px;color:#9B7B5A;">Tidak ada gap negatif</div>'}
    </div>
    <div class="card card-accent-teal">
        <div class="reason-title" style="color:#166534;">▲ Atribut Unggul vs Kompetitor</div>
        {pos_rows if pos_rows else '<div style="font-size:12px;color:#9B7B5A;">Tidak ada gap positif</div>'}
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 5 — TOUCHPOINT GAP RANKING
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">4 · Touchpoint Gap Ranking — Di Experience Mana Kompetitor Unggul?</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

col_tp1, col_tp2 = st.columns([2, 3])

with col_tp1:
    tp_sorted = sorted(tp_data, key=lambda x: x["gap"])
    rows_tp = ""
    for d in tp_sorted:
        gap_clr = "#15803D" if d["gap"] >= 0 else "#B91C1C"
        sign = "+" if d["gap"] >= 0 else ""
        xyz_clr = pct_color(d["xyz"])
        rows_tp += f"""<tr>
            <td style="font-weight:600;color:#1A0A10;">{d['label']}</td>
            <td style="text-align:right;font-family:'DM Serif Display',serif;font-size:18px;color:{xyz_clr};">{d['xyz']}%</td>
            <td style="text-align:right;font-size:12px;color:#9B7B5A;">{d['komp']}%</td>
            <td style="text-align:right;font-weight:700;color:{gap_clr};">{sign}{d['gap']}%</td>
        </tr>"""

    st.markdown(f"""
    <div class="card card-accent-maroon">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#9B7B5A;margin-bottom:12px;">Ranking Gap Touchpoint</div>
        <table class="rank-table">
            <thead><tr>
                <th>Touchpoint</th>
                <th class="right">XYZ</th>
                <th class="right">Komp</th>
                <th class="right">Gap</th>
            </tr></thead>
            <tbody>{rows_tp}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)

with col_tp2:
    tp_labels = [d["label"] for d in tp_sorted]
    tp_xyz    = [d["xyz"]   for d in tp_sorted]
    tp_komp   = [d["komp"]  for d in tp_sorted]

    fig_tp = go.Figure()
    fig_tp.add_trace(go.Bar(
        name="Bank XYZ", x=tp_labels, y=tp_xyz,
        marker_color="#3D0812",
        text=[f"{v}%" for v in tp_xyz],
        textposition="outside", textfont=dict(color="#5C3D2E", size=10, family="Inter"),
    ))
    fig_tp.add_trace(go.Bar(
        name="Kompetitor", x=tp_labels, y=tp_komp,
        marker_color="#C9932A",
        text=[f"{v}%" for v in tp_komp],
        textposition="outside", textfont=dict(color="#5C3D2E", size=10, family="Inter"),
    ))
    fig_tp.update_layout(
        **PLOT, barmode="group",
        xaxis=dict(color="#9B7B5A", gridcolor="#F3EBE1"),
        yaxis=dict(color="#9B7B5A", gridcolor="#F3EBE1", range=[0, 115], title="Score (%)"),
        legend=dict(font=dict(color="#5C3D2E", size=11, family="Inter"),
                    bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        margin=dict(t=10, b=10, l=10, r=10), height=320,
    )

    st.markdown("""<div class="card card-accent-teal">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#9B7B5A;margin-bottom:4px;">Perbandingan Skor Touchpoint</div>
    </div>""", unsafe_allow_html=True)

    # Radar
    dims = [d["label"] for d in tp_data]
    xyz_r = [d["xyz"] for d in tp_data]
    komp_r = [d["komp"] for d in tp_data]
    dims_c = dims + [dims[0]]
    xyz_c  = xyz_r  + [xyz_r[0]]
    komp_c = komp_r + [komp_r[0]]

    fig_rad = go.Figure()
    fig_rad.add_trace(go.Scatterpolar(
        r=xyz_c, theta=dims_c, fill="toself",
        fillcolor="rgba(61,8,18,0.12)", line=dict(color="#3D0812", width=2.5), name="Bank XYZ"))
    fig_rad.add_trace(go.Scatterpolar(
        r=komp_c, theta=dims_c, fill="toself",
        fillcolor="rgba(201,147,42,0.12)", line=dict(color="#C9932A", width=2.5), name="Kompetitor"))
    fig_rad.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 110], color="#9B7B5A", gridcolor="#E8D9C8"),
            angularaxis=dict(color="#9B7B5A", gridcolor="#E8D9C8"),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#5C3D2E", size=11),
        legend=dict(font=dict(color="#5C3D2E", size=11, family="Inter"),
                    bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=20, l=20, r=20), height=300,
    )
    st.plotly_chart(fig_rad, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 6 — REASON ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">5 · Reason Analysis — Mengapa Nasabah Merekomendasikan / Puas?</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

def get_top_reasons(df, sentiment_col, category_col, sentiment_val, n=8):
    if sentiment_col not in df.columns or category_col not in df.columns:
        return pd.Series(dtype=int)
    sub = df[df[sentiment_col] == sentiment_val][category_col].dropna()
    sub = sub[sub.astype(str).str.strip() != ""]
    return sub.value_counts().head(n)

tab_nps, tab_csi = st.tabs(["NPS — Alasan Rekomendasi", "CSI — Alasan Kepuasan"])

with tab_nps:
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)

    def reason_card(col, counts, title, title_cls, color):
        if len(counts) == 0:
            col.markdown(f"""<div class="reason-card"><div class="reason-title {title_cls}">{title}</div>
                <div style="font-size:12px;color:#9B7B5A;">Tidak ada data</div></div>""", unsafe_allow_html=True)
            return
        fig = go.Figure(go.Bar(
            x=counts.values, y=counts.index, orientation="h",
            marker_color=color,
            text=counts.values, textposition="outside",
            textfont=dict(color="#5C3D2E", size=10, family="Inter"),
        ))
        fig.update_layout(**PLOT,
            xaxis=dict(color="#9B7B5A", gridcolor="#F3EBE1"),
            yaxis=dict(color="#374151", tickfont=dict(size=9, family="Inter"), autorange="reversed"),
            margin=dict(t=6, b=6, l=6, r=50), height=260)
        col.markdown(f"""<div class="card {'card-accent-teal' if 'Positif' in title else 'card-accent-red'}">
            <div class="reason-title {'reason-pos-title' if 'Positif' in title else 'reason-neg-title'}">{title}</div>
        </div>""", unsafe_allow_html=True)
        col.plotly_chart(fig, use_container_width=True)

    nps_xyz_pos  = get_top_reasons(df, "nps_xyz_sentimen",  "nps_xyz_kategori",  "POSITIVE COMMENTS")
    nps_xyz_neg  = get_top_reasons(df, "nps_xyz_sentimen",  "nps_xyz_kategori",  "NEGATIVE COMMENTS")
    nps_komp_pos = get_top_reasons(df, "nps_komp_sentimen", "nps_komp_kategori", "POSITIVE COMMENTS")
    nps_komp_neg = get_top_reasons(df, "nps_komp_sentimen", "nps_komp_kategori", "NEGATIVE COMMENTS")

    reason_card(col_r1, nps_xyz_pos,  "▲ Positif NPS — XYZ",        "reason-pos-title", "#0F5E5A")
    reason_card(col_r2, nps_xyz_neg,  "▼ Negatif NPS — XYZ",        "reason-neg-title", "#B91C1C")
    reason_card(col_r3, nps_komp_pos, "▲ Positif NPS — Kompetitor", "reason-pos-title", "#C9932A")
    reason_card(col_r4, nps_komp_neg, "▼ Negatif NPS — Kompetitor", "reason-neg-title", "#6B7280")

with tab_csi:
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)

    csi_xyz_pos  = get_top_reasons(df, "alasan_csi_xyz",       "alasan_csi_xyz",       "POSITIVE COMMENTS")
    csi_xyz_neg  = get_top_reasons(df, "alasan_csi_xyz",       "alasan_csi_xyz",       "NEGATIVE COMMENTS")
    csi_komp_pos = get_top_reasons(df, "alasan_csi_kompetitor","alasan_csi_kompetitor","POSITIVE COMMENTS")
    csi_komp_neg = get_top_reasons(df, "alasan_csi_kompetitor","alasan_csi_kompetitor","NEGATIVE COMMENTS")

    # Fallback: jika kolom alasan CSI adalah text biasa, tampilkan word-level counts
    def get_text_top(col, n=8):
        if col not in df.columns: return pd.Series(dtype=int)
        words = []
        for v in df[col].dropna():
            for w in str(v).split(","):
                w = w.strip()
                if len(w) > 3: words.append(w)
        return pd.Series(words).value_counts().head(n)

    # Try sentiment-based first, else text-based
    if len(csi_xyz_pos) == 0:
        csi_xyz_pos = get_text_top("alasan_csi_xyz")
    if len(csi_komp_pos) == 0:
        csi_komp_pos = get_text_top("alasan_csi_kompetitor")

    reason_card(col_c1, csi_xyz_pos,  "▲ Alasan CSI Positif — XYZ",        "reason-pos-title", "#0F5E5A")
    reason_card(col_c2, csi_xyz_neg,  "▼ Alasan CSI Negatif — XYZ",        "reason-neg-title", "#B91C1C")
    reason_card(col_c3, csi_komp_pos, "▲ Alasan CSI Positif — Kompetitor", "reason-pos-title", "#C9932A")
    reason_card(col_c4, csi_komp_neg, "▼ Alasan CSI Negatif — Kompetitor", "reason-neg-title", "#6B7280")

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 6 — PRIORITY ACTION RANKING
# Ranked action list: hanya area negatif, diurutkan berdasarkan gap magnitude
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">6 · Priority Action Ranking — Area Paling Mendesak untuk Dibenahi</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

# Bangun dataset gabungan brand + touchpoint, normalisasi ke skala %
all_items = []
for d in img_gap_data:
    all_items.append({
        "label": d["label"],
        "xyz":   round(d["xyz"] / 6 * 100, 1),
        "komp":  round(d["komp"] / 6 * 100, 1),
        "gap":   round(d["gap"] / 6 * 100, 1),
        "type":  "Brand Image",
    })
for d in tp_data:
    all_items.append({
        "label": d["label"],
        "xyz":   d["xyz"],
        "komp":  d["komp"],
        "gap":   d["gap"],
        "type":  "Touchpoint",
    })

# Urutkan dari gap paling negatif (paling mendesak) ke paling positif
all_items.sort(key=lambda x: x["gap"])

neg_items = [d for d in all_items if d["gap"] < 0]
pos_items = [d for d in all_items if d["gap"] >= 0]

if neg_items:
    # Ranked action list — hanya area negatif, urut gap paling parah
    neg_sorted = sorted(neg_items, key=lambda x: x["gap"])

    # Callout summary di atas list
    most_urgent = neg_sorted[0]
    st.markdown(f"""
    <div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:12px;
                padding:14px 16px;margin-bottom:16px;">
        <div style="font-size:9.5px;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.1em;color:#991B1B;margin-bottom:4px;">
            ⚠ Prioritas Utama
        </div>
        <div style="font-family:'DM Serif Display',serif;font-size:20px;
                    color:#7F1D1D;line-height:1.2;">{most_urgent['label']}</div>
        <div style="font-size:12px;color:#B91C1C;margin-top:4px;font-weight:600;">
            Gap {most_urgent['gap']:+.1f}% &nbsp;·&nbsp; {most_urgent['type']}
        </div>
        <div style="font-size:11px;color:#9B7B5A;margin-top:4px;">
            XYZ {most_urgent['xyz']:.1f}% vs Komp {most_urgent['komp']:.1f}%
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="font-size:10px;font-weight:700;text-transform:uppercase;
                letter-spacing:0.09em;color:#9B7B5A;margin-bottom:10px;">
        Ranking Area yang Perlu Ditingkatkan
    </div>""", unsafe_allow_html=True)

    for i, item in enumerate(neg_sorted):
        bar_w = int(abs(item["gap"]) / max(abs(d["gap"])
                    for d in neg_sorted) * 100)
        rank_color = "#991B1B" if i == 0 else (
            "#B91C1C" if i == 1 else ("#EF4444" if i == 2 else "#9B7B5A"))
        st.markdown(f"""
        <div class="opp-item" style="flex-direction:column;align-items:stretch;gap:6px;">
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div class="opp-rank" style="font-size:20px;color:{rank_color};">{i+1}</div>
                    <div>
                        <div class="opp-area">{item['label']}</div>
                        <div class="opp-meta">{item['type']}</div>
                    </div>
                </div>
                <div style="font-size:13px;font-weight:700;color:{rank_color};">
                    {item['gap']:+.1f}%
                </div>
            </div>
            <div style="height:5px;background:#F3EBE1;border-radius:99px;overflow:hidden;">
                <div style="width:{bar_w}%;height:100%;background:{rank_color};
                            border-radius:99px;"></div>
            </div>
            <div style="font-size:10px;color:#9B7B5A;">
                XYZ {item['xyz']:.1f}% &nbsp;·&nbsp; Komp {item['komp']:.1f}%
            </div>
        </div>""", unsafe_allow_html=True)

else:
    # Tidak ada gap negatif — tampilkan top area untuk dipertahankan
    pos_sorted = sorted(pos_items, key=lambda x: x["gap"], reverse=True)

    st.markdown("""
    <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;
                padding:14px 16px;margin-bottom:16px;">
        <div style="font-size:9.5px;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.1em;color:#166534;margin-bottom:4px;">✅ Status</div>
        <div style="font-family:'DM Serif Display',serif;font-size:18px;color:#14532D;">
            XYZ Unggul di Semua Area
        </div>
        <div style="font-size:11px;color:#9B7B5A;margin-top:4px;">
            Tidak ada area yang tertinggal dari kompetitor
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="font-size:10px;font-weight:700;text-transform:uppercase;
                letter-spacing:0.09em;color:#9B7B5A;margin-bottom:10px;">
        Top Area Keunggulan — Pertahankan
    </div>""", unsafe_allow_html=True)

    # Grid full-width — pakai kolom biar memenuhi lebar yang ditinggalkan chart
    top5 = pos_sorted[:5]
    n_cols = min(3, len(top5))
    cols = st.columns(n_cols)

    for i, item in enumerate(top5):
        bar_w = int(item["gap"] / max(d["gap"] for d in pos_sorted) * 100)
        with cols[i % n_cols]:
            st.markdown(f"""
            <div class="opp-item" style="flex-direction:column;align-items:stretch;gap:6px;
                        height:100%;">
                <div style="display:flex;align-items:center;justify-content:space-between;">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div class="opp-rank" style="font-size:20px;color:#166534;">{i+1}</div>
                        <div>
                            <div class="opp-area">{item['label']}</div>
                            <div class="opp-meta">{item['type']}</div>
                        </div>
                    </div>
                    <div style="font-size:13px;font-weight:700;color:#166534;">
                        {item['gap']:+.1f}%
                    </div>
                </div>
                <div style="height:5px;background:#F3EBE1;border-radius:99px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;background:#22C55E;
                                border-radius:99px;"></div>
                </div>
                <div style="font-size:10px;color:#9B7B5A;">
                    XYZ {item['xyz']:.1f}% &nbsp;·&nbsp; Komp {item['komp']:.1f}%
                </div>
            </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)