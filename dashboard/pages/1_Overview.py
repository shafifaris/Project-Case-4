# 1_Overview.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# ── CSS & STYLE ───────────────────────────────────────────────────────────────
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
    margin-bottom: 16px; margin-top: 4px;
}
.section-label-text {
    color: #3D0812; font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; white-space: nowrap;
}
.section-label-line {
    flex: 1; height: 1px; background: linear-gradient(90deg, #C4A882, transparent);
}

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
.exec-card.indigo::before { background: linear-gradient(90deg, #312E81, #6366F1); }
.exec-card.cyan::before   { background: linear-gradient(90deg, #0E7490, #22D3EE); }
.exec-icon  { font-size: 22px; margin-bottom: 10px; display: block; line-height: 1; }
.exec-label { color: #9B7B5A; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
.exec-value { font-family: 'DM Serif Display', serif; font-size: 36px; font-weight: 400; line-height: 1; margin-bottom: 6px; }
.exec-sub   { font-size: 11px; color: #9B7B5A; font-weight: 500; }
.exec-badge { display: inline-block; padding: 3px 8px; border-radius: 20px; font-size: 10px; font-weight: 700; margin-top: 8px; }
.badge-green  { background: #DCFCE7; color: #166534; }
.badge-yellow { background: #FEF9C3; color: #854D0E; }
.badge-red    { background: #FEE2E2; color: #991B1B; }

.comp-table-wrap {
    background: white; border-radius: 14px; padding: 20px 22px;
    border: 1px solid #E8D9C8; box-shadow: 0 2px 12px rgba(61,8,18,0.06);
    margin-top: 16px;
}
.comp-table { width: 100%; border-collapse: collapse; }
.comp-table th {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #9B7B5A; padding: 8px 12px;
    border-bottom: 2px solid #E8D9C8; text-align: left;
}
.comp-table th.right { text-align: right; }
.comp-table td { padding: 10px 12px; border-bottom: 1px solid #F3EBE1; font-size: 13px; }
.comp-table tr:last-child td { border-bottom: none; }
.comp-table td.metric-name { font-weight: 600; color: #1A0A10; }
.comp-table td.val-xyz  { text-align: right; font-family: 'DM Serif Display', serif; font-size: 20px; color: #3D0812; }
.comp-table td.val-komp { text-align: right; font-family: 'DM Serif Display', serif; font-size: 20px; color: #6B7280; }
.comp-table td.gap-pos  { text-align: right; color: #15803D; font-weight: 700; }
.comp-table td.gap-neg  { text-align: right; color: #B91C1C; font-weight: 700; }

.idx-card {
    background: white; border-radius: 14px; padding: 20px 18px;
    border: 1px solid #E8D9C8; box-shadow: 0 2px 12px rgba(61,8,18,0.06);
}
.idx-title  { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #9B7B5A; margin-bottom: 4px; }
.idx-value  { font-family: 'DM Serif Display', serif; font-size: 42px; color: #1A0A10; line-height: 1.1; margin-bottom: 4px; }
.idx-sub    { font-size: 11px; color: #9B7B5A; margin-bottom: 12px; }
.idx-divider { border: none; border-top: 1px solid #F3EBE1; margin: 12px 0; }
.idx-list-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.idx-list-label.pos { color: #15803D; }
.idx-list-label.neg { color: #B91C1C; }
.idx-item { display: flex; justify-content: space-between; align-items: center; padding: 5px 0; border-bottom: 1px solid #FAF4EE; font-size: 12px; }
.idx-item:last-child { border-bottom: none; }
.idx-item-name { color: #374151; font-weight: 500; }
.idx-item-val-pos { font-weight: 700; color: #15803D; font-size: 12px; }
.idx-item-val-neg { font-weight: 700; color: #B91C1C; font-size: 12px; }
.idx-item-val-neu { font-weight: 700; color: #3D0812; font-size: 12px; }

.mpi-bar-wrap { margin: 10px 0; }
.mpi-bar-header { display: flex; justify-content: space-between; font-size: 11.5px; margin-bottom: 5px; color: #374151; font-weight: 500; }
.mpi-bar-bg   { height: 10px; background: #F3EBE1; border-radius: 99px; overflow: hidden; }
.mpi-bar-xyz  { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #3D0812, #8B1A2E); }
.mpi-bar-komp { height: 100%; border-radius: 99px; background: #D1D5DB; }

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

    # ── Konversi semua kolom waktu ke numerik ──
    time_cols = ['waktu_tunggu_teller_aktual', 'waktu_tunggu_teller_toleransi',
                 'waktu_tunggu_cs_aktual', 'waktu_tunggu_cs_toleransi']

    for col in time_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # NPS XYZ
    def parse_nps(val):
        if pd.isna(val) or str(val).strip() == '':
            return np.nan
        try:
            val_str = str(val).strip().split()[0]
            return int(val_str)
        except:
            return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)
    df['nps_category'] = df['nps_num'].apply(
        lambda v: 'Promoter' if v >= 9 else (
            'Passive' if v >= 7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    # NPS Kompetitor
    df['nps_komp_num'] = df['nps_kompetitor'].apply(parse_nps)
    df['nps_komp_category'] = df['nps_komp_num'].apply(
        lambda v: 'Promoter' if v >= 9 else (
            'Passive' if v >= 7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    # ── CES (Customer Effort Score) ──
    # Mengonversi kolom ke numerik untuk memastikan perhitungan aman
    if 'aksesibilitas_cabang_xyz' in df.columns:
        df['aksesibilitas_cabang_xyz'] = pd.to_numeric(df['aksesibilitas_cabang_xyz'], errors='coerce')
    
    # Nilai ces_xyz diambil langsung dari kolom aksesibilitas_cabang_xyz
    df['ces_xyz'] = df['aksesibilitas_cabang_xyz']

    # CES Kompetitor
    tp_komp_cols = ['overall_teller_komp', 'overall_cs_komp', 'overall_atm_komp',
                    'overall_banking_hall_komp', 'overall_sekuriti_komp']
    for col in tp_komp_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df['ces_komp_raw'] = df[tp_komp_cols].mean(axis=1)
    df['ces_kompetitor'] = df['ces_komp_raw'].apply(
        lambda x: round(7 - x, 1) if pd.notna(x) else np.nan)

    # Semua kolom numerik
    num_cols = [
        'csi_xyz', 'cli_xyz', 'csi_kompetitor', 'cli_kompetitor',
        'ces_xyz', 'ces_kompetitor',
        'overall_teller_xyz', 'overall_cs_xyz', 'overall_atm_xyz',
        'overall_banking_hall_xyz', 'overall_sekuriti_xyz',
        'overall_operasional_xyz', 'overall_parkir_xyz', 'overall_toilet_xyz',
        'overall_teller_komp', 'overall_cs_komp', 'overall_atm_komp',
        'overall_banking_hall_komp', 'overall_sekuriti_komp',
        'overall_operasional_komp', 'overall_parkir_komp', 'overall_toilet_komp',
        'cef_bahagia_xyz', 'cef_percaya_xyz', 'cef_dihargai_xyz', 'cef_diperhatikan_xyz',
        'cef_aman_xyz', 'cef_fokus_xyz', 'cef_memanjakan_xyz', 'cef_tertarik_xyz', 'cef_semangat_xyz',
        'cef_tidak_puas_xyz', 'cef_frustasi_xyz', 'cef_kecewa_xyz',
        'cef_tertekan_xyz', 'cef_tidak_bahagia_xyz', 'cef_diabaikan_xyz', 'cef_tergesa_xyz',
        'img_terkenal_xyz', 'img_rasa_aman_xyz', 'img_dihargai_xyz', 'img_reputasi_xyz',
        'img_produk_lengkap_xyz', 'img_investasi_xyz', 'img_kemudahan_transaksi_xyz',
        'img_teknologi_xyz', 'img_reward_xyz', 'img_echannel_xyz',
        'img_terkenal_komp', 'img_rasa_aman_komp', 'img_dihargai_komp', 'img_reputasi_komp',
        'img_produk_lengkap_komp', 'img_investasi_komp', 'img_kemudahan_transaksi_komp',
        'img_teknologi_komp', 'img_reward_komp', 'img_echannel_komp',
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Pct skala 1-6 → 0-100
    tp_pct_cols = [
        'csi_xyz', 'cli_xyz', 'csi_kompetitor', 'cli_kompetitor',
        'ces_xyz', 'ces_kompetitor',
        'overall_teller_xyz', 'overall_cs_xyz', 'overall_atm_xyz',
        'overall_banking_hall_xyz', 'overall_sekuriti_xyz',
        'overall_operasional_xyz', 'overall_parkir_xyz', 'overall_toilet_xyz',
        'overall_teller_komp', 'overall_cs_komp', 'overall_atm_komp',
        'overall_banking_hall_komp', 'overall_sekuriti_komp',
        'overall_operasional_komp', 'overall_parkir_komp', 'overall_toilet_komp',
    ]
    for c in tp_pct_cols:
        if c in df.columns:
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
    icons = {"Overview": "◈", "Branch Intelligence": "▣",
             "Touchpoint": "◎", "Customer Behaviour": "◉", "Competitor": "◆"}
    for name, path in pages.items():
        active = "active" if name == "Overview" else ""
        st.markdown(
            f"<a href='{path}' target='_self' class='nav-pill {active}'>"
            f"<span>{icons[name]}</span><span>{name}</span></a>",
            unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(245,212,138,0.12);margin:16px 0;'>",
                unsafe_allow_html=True)
    st.markdown("<div class='nav-label'>Filter Data</div>",
                unsafe_allow_html=True)

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


def pct_label(v): return "Baik" if v >= 80 else (
    "Perlu Perhatian" if v >= 65 else "Kritis")


def pct_color(v): return "#15803D" if v >= 80 else (
    "#B45309" if v >= 65 else "#B91C1C")


def badge_cls(v, hi, mid):
    return "badge-green" if v >= hi else ("badge-yellow" if v >= mid else "badge-red")


def ces_label(v):
    if v <= 2:
        return "Mudah"
    elif v <= 4:
        return "Sedang"
    else:
        return "Sulit"


def ces_color(v):
    if v <= 2:
        return "#15803D"
    elif v <= 4:
        return "#B45309"
    else:
        return "#B91C1C"


PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color="#5C3D2E", size=11),
)

# ════════════════════════════════════════════════════════════════════════════
# COMPUTED METRICS
# ════════════════════════════════════════════════════════════════════════════

# ─ NPS XYZ ─
promoters = int((df["nps_category"] == "Promoter").sum())
detractors = int((df["nps_category"] == "Detractor").sum())
passives = int((df["nps_category"] == "Passive").sum())
nps_score = round((promoters - detractors) / n * 100, 1) if n > 0 else 0.0
prom_pct = round(promoters / n * 100, 1) if n > 0 else 0.0
detr_pct = round(detractors / n * 100, 1) if n > 0 else 0.0

# ─ NPS Kompetitor ─
komp_valid = df["nps_komp_num"].dropna()
n_komp = len(komp_valid)
if n_komp > 0:
    prom_k = int((df["nps_komp_category"] == "Promoter").sum())
    detr_k = int((df["nps_komp_category"] == "Detractor").sum())
    nps_komp_score = round((prom_k - detr_k) / n_komp * 100, 1)
else:
    nps_komp_score = 0.0

# ─ CSI / CLI XYZ & Kompetitor ─
csi_score = round(safe_mean(df["csi_xyz"]),
                  2) if "csi_xyz" in df.columns else 0.0
csi_pct = round(csi_score / 6 * 100, 1)
csi_komp_score = round(
    safe_mean(df["csi_kompetitor"]), 2) if "csi_kompetitor" in df.columns else 0.0

cli_score = round(safe_mean(df["cli_xyz"]),
                  2) if "cli_xyz" in df.columns else 0.0
cli_pct = round(cli_score / 6 * 100, 1)
cli_komp_score = round(
    safe_mean(df["cli_kompetitor"]), 2) if "cli_kompetitor" in df.columns else 0.0

# ─ CES XYZ & Kompetitor ─
ces_score = round(safe_mean(df["ces_xyz"]),
                  2) if "ces_xyz" in df.columns else 0.0
ces_pct = round((6 - ces_score) / 6 * 100, 1)
ces_komp_score = round(
    safe_mean(df["ces_kompetitor"]), 2) if "ces_kompetitor" in df.columns else 0.0

# ─ CEF — Emotional Index ─
CEF_POS_COLS = [
    'cef_bahagia_xyz', 'cef_percaya_xyz', 'cef_dihargai_xyz', 'cef_diperhatikan_xyz',
    'cef_aman_xyz', 'cef_fokus_xyz', 'cef_memanjakan_xyz', 'cef_tertarik_xyz', 'cef_semangat_xyz',
]
CEF_NEG_COLS = [
    'cef_tidak_puas_xyz', 'cef_frustasi_xyz', 'cef_kecewa_xyz',
    'cef_tertekan_xyz', 'cef_tidak_bahagia_xyz', 'cef_diabaikan_xyz', 'cef_tergesa_xyz',
]
CEF_POS_LABELS = {
    'cef_bahagia_xyz': 'Bahagia', 'cef_percaya_xyz': 'Percaya', 'cef_dihargai_xyz': 'Dihargai',
    'cef_diperhatikan_xyz': 'Diperhatikan', 'cef_aman_xyz': 'Aman', 'cef_fokus_xyz': 'Fokus',
    'cef_memanjakan_xyz': 'Memanjakan', 'cef_tertarik_xyz': 'Tertarik', 'cef_semangat_xyz': 'Semangat',
}
CEF_NEG_LABELS = {
    'cef_tidak_puas_xyz': 'Tidak Puas', 'cef_frustasi_xyz': 'Frustasi', 'cef_kecewa_xyz': 'Kecewa',
    'cef_tertekan_xyz': 'Tertekan', 'cef_tidak_bahagia_xyz': 'Tidak Bahagia',
    'cef_diabaikan_xyz': 'Diabaikan', 'cef_tergesa_xyz': 'Tergesa',
}

cef_pos_vals = {c: round(safe_mean(df[c]), 2)
                for c in CEF_POS_COLS if c in df.columns}
cef_neg_vals = {c: round(safe_mean(df[c]), 2)
                for c in CEF_NEG_COLS if c in df.columns}

# Skala 1–6 langsung dari rata-rata tiap grup
avg_pos = round(float(np.mean(list(cef_pos_vals.values()))), 2) if cef_pos_vals else 0.0
avg_neg = round(float(np.mean(list(cef_neg_vals.values()))), 2) if cef_neg_vals else 0.0

# emo_index dihapus — display pakai avg_pos & avg_neg langsung

top3_pos = sorted(cef_pos_vals.items(), key=lambda x: x[1], reverse=True)[:3]
top3_neg = sorted(cef_neg_vals.items(), key=lambda x: x[1], reverse=True)[:3]

# ─ Brand Image Index ─
IMG_XYZ_COLS = [
    'img_terkenal_xyz', 'img_rasa_aman_xyz', 'img_dihargai_xyz', 'img_reputasi_xyz',
    'img_produk_lengkap_xyz', 'img_investasi_xyz', 'img_kemudahan_transaksi_xyz',
    'img_teknologi_xyz', 'img_reward_xyz', 'img_echannel_xyz',
]
IMG_KOMP_COLS = [
    'img_terkenal_komp', 'img_rasa_aman_komp', 'img_dihargai_komp', 'img_reputasi_komp',
    'img_produk_lengkap_komp', 'img_investasi_komp', 'img_kemudahan_transaksi_komp',
    'img_teknologi_komp', 'img_reward_komp', 'img_echannel_komp',
]
IMG_LABELS = {
    'img_terkenal_xyz': 'Terkenal', 'img_rasa_aman_xyz': 'Rasa Aman', 'img_dihargai_xyz': 'Dihargai',
    'img_reputasi_xyz': 'Reputasi', 'img_produk_lengkap_xyz': 'Produk Lengkap',
    'img_investasi_xyz': 'Investasi', 'img_kemudahan_transaksi_xyz': 'Kemudahan Transaksi',
    'img_teknologi_xyz': 'Teknologi', 'img_reward_xyz': 'Reward', 'img_echannel_xyz': 'E-Channel',
}

img_xyz_vals = {c: round(safe_mean(df[c]), 2)
                for c in IMG_XYZ_COLS if c in df.columns}
img_komp_vals = {c: round(safe_mean(df[c]), 2)
                 for c in IMG_KOMP_COLS if c in df.columns}
brand_index = round(
    float(np.mean(list(img_xyz_vals.values()))),  2) if img_xyz_vals else 0.0
brand_komp_index = round(
    float(np.mean(list(img_komp_vals.values()))), 2) if img_komp_vals else 0.0

img_sorted = sorted(img_xyz_vals.items(), key=lambda x: x[1], reverse=True)
img_top3 = img_sorted[:3]
img_bot3 = img_sorted[-3:][::-1]

# ─ Market Preference Index ─


def xyz_exact_pct(col):
    if col not in df.columns:
        return 0.0
    s = df[col].dropna().astype(str).str.strip()
    if len(s) == 0:
        return 0.0
    return round((s == "Bank XYZ").mean() * 100, 1)


def xyz_contains_pct(col):
    if col not in df.columns:
        return 0.0
    s = df[col].dropna().astype(str).str.strip()
    if len(s) == 0:
        return 0.0
    return round(s.str.contains("Bank XYZ", regex=False).mean() * 100, 1)


mpi_dana = xyz_exact_pct("bank_utama_simpan_dana")
mpi_trx = xyz_exact_pct("bank_utama_transaksi")
mpi_aktif = xyz_contains_pct("bank_aktif_digunakan")

mpi_vals_list = [v for v in [mpi_dana, mpi_trx, mpi_aktif] if v > 0]
mpi_index = round(float(np.mean(mpi_vals_list)), 1) if mpi_vals_list else 0.0

# ─ Touchpoint ─
TOUCHPOINTS = [
    ("Teller",       "overall_teller_xyz",       "overall_teller_komp"),
    ("Customer Svc", "overall_cs_xyz",            "overall_cs_komp"),
    ("ATM",          "overall_atm_xyz",           "overall_atm_komp"),
    ("Banking Hall", "overall_banking_hall_xyz",  "overall_banking_hall_komp"),
    ("Sekuriti",     "overall_sekuriti_xyz",      "overall_sekuriti_komp"),
    ("Operasional",  "overall_operasional_xyz",   "overall_operasional_komp"),
    ("Parkir",       "overall_parkir_xyz",        "overall_parkir_komp"),
    ("Toilet",       "overall_toilet_xyz",        "overall_toilet_komp"),
]

tp_data = []
for label, col_xyz, col_komp in TOUCHPOINTS:
    val_xyz = round(safe_mean(df[col_xyz]) / 6 *
                    100, 1) if col_xyz in df.columns else 0.0
    val_komp = round(safe_mean(df[col_komp]) / 6 *
                     100, 1) if col_komp in df.columns else 0.0
    tp_data.append({"label": label, "xyz": val_xyz, "komp": val_komp})

tp_sorted_asc = sorted(tp_data, key=lambda x: x["xyz"])

# ─ Cabang NPS ─
cabang_nps = df.groupby(["nama_cabang", "provinsi"]).agg(
    responden=("serial_id", "count"),
    nps_avg=("nps_num", "mean"),
    promoter_pct=("nps_category", lambda x: round(
        (x == "Promoter").mean() * 100, 1)),
).reset_index()
cabang_nps["nps_avg"] = cabang_nps["nps_avg"].round(1)

# ════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">◈ Bank XYZ · Customer Experience Intelligence</div>
    <h2>Executive Overview</h2>
    <p>{n:,} responden &nbsp;·&nbsp; {df['nama_cabang'].nunique()} kantor cabang &nbsp;·&nbsp; {df['provinsi'].nunique()} provinsi</p>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 1 — EXECUTIVE KPI (5 KPI termasuk CES)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">Executive KPI</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    bc1 = badge_cls(nps_score, 50, 20)
    label1 = "Excellent" if nps_score >= 50 else (
        "Good" if nps_score >= 20 else "Needs Attention")
    c1.markdown(f"""<div class="exec-card maroon">
        <span class="exec-icon">📊</span>
        <div class="exec-label">Net Promoter Score</div>
        <div class="exec-value" style="color:#3D0812;">{nps_score}</div>
        <div class="exec-sub">Promoter {prom_pct}% · Detractor {detr_pct}%</div>
        <span class="exec-badge {bc1}">{label1}</span>
    </div>""", unsafe_allow_html=True)

with c2:
    bc2 = badge_cls(csi_pct, 80, 65)
    label2 = "Excellent" if csi_pct >= 80 else (
        "Good" if csi_pct >= 65 else "Needs Attention")
    c2.markdown(f"""<div class="exec-card gold">
        <span class="exec-icon">⭐</span>
        <div class="exec-label">Customer Satisfaction (CSI)</div>
        <div class="exec-value" style="color:#7A5100;">{csi_score}<span style="font-size:18px;color:#9B7B5A;">/6</span></div>
        <div class="exec-sub">{csi_pct}% dari skala penuh</div>
        <span class="exec-badge {bc2}">{label2}</span>
    </div>""", unsafe_allow_html=True)

with c3:
    bc3 = badge_cls(cli_pct, 80, 65)
    label3 = "Excellent" if cli_pct >= 80 else (
        "Good" if cli_pct >= 65 else "Needs Attention")
    c3.markdown(f"""<div class="exec-card teal">
        <span class="exec-icon">🔁</span>
        <div class="exec-label">Customer Loyalty (CLI)</div>
        <div class="exec-value" style="color:#0F5E5A;">{cli_score}<span style="font-size:18px;color:#9B7B5A;">/6</span></div>
        <div class="exec-sub">{cli_pct}% dari skala penuh</div>
        <span class="exec-badge {bc3}">{label3}</span>
    </div>""", unsafe_allow_html=True)

with c4:
    # Membalik parameter badge_cls agar ces_pct rendah dapet warna hijau (success)
    # dan ces_pct tinggi dapet warna merah (danger)
    bc4 = badge_cls(100 - ces_pct, 80, 65)
    
    # Kembali ke logika asli kamu (skor kecil = Sulit / High Effort)
    ces_label_text = "Sulit" if ces_score <= 2 else (
        "Sedang" if ces_score <= 4 else "Mudah")
        
    label4 = "High Effort" if ces_score <= 2 else (
        "Medium Effort" if ces_score <= 4 else "Low Effort")
        
    c4.markdown(f"""<div class="exec-card cyan">
        <span class="exec-icon">💪</span>
        <div class="exec-label">Customer Effort Score (CES)</div>
        <div class="exec-value" style="color:#0F5E5A ;">{ces_score}<span style="font-size:18px;color:#9B7B5A;">/6</span></div>
        <div class="exec-sub">{ces_pct}% effort-free · {ces_label_text}</div>
        <span class="exec-badge {bc4}">{label4}</span>
    </div>""", unsafe_allow_html=True)

with c5:
    bc5 = badge_cls(mpi_index, 70, 50)
    label5 = "Dominan" if mpi_index >= 70 else (
        "Kompetitif" if mpi_index >= 50 else "Perlu Ditingkatkan")
    c5.markdown(f"""<div class="exec-card indigo">
        <span class="exec-icon">🏆</span>
        <div class="exec-label">Market Preference Index</div>
        <div class="exec-value" style="color:#312E81;">{mpi_index}<span style="font-size:18px;color:#9B7B5A;">%</span></div>
        <div class="exec-sub">nasabah pilih XYZ sebagai bank utama</div>
        <span class="exec-badge {bc5}">{label5}</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 2 — COMPETITIVE POSITION
# ════════════════════════════════════════════════════════════════════════════

# CSS bubble/card + stretch fix (multi-layer)
st.markdown(
    '<style>'
    '[data-testid="stHorizontalBlock"] { align-items: stretch; } '
    '[data-testid="column"] { display: flex; flex-direction: column; } '
    '[data-testid="column"] > div { height: 100%; flex: 1; } '
    '[data-testid="column"] > div > div { height: 100%; } '
    '[data-testid="column"] [data-testid="stVerticalBlockBorderWrapper"] { height: 100%; } '
    '[data-testid="column"] [data-testid="stVerticalBlock"] { height: 100%; } '
    '.st-key-comp_table_card, .st-key-comp_donut_card, .st-key-comp_radar_card { '
    'background: white; border: 1px solid #E8D9C8; border-radius: 16px; '
    'padding: 18px 20px; box-shadow: 0 2px 12px rgba(61,8,18,0.06); '
    'height: 100%; box-sizing: border-box; '
    'display: flex; flex-direction: column; } '
    '.comp-card-title { font-size: 11px; font-weight: 700; text-transform: uppercase; '
    'letter-spacing: 0.09em; color: #9B7B5A; margin-bottom: 10px; } '
    '</style>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-label">'
    '<span class="section-label-text">Competitive Position</span>'
    '<div class="section-label-line"></div>'
    '</div>',
    unsafe_allow_html=True
)

col_comp, col_donut, col_radar = st.columns([3, 2, 2])

# ─ Tabel Perbandingan ─
with col_comp:
    with st.container(key="comp_table_card"):
        st.markdown(
            '<div class="comp-card-title" style="margin-bottom:20px;">'
            'Perbandingan Metrik XYZ vs Kompetitor</div>',
            unsafe_allow_html=True
        )


        def gap_row(metric, xyz_val, komp_val, suffix=""):
            diff = round(xyz_val - komp_val, 1)
            cls  = "gap-pos" if diff >= 0 else "gap-neg"
            sign = "+" if diff >= 0 else ""
            return (
                '<tr>'
                f'<td class="metric-name">{metric}</td>'
                f'<td class="val-xyz">{xyz_val}{suffix}</td>'
                f'<td class="val-komp">{komp_val}{suffix}</td>'
                f'<td class="{cls}">{sign}{diff}{suffix}</td>'
                '</tr>'
            )

        mpi_komp = round(100 - mpi_index, 1) if mpi_index > 0 else 0.0

        # Menambahkan CES dengan fungsi gap_row bawaan Anda (skala disesuaikan, contoh: /5 atau /7)
        rows_html = (
            gap_row("Net Promoter Score (NPS)", nps_score, nps_komp_score)
            + gap_row("Satisfaction (CSI)", csi_score, csi_komp_score, "/6")
            + gap_row("Loyalty (CLI)", cli_score, cli_komp_score, "/6")
            + gap_row("Brand Image Index", brand_index, brand_komp_index, "/6")
        )

        table_html = (
            '<table class="comp-table">'
            '<thead><tr>'
            '<th>Metric</th>'
            '<th class="right">Bank XYZ</th>'
            '<th class="right">Kompetitor</th>'
            '<th class="right">Gap</th>'
            '</tr></thead>'
            f'<tbody>{rows_html}</tbody>'
            '</table>'
        )
        st.markdown(table_html, unsafe_allow_html=True)

# ─ Donut NPS ─
with col_donut:
    with st.container(key="comp_donut_card"):
        st.markdown('<div class="comp-card-title">Distribusi NPS</div>', unsafe_allow_html=True)

        fig_donut = go.Figure(go.Pie(
            labels=["Promoter", "Passive", "Detractor"],
            values=[promoters, passives, detractors],
            hole=0.68,
            marker_colors=["#15803D", "#C9932A", "#B91C1C"],
            textfont=dict(size=10, color="white"),
            textinfo="percent",
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        ))
        fig_donut.update_layout(
            **PLOT, height=260,
            margin=dict(t=10, b=30, l=0, r=0),
            showlegend=True,
            legend=dict(font=dict(color="#5C3D2E", size=10), orientation="h", x=0.05, y=-0.08),
            annotations=[dict(
                text=f"<b>{nps_score}</b><br><span style='font-size:10px'>NPS</span>",
                x=0.5, y=0.5,
                font=dict(size=22, color="#1A0A10", family="DM Serif Display"),
                showarrow=False,
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# ─ Radar Brand Image ─
with col_radar:
    with st.container(key="comp_radar_card"):
        st.markdown('<div class="comp-card-title">Radar Perception</div>', unsafe_allow_html=True)

        if img_xyz_vals and img_komp_vals:
            radar_keys   = list(img_xyz_vals.keys())
            radar_labels = [IMG_LABELS.get(k, k) for k in radar_keys]
            r_xyz  = [img_xyz_vals[k] for k in radar_keys]
            r_komp = [img_komp_vals.get(k.replace("_xyz", "_komp"), 0) for k in radar_keys]

            r_xyz_c  = r_xyz  + [r_xyz[0]]
            r_komp_c = r_komp + [r_komp[0]]
            r_lbl_c  = radar_labels + [radar_labels[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=r_xyz_c, theta=r_lbl_c,
                fill='toself', fillcolor='rgba(139,26,46,0.12)',
                line=dict(color='#8B1A2E', width=2),
                marker=dict(color='#C9932A', size=5),
                name='Bank XYZ',
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=r_komp_c, theta=r_lbl_c,
                fill='toself', fillcolor='rgba(100,100,100,0.08)',
                line=dict(color='#9CA3AF', width=1.5, dash='dot'),
                marker=dict(color='#9CA3AF', size=4),
                name='Kompetitor',
            ))
            fig_radar.update_layout(
                **PLOT,
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 6],
                                    tickfont=dict(size=8, color="#9B7B5A"),
                                    gridcolor="#EEE4D8"),
                    angularaxis=dict(tickfont=dict(size=9, color="#374151")),
                    bgcolor="rgba(0,0,0,0)",
                ),
                height=260,
                margin=dict(t=20, b=10, l=30, r=30),
                legend=dict(font=dict(size=10, color="#5C3D2E"),
                            orientation="h", x=0.15, y=-0.05),
                showlegend=True,
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.markdown(
                '<div style="height:260px;display:flex;align-items:center;justify-content:center;'
                'color:#9B7B5A;font-size:12px;">Data brand image tidak tersedia</div>',
                unsafe_allow_html=True
            )
st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 3 — EXPERIENCE HEALTH (tanpa CES detail)
# ════════════════════════════════════════════════════════════════════════════

# CSS pendukung
st.markdown(
    """
    <style>
    [data-testid="column"] > div { height: 100%; }
    .idx-card { box-sizing: border-box; }
    .compact-idx .idx-title  { font-size: 10px;   margin-bottom: 2px; }
    .compact-idx .idx-value  { font-size: 26px;   margin-bottom: 1px; }
    .compact-idx .idx-sub    { font-size: 10px;   margin-bottom: 4px; }
    .compact-idx .idx-divider { margin: 6px 0; }
    .compact-idx .idx-list-label { font-size: 9.5px; margin-bottom: 4px; }
    .compact-idx .idx-item   { padding: 3px 0; font-size: 11px; }
    .compact-idx .mpi-bar-box { padding: 7px 10px; margin-top: 0; }
    .compact-idx .mpi-bar-label { font-size: 10px; margin-bottom: 3px; }
    .compact-idx .mpi-bar-track { height: 5px; }

    /* ── Equal-height columns ── */
    [data-testid="stHorizontalBlock"] { align-items: stretch !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div > div {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] .idx-card {
        flex: 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-label">'
    '<span class="section-label-text">Experience Health</span>'
    '<div class="section-label-line"></div>'
    '</div>',
    unsafe_allow_html=True
)

col_emo, col_brand, col_mpi = st.columns([2, 2, 2])

# ─ Emotional Index ─
with col_emo:
    pos_rows = ""
    for c, v in top3_pos:
        pos_rows += (
            '<div class="idx-item">'
            f'<span class="idx-item-name">{CEF_POS_LABELS.get(c, c)}</span>'
            f'<span class="idx-item-val-pos">{v}</span>'
            '</div>'
        )

    neg_rows = ""
    for c, v in top3_neg:
        neg_rows += (
            '<div class="idx-item">'
            f'<span class="idx-item-name">{CEF_NEG_LABELS.get(c, c)}</span>'
            f'<span class="idx-item-val-neg">{v}</span>'
            '</div>'
        )

    emo_card = (
        '<div class="idx-card compact-idx" style="display:flex;flex-direction:column;height:100%;">'
        '<div class="idx-title">Emotional Index</div>'

        '<div style="display:flex;gap:8px;margin:6px 0 4px;">'

        '<div style="flex:1;background:#F0FDF4;border-radius:8px;padding:8px 10px;text-align:center;">'
        '<div style="font-size:11px;color:#15803D;font-weight:600;margin-bottom:2px;">😊 Positif</div>'
        f'<div style="font-size:22px;font-weight:700;color:#15803D;">{avg_pos:.2f}'
        '<span style="font-size:12px;color:#9B7B5A;">/6</span></div>'
        '</div>'

        '<div style="flex:1;background:#FFF1F2;border-radius:8px;padding:8px 10px;text-align:center;">'
        '<div style="font-size:11px;color:#B91C1C;font-weight:600;margin-bottom:2px;">😟 Negatif</div>'
        f'<div style="font-size:22px;font-weight:700;color:#B91C1C;">{avg_neg:.2f}'
        '<span style="font-size:12px;color:#9B7B5A;">/6</span></div>'
        '</div>'

        '</div>'

        '<hr class="idx-divider">'
        '<div class="idx-list-label pos">▲ Top Emosi Positif</div>'
        f'{pos_rows}'
        '<div class="idx-list-label neg" style="margin-top:6px;">▼ Top Emosi Negatif</div>'
        f'{neg_rows}'
        '</div>'
    )
    st.markdown(emo_card, unsafe_allow_html=True)

# ─ Brand Image Index ─
with col_brand:
    brand_color = "#15803D" if brand_index >= 4.5 else (
        "#B45309" if brand_index >= 3.5 else "#B91C1C")
    brand_diff = round(brand_index - brand_komp_index, 2)
    brand_sign = "+" if brand_diff >= 0 else ""
    brand_diff_color = "#15803D" if brand_diff >= 0 else "#B91C1C"

    top_rows = ""
    for c, v in img_top3:
        top_rows += (
            '<div class="idx-item">'
            f'<span class="idx-item-name">{IMG_LABELS.get(c, c)}</span>'
            f'<span class="idx-item-val-pos">{v}</span>'
            '</div>'
        )

    bot_rows = ""
    for c, v in img_bot3:
        bot_rows += (
            '<div class="idx-item">'
            f'<span class="idx-item-name">{IMG_LABELS.get(c, c)}</span>'
            f'<span class="idx-item-val-neg">{v}</span>'
            '</div>'
        )

    brand_card = (
        '<div class="idx-card compact-idx" style="display:flex;flex-direction:column;height:100%;">'
        '<div class="idx-title">Brand Image Index</div>'
        f'<div class="idx-value" style="color:{brand_color};">{brand_index}'
        '<span style="font-size:16px;color:#9B7B5A;">/6</span></div>'
        f'<div class="idx-sub">vs Kompetitor '
        f'<span style="color:{brand_diff_color};font-weight:700;">{brand_sign}{brand_diff}</span></div>'
        '<hr class="idx-divider">'
        '<div class="idx-list-label pos">▲ Atribut Terkuat</div>'
        f'{top_rows}'
        '<div class="idx-list-label neg" style="margin-top:6px;">▼ Perlu Ditingkatkan</div>'
        f'{bot_rows}'
        '</div>'
    )
    st.markdown(brand_card, unsafe_allow_html=True)

# ─ MPI Bars ─
with col_mpi:
    mpi_items = [
        ("Bank Utama Dana",      mpi_dana),
        ("Bank Utama Transaksi", mpi_trx),
        ("Bank Aktif Digunakan", mpi_aktif),
    ]

    bars_html = ""
    for lbl, val in mpi_items:
        bars_html += (
            '<div class="mpi-bar-box" style="background:white;border:1px solid #E8D9C8;'
            'border-radius:10px;box-shadow:0 1px 4px rgba(61,8,18,0.04);">'
            '<div class="mpi-bar-label" style="display:flex;justify-content:space-between;">'
            f'<span style="color:#374151;font-weight:500;">{lbl}</span>'
            f'<span style="color:#3D0812;font-weight:700;">XYZ {val}%</span>'
            '</div>'
            '<div class="mpi-bar-track" style="background:#F3EBE1;border-radius:99px;overflow:hidden;">'
            f'<div style="height:100%;width:{val}%;border-radius:99px;'
            'background:linear-gradient(90deg,#3D0812,#8B1A2E);"></div>'
            '</div>'
            '</div>'
        )

    mpi_card = (
        '<div class="idx-card compact-idx" style="display:flex;flex-direction:column;height:100%;">'
        '<div class="idx-title">Market Preference Index</div>'
        f'<div class="idx-value" style="color:#312E81;">{mpi_index}'
        '<span style="font-size:16px;color:#9B7B5A;">%</span></div>'
        '<div class="idx-sub">nasabah menjadikan XYZ sebagai bank utama</div>'
        '<hr class="idx-divider">'
        '<div style="display:flex;flex-direction:column;justify-content:space-between;'
        'flex:1;gap:20px;margin-top:14px;">'
        f'{bars_html}'
        '</div>'
        '</div>'
    )
    st.markdown(mpi_card, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# ════════════════════════════════════════════════════════════════════════════
# BARIS 4 — TOUCHPOINT SNAPSHOT
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">Touchpoint Snapshot</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

# Render touchpoint pakai st.columns — jauh lebih reliable daripada CSS grid
tp_cols = st.columns(len(tp_data))
for col_tp, tp in zip(tp_cols, tp_data):
    v    = tp["xyz"]
    vk   = tp["komp"]
    clr  = pct_color(v)
    lbl  = pct_label(v)
    diff = round(v - vk, 1)
    sign = "+" if diff >= 0 else ""
    diff_clr = "#15803D" if diff >= 0 else "#B91C1C"
    col_tp.markdown(f"""
    <div style="background:white;border:1px solid #E8D9C8;border-radius:10px;
                padding:14px 10px;text-align:center;
                box-shadow:0 1px 4px rgba(61,8,18,0.05);">
        <div style="font-size:9.5px;font-weight:700;color:#9B7B5A;
                    text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">
            {tp["label"]}
        </div>
        <div style="font-family:'DM Serif Display',serif;font-size:22px;color:{clr};">{v}%</div>
        <div style="font-size:9.5px;font-weight:600;color:{clr};margin-top:2px;">{lbl}</div>
        <div style="font-size:10px;color:{diff_clr};font-weight:700;margin-top:4px;">
            vs Komp {sign}{diff}%
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# BARIS 5 — ACTION REQUIRED (Full Width)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">Action Required</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)

action_items = []

# 1. NPS
if nps_score < 20:
    action_items.append(
        ("🔴", f"NPS kritis: {nps_score}", f"{detr_pct}% responden adalah Detractor — perlu segera ditangani"))
elif nps_score < 50:
    action_items.append(
        ("🟡", f"NPS di bawah target 50 (saat ini {nps_score})", "Push konversi Passive → Promoter lewat program loyalty"))

# 2. NPS vs Kompetitor
nps_gap = round(nps_score - nps_komp_score, 1)
if nps_gap < 0:
    action_items.append(
        ("🔴", f"NPS kalah dari kompetitor (gap {nps_gap})", "Review faktor pembeda layanan"))

# 3. CSI
if csi_pct < 65:
    action_items.append(
        ("🔴", f"CSI rendah: {csi_pct}% (Kritis)", "Tingkatkan kualitas layanan dasar"))
elif csi_pct < 80:
    action_items.append(
        ("🟡", f"CSI perlu ditingkatkan: {csi_pct}%", "Fokus pada peningkatan kepuasan nasabah"))

# 4. CLI
if cli_pct < 65:
    action_items.append(
        ("🔴", f"CLI rendah: {cli_pct}% (Kritis)", "Bangun program loyalitas untuk meningkatkan retensi"))
elif cli_pct < 80:
    action_items.append(
        ("🟡", f"CLI perlu ditingkatkan: {cli_pct}%", "Tingkatkan engagement nasabah"))

# 5. CES
if ces_score > 4:
    action_items.append(
        ("🟢", f"CES tinggi: {ces_score} (Mudah)", "Pertahankan performa yang baik"))
elif ces_score > 3:
    action_items.append(
        ("🟡", f"CES sedang: {ces_score}", "Optimasi alur layanan untuk memudahkan nasabah"))

# 6. MPI
if mpi_index < 50:
    action_items.append(
        ("🔴", f"MPI rendah: {mpi_index}%", "Perkuat positioning dan diferensiasi brand"))
elif mpi_index < 70:
    action_items.append(
        ("🟡", f"MPI sedang: {mpi_index}%", "Tingkatkan preferensi nasabah melalui value proposition"))

# 7. Brand Image
if brand_index < 3.5:
    action_items.append(
        ("🔴", f"Brand Image rendah: {brand_index}/6", "Bangun brand awareness dan reputasi"))
elif brand_index < 4.5:
    action_items.append(
        ("🟡", f"Brand Image sedang: {brand_index}/6", "Perkuat atribut brand yang lemah"))

# 8. Touchpoint kritis — bottom 3
for tp in tp_sorted_asc[:3]:
    if tp["xyz"] < 80:
        dot = "🔴" if tp["xyz"] < 65 else "🟡"
        diff_tp = round(tp["xyz"] - tp["komp"], 1)
        sign_tp = "+" if diff_tp >= 0 else ""
        action_items.append((dot,
                             f"{tp['label']}: {tp['xyz']}% ({pct_label(tp['xyz'])})",
                             f"vs Kompetitor {sign_tp}{diff_tp}% — review SOP dan staffing"))

# 9. Brand image terendah
if img_bot3:
    for i, (col, val) in enumerate(img_bot3[:2]):
        low_lbl = IMG_LABELS.get(col, col)
        dot = "🔴" if val < 3.5 else "🟡"
        action_items.append((dot,
                             f"Brand '{low_lbl}' lemah ({val}/6)",
                             "Pertimbangkan campaign peningkatan persepsi"))

# 10. Emotional negatif tertinggi
if top3_neg:
    for neg_col, neg_val in top3_neg[:2]:
        if neg_val > avg_pos * 0.5:
            neg_lbl = CEF_NEG_LABELS.get(neg_col, neg_col)
            dot = "🔴" if neg_val > 4 else "🟡"
            action_items.append((dot,
                                 f"Emosi '{neg_lbl}' tinggi ({neg_val})",
                                 "Review alur antrian dan waktu tunggu"))

# 11. Emotional positif terendah
if top3_pos:
    for pos_col, pos_val in top3_pos[-2:]:
        if pos_val < 4:
            pos_lbl = CEF_POS_LABELS.get(pos_col, pos_col)
            action_items.append(("🟡",
                                 f"Emosi '{pos_lbl}' rendah ({pos_val})",
                                 "Tingkatkan pengalaman positif nasabah"))

# 12. Cabang dengan NPS terendah
if len(cabang_nps) > 0:
    worst = cabang_nps.nsmallest(1, "promoter_pct").iloc[0]
    if worst['promoter_pct'] < 50:
        action_items.append(("🔴",
                             f"Cabang '{worst['nama_cabang']}' NPS terendah ({worst['promoter_pct']}% promoter)",
                             f"Provinsi: {worst['provinsi']} — {int(worst['responden'])} responden"))

# Jika tidak ada action items
if not action_items:
    action_items.append(
        ("✅", "Semua metrik dalam kondisi baik", "Pertahankan performa saat ini"))

# Tampilkan semua action items dalam satu kolom penuh (memanjang)
action_html = "".join([
    f"""<div style="background:white;border:1px solid #E8D9C8;border-radius:10px;
                padding:14px 18px;margin-bottom:8px;
                box-shadow:0 1px 4px rgba(61,8,18,0.05);
                border-left: 4px solid {'#EF4444' if dot == '🔴' else '#F59E0B' if dot == '🟡' else '#22C55E'};
                display:flex;align-items:center;gap:14px;">
        <span style="font-size:22px;flex-shrink:0;">{dot}</span>
        <div style="flex:1;">
            <div style="font-size:13.5px;font-weight:600;color:#1A0A10;">{title}</div>
            <div style="font-size:11.5px;color:#9B7B5A;margin-top:2px;">{meta}</div>
        </div>
    </div>"""
    for dot, title, meta in action_items
])

st.markdown(
    f'<div style="max-width:100%;">{action_html}</div>', unsafe_allow_html=True)