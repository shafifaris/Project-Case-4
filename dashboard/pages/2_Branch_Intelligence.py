import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import json

# ── CSS & STYLE (match Overview) ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&family=DM+Serif+Display&display=swap');

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
.exec-card.red::before    { background: linear-gradient(90deg, #B91C1C, #EF4444); }
.exec-icon  { font-size: 22px; margin-bottom: 10px; display: block; line-height: 1; }
.exec-label { color: #9B7B5A; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
.exec-value { font-family: 'DM Serif Display', serif; font-size: 32px; font-weight: 400; line-height: 1; margin-bottom: 6px; }
.exec-sub   { font-size: 11px; color: #9B7B5A; font-weight: 500; }
.exec-badge { display: inline-block; padding: 3px 8px; border-radius: 20px; font-size: 10px; font-weight: 700; margin-top: 8px; }
.badge-green  { background: #DCFCE7; color: #166534; }
.badge-yellow { background: #FEF9C3; color: #854D0E; }
.badge-red    { background: #FEE2E2; color: #991B1B; }

.idx-title  { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #9B7B5A; margin-bottom: 10px; }
.idx-item { display: flex; justify-content: space-between; align-items: center; padding: 6px 2px; border-bottom: 1px solid #FAF4EE; font-size: 12.5px; }
.idx-item:last-child { border-bottom: none; }
.idx-item-name { color: #374151; font-weight: 500; }
.idx-item-val-pos { font-weight: 700; color: #15803D; font-size: 12px; }
.idx-item-val-neg { font-weight: 700; color: #B91C1C; font-size: 12px; }
.idx-item-val-neu { font-weight: 700; color: #3D0812; font-size: 12px; }

.insight-box {
    font-size: 11.5px; color: #5C3D2E; margin-top: 8px; padding: 10px 12px;
    background: #FDF6EE; border-radius: 8px; border-left: 3px solid #C9932A;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border: 1px solid #E8D9C8 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px rgba(61,8,18,0.06);
    position: relative; overflow: hidden;
    padding: 6px 4px 2px;
}
div[data-testid="stVerticalBlockBorderWrapper"]::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #3D0812, #C9932A);
}

[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #E8D9C8; }
</style>
""", unsafe_allow_html=True)

# Mapping nama provinsi dari data ke KEY GeoJSON (NAME_1) agar konsisten dengan Overview
PROV_GEO_MAP = {
    "DKI Jakarta":       "JakartaRaya",
    "Jawa Barat":        "JawaBarat",
    "Jawa Tengah":       "JawaTengah",
    "Jawa Timur":        "JawaTimur",
    "Banten":            "Banten",
    "Bali":              "Bali",
    "Sumatera Utara":   "SumateraUtara",
    "Sumatera Selatan": "SumateraSelatan",
    "Lampung":          "Lampung",
    "Riau":             "Riau",
    "Kepulauan Riau":   "KepulauanRiau",
    "Kalimantan Selatan": "KalimantanSelatan",
    "Kalimantan Timur": "KalimantanTimur",
    "Sulawesi Selatan": "SulawesiSelatan",
}

# ── LOAD DATA & GEOJSON ───────────────────────────────────────────────────────
DETAIL_GROUPS = {
    "Banking Hall": [
        'tp_bh_jumlah_cabang_xyz', 'tp_bh_weekend_banking_xyz', 'tp_bh_penampilan_gedung_xyz',
        'tp_bh_area_parkir_xyz', 'tp_bh_kebersihan_parkir_xyz', 'tp_bh_kebersihan_masuk_xyz',
        'tp_bh_kebersihan_hall_xyz', 'tp_bh_tempat_duduk_xyz', 'tp_bh_ac_sejuk_xyz',
        'ruang_tunggu_nyaman_xyz', 'tp_bh_wifi_xyz', 'tp_bh_tv_xyz', 'tp_bh_wangi_xyz',
        'tp_bh_bersih_xyz', 'tp_bh_signage_pelayanan_xyz', 'tp_bh_kerapian_xyz', 'tp_bh_tata_letak_xyz',
        'tp_bh_ada_toilet_xyz', 'tp_bh_toilet_bersih_xyz', 'tp_bh_toilet_harum_xyz',
    ],
    "Security": [
        'tp_satpam_penampilan_rapi_xyz', 'tp_satpam_seragam_lengkap_xyz', 'tp_satpam_sambut_ramah_xyz',
        'tp_satpam_sopan_xyz', 'tp_satpam_ucap_salam_xyz', 'tp_satpam_tawar_bantuan_xyz',
        'tp_satpam_arahkan_nasabah_xyz', 'tp_satpam_beri_nomor_antrian_xyz', 'tp_satpam_atur_antrian_xyz',
        'tp_satpam_jumlah_memadai_xyz', 'tp_satpam_dalam_siaga_xyz',
    ],
    "Teller": [
        'tp_teller_antrian_cepat_xyz', 'tp_teller_sistem_antrian_xyz', 'tp_teller_layanan_cepat_xyz',
        'tp_teller_jumlah_mencukupi_xyz', 'tp_teller_penampilan_rapi_xyz', 'tp_teller_akurasi_transaksi_xyz',
        'tp_teller_sistem_komputer_xyz', 'tp_teller_pengetahuan_xyz', 'tp_teller_keramahan_xyz',
        'tp_teller_ucap_salam_xyz', 'tp_teller_keinginan_bantu_xyz', 'tp_teller_personal_approach_xyz',
    ],
    "Customer Service": [
        'tp_cs_keramahan_xyz', 'tp_cs_jumlah_mencukupi_xyz', 'tp_cs_pengetahuan_produk_xyz',
        'tp_cs_ketepatan_solusi_xyz', 'tp_cs_kecepatan_layanan_xyz', 'tp_cs_ketelitian_xyz',
        'tp_cs_antrian_cepat_xyz', 'tp_cs_pemahaman_nasabah_xyz', 'tp_cs_info_lengkap_akurat_xyz',
        'tp_cs_penampilan_rapi_xyz', 'tp_cs_keinginan_bantu_xyz', 'tp_cs_personal_approach_xyz',
        'tp_cs_ucap_salam_xyz',
    ],
    "Customer Assistant": [
        'tp_ca_keramahan_xyz', 'tp_ca_standby_xyz', 'tp_ca_pengetahuan_produk_xyz',
        'tp_ca_kecepatan_layanan_xyz', 'tp_ca_ketelitian_xyz', 'tp_ca_tangani_masalah_xyz',
        'tp_ca_pemahaman_nasabah_xyz', 'tp_ca_info_lengkap_akurat_xyz', 'tp_ca_penampilan_rapi_xyz',
        'tp_ca_keinginan_bantu_xyz', 'tp_ca_ucap_salam_xyz', 'tp_ca_personal_approach_xyz',
    ],
    "ATM": [
        'tp_atm_kemudahan_akses_xyz', 'tp_atm_ketersediaan_jenis_xyz', 'tp_atm_kelengkapan_fitur_xyz',
        'tp_atm_antrian_xyz', 'tp_atm_keamanan_xyz', 'tp_atm_kehandalan_xyz', 'tp_atm_lokasi_aman_xyz',
        'tp_atm_kenyamanan_xyz', 'tp_atm_pilihan_pecahan_xyz', 'tp_atm_stok_uang_xyz',
    ],
}
DETAIL_COLS = [c for cols in DETAIL_GROUPS.values() for c in cols]

OVERALL_COLS = [
    'overall_teller_xyz', 'overall_cs_xyz', 'overall_atm_xyz', 'overall_banking_hall_xyz',
    'overall_sekuriti_xyz', 'overall_operasional_xyz', 'overall_ca_xyz',
    'overall_parkir_xyz', 'overall_toilet_xyz', 'csi_xyz', 'cli_xyz', 'aksesibilitas_cabang_xyz',
]
TIME_COLS = [
    'waktu_tunggu_teller_aktual', 'waktu_tunggu_teller_toleransi',
    'waktu_tunggu_cs_aktual', 'waktu_tunggu_cs_toleransi',
    'waktu_ideal_tambah_teller', 'waktu_ideal_tambah_cs',
]


@st.cache_data
def load_data_and_geojson():
    BASE = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_excel(os.path.join(BASE, "..", "df_new.xlsx"))

    # Bersihkan nama kolom dari spasi tidak sengaja
    df.columns = df.columns.str.strip()

    def parse_nps(val):
        if pd.isna(val) or str(val).strip() == '':
            return np.nan
        try:
            return int(str(val).strip().split()[0])
        except:
            return np.nan

    df['nps_num'] = df['nps_xyz'].apply(parse_nps)
    df['nps_category'] = df['nps_num'].apply(
        lambda v: 'Promoter' if v >= 9 else (
            'Passive' if v >= 7 else 'Detractor')
        if not pd.isna(v) else np.nan)

    # Fungsi pembantu untuk mengekstrak angka dari teks skala (misal: "6 Sangat Mudah" -> 6)
    def clean_to_numeric(val):
        if pd.isna(val) or str(val).strip() == '':
            return np.nan
        try:
            # Ambil karakter angka pertama jika berbentuk teks kombinasi
            return pd.to_numeric(str(val).strip().split()[0], errors='coerce')
        except:
            return np.nan

    # Terapkan konversi numerik ke semua kolom metrik
    for c in OVERALL_COLS + DETAIL_COLS + TIME_COLS:
        if c in df.columns:
            # Jika kolom bertipe string/object, bersihkan teksnya dahulu
            if df[c].dtype == 'object':
                df[c] = df[c].apply(clean_to_numeric)
            else:
                df[c] = pd.to_numeric(df[c], errors='coerce')

    # Buat kolom persentase (_pct)
    for c in OVERALL_COLS + DETAIL_COLS:
        if c in df.columns:
            df[c + '_pct'] = (df[c] / 6 * 100).round(1)
        else:
            # Antisipasi jika kolom tetap tidak terbuat agar aplikasi tidak crash
            df[c + '_pct'] = np.nan

    # Load GeoJSON untuk Map
    geojson_path = os.path.join(BASE, "..", "indonesia_provinces.json")
    geojson_data = None
    if os.path.exists(geojson_path):
        with open(geojson_path, "r") as f:
            geojson_data = json.load(f)

    return df, geojson_data


df_raw, indonesia_geojson = load_data_and_geojson()


def pretty_label(col):
    name = col
    for pre in ['tp_bh_', 'tp_satpam_', 'tp_teller_', 'tp_cs_', 'tp_ca_', 'tp_atm_']:
        if name.startswith(pre):
            name = name[len(pre):]
            break
    name = name.replace('_xyz', '').replace('_', ' ').title()
    return name


def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0


def tier_color(metric, val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "#9CA3AF"
    if metric == "NPS":
        return "#15803D" if val >= 50 else ("#C9932A" if val >= 20 else "#B91C1C")
    return "#15803D" if val >= 80 else ("#C9932A" if val >= 65 else "#B91C1C")


def section_label(text):
    return f"""<div class="section-label">
        <span class="section-label-text">{text}</span>
        <div class="section-label-line"></div>
    </div>"""


# Global font style: Hitam Bold (#000000) untuk teks utama chart
PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color="#000000", size=11),
)

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
        "Overview":           "/Overview",
        "Branch Intelligence": "/Branch_Intelligence",
        "Touchpoint":          "/Touchpoint",
        "Customer Behaviour":  "/Customer_Behaviour",
        "Competitor":          "/Competitor",
    }
    icons = {"Overview": "◈", "Branch Intelligence": "▣",
             "Touchpoint": "◎", "Customer Behaviour": "◉", "Competitor": "◆"}
    for name, path in pages.items():
        active = "active" if name == "Branch Intelligence" else ""
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

    branch_opts = sorted(pool["nama_cabang"].dropna().unique().tolist())
    sel_branch = st.multiselect(
        "Cabang", branch_opts, placeholder="Semua Cabang")

    panel_opts = ["Semua", "Teller", "CS"]
    sel_panel = st.selectbox("Panel", panel_opts)

    # ── UBAH MENJADI MULTISELECT ──
    usia_opts = sorted(df_raw["range_usia"].dropna().unique().tolist())
    sel_usia = st.multiselect("Usia", usia_opts, placeholder="Semua Usia")

    st.markdown("<hr style='border-color:rgba(245,212,138,0.12);margin:16px 0;'>",
                unsafe_allow_html=True)
    st.markdown("<div style='font-size:9.5px;color:rgba(245,212,138,0.30);padding:0 4px;'>v3.1 · Bank XYZ Analytics</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_prov and "Semua" not in sel_prov:
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

# ════════════════════════════════════════════════════════════════════════════
# COMPUTED METRICS — BRANCH LEVEL (DIPERBAIKI)
# ════════════════════════════════════════════════════════════════════════════

# ── HITUNG NPS AGREGAT ──
total_promoters = int((df["nps_category"] == "Promoter").sum())
total_detractors = int((df["nps_category"] == "Detractor").sum())
total_responses = len(df)
avg_nps_agregat = round((total_promoters - total_detractors) /
                        total_responses * 100, 1) if total_responses > 0 else 0.0

if n > 0:
    branch_nps_agg = df.groupby("nama_cabang").agg(
        total_responden=("serial_id", "count"),
        promoters=("nps_category", lambda x: (x == "Promoter").sum()),
        detractors=("nps_category", lambda x: (x == "Detractor").sum()),
    ).reset_index()

    branch_nps_agg["nps_score"] = (
        (branch_nps_agg["promoters"] - branch_nps_agg["detractors"]) /
        branch_nps_agg["total_responden"] * 100
    ).round(1)

    branch_stats = df.groupby(["nama_cabang", "provinsi", "kab_kota"]).agg(
        responden=("serial_id", "count"),
        csi_pct=("csi_xyz_pct", "mean"),
        cli_pct=("cli_xyz_pct", "mean"),
        # CES menggunakan kolom _pct yang sudah diselaraskan di load_data
        ces_pct=("aksesibilitas_cabang_xyz_pct", "mean"),
        wait_teller=("waktu_tunggu_teller_aktual", "mean"),
        tol_teller=("waktu_tunggu_teller_toleransi", "mean"),
        wait_cs=("waktu_tunggu_cs_aktual", "mean"),
        tol_cs=("waktu_tunggu_cs_toleransi", "mean"),
        add_teller=("waktu_ideal_tambah_teller", "mean"),
        add_cs=("waktu_ideal_tambah_cs", "mean"),
    ).reset_index()

    branch_stats = branch_stats.merge(
        branch_nps_agg[["nama_cabang", "nps_score"]],
        on="nama_cabang",
        how="left"
    )

    branch_stats["csi_pct"] = branch_stats["csi_pct"].round(1)
    branch_stats["cli_pct"] = branch_stats["cli_pct"].round(1)
    branch_stats["ces_pct"] = branch_stats["ces_pct"].round(1)
    branch_stats["gap_teller"] = (
        branch_stats["wait_teller"] - branch_stats["tol_teller"]).round(1)
    branch_stats["gap_cs"] = (
        branch_stats["wait_cs"] - branch_stats["tol_cs"]).round(1)
else:
    branch_stats = pd.DataFrame(columns=["nama_cabang", "provinsi", "kab_kota", "responden", "csi_pct", "cli_pct", "ces_pct",
                                         "wait_teller", "tol_teller", "wait_cs", "tol_cs", "add_teller", "add_cs",
                                         "nps_score", "gap_teller", "gap_cs"])

METRIC_COL = {"CSI": "csi_pct", "NPS": "nps_score", "CLI": "cli_pct", "CES": "ces_pct"}

# ════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">▣ Bank XYZ · Customer Experience Intelligence</div>
    <h2>Branch Intelligence</h2>
    <p>{n:,} responden &nbsp;·&nbsp; {df['nama_cabang'].nunique()} cabang aktif &nbsp;·&nbsp; {df['provinsi'].nunique()} provinsi</p>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# KPI ROW — RINGKASAN CABANG (DIPERBAIKI DENGAN RATA-RATA TERTIMBANG)
# ════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("Ringkasan Cabang"), unsafe_allow_html=True)

# Perbaikan Statistik: Menggunakan Weighted Average agar akurat dan konsisten dengan level data mentah
if len(branch_stats) > 0 and branch_stats["responden"].sum() > 0:
    total_n = branch_stats["responden"].sum()
    avg_csi = round((branch_stats["csi_pct"] * branch_stats["responden"]).sum() / total_n, 1)
    avg_ces = round((branch_stats["ces_pct"] * branch_stats["responden"]).sum() / total_n, 1)
    n_critical = int(((branch_stats["csi_pct"] < 65) | (branch_stats["nps_score"] < 20)).sum())
else:
    avg_csi = 0.0
    avg_ces = 0.0
    n_critical = 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="exec-card maroon">
        <span class="exec-icon">▣</span>
        <div class="exec-label">Total Cabang Aktif</div>
        <div class="exec-value" style="color:#3D0812;">{df['nama_cabang'].nunique()}</div>
        <div class="exec-sub">Tersebar di {df['provinsi'].nunique()} provinsi</div>
    </div>""", unsafe_allow_html=True)
with c2:
    bc = "badge-green" if avg_nps_agregat >= 50 else ("badge-yellow" if avg_nps_agregat >= 20 else "badge-red")
    lbl = "Excellent" if avg_nps_agregat >= 50 else ("Good" if avg_nps_agregat >= 20 else "Needs Attention")
    st.markdown(f"""<div class="exec-card gold">
        <span class="exec-icon">📊</span>
        <div class="exec-label">Agregat NPS / Avg CES</div>
        <div class="exec-value" style="color:#7A5100;">{avg_nps_agregat} <span style="font-size:16px;color:#9B7B5A;">/ {avg_ces}%</span></div>
        <div class="exec-sub">Seluruh responden ({total_responses:,})</div>
        <span class="exec-badge {bc}">{lbl}</span>
    </div>""", unsafe_allow_html=True)
with c3:
    bc3 = "badge-green" if avg_csi >= 80 else ("badge-yellow" if avg_csi >= 65 else "badge-red")
    lbl3 = "Excellent" if avg_csi >= 80 else ("Good" if avg_csi >= 65 else "Needs Attention")
    st.markdown(f"""<div class="exec-card teal">
        <span class="exec-icon">⭐</span>
        <div class="exec-label">Rata-rata CSI Cabang</div>
        <div class="exec-value" style="color:#0F5E5A;">{avg_csi}<span style="font-size:16px;color:#9B7B5A;">%</span></div>
        <div class="exec-sub">Weighted average dari skala penuh</div>
        <span class="exec-badge {bc3}">{lbl3}</span>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="exec-card red">
        <span class="exec-icon">⚠</span>
        <div class="exec-label">Cabang Perlu Perhatian</div>
        <div class="exec-value" style="color:#B91C1C;">{n_critical}</div>
        <div class="exec-sub">CSI &lt; 65% atau NPS &lt; 20</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 1. GEOGRAPHIC PERFORMANCE MAP
# ════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("Geographic Performance Map"), unsafe_allow_html=True)

with st.container(border=True):
    top_row = st.columns([1, 3])
    with top_row[0]:
        map_metric = st.selectbox("Metric", ["CSI", "NPS", "CLI", "CES"], key="map_metric")
    st.markdown(f'<div class="idx-title">Performa Cabang per Provinsi — {map_metric}</div>', unsafe_allow_html=True)

    if len(branch_stats) > 0 and indonesia_geojson is not None:
        metric_col_map = METRIC_COL[map_metric]
        
        # Perbaikan Statistik: Groupby provinsi menggunakan weighted average berdasarkan responden cabang
        prov_geo = branch_stats.groupby("provinsi").apply(
            lambda x: pd.Series({
                "responden": x["responden"].sum(),
                "value": (x[metric_col_map] * x["responden"]).sum() / x["responden"].sum() if x["responden"].sum() > 0 else 0.0
            })
        ).reset_index()
        prov_geo["value"] = prov_geo["value"].round(1)

        prov_geo["geo_name"] = prov_geo["provinsi"].map(PROV_GEO_MAP)
        prov_geo = prov_geo.dropna(subset=["geo_name"])

        fig_map = go.Figure(go.Choropleth(
            geojson=indonesia_geojson,
            featureidkey="properties.NAME_1",
            locations=prov_geo["geo_name"],
            z=prov_geo["value"],
            colorscale=[[0, "#db7332"], [0.5, "#f59e0b"], [1, "#10b981"]] if map_metric != "NPS" else [[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#10b981"]],
            marker_line_color='#ffffff',
            marker_line_width=0.7,
            colorbar=dict(
                thickness=15,
                len=0.7,
                x=1.0,
                tickfont=dict(color="#374151", size=10),
                title=dict(text=f"Score<br>{map_metric}", font=dict(color="#374151", size=11))
            ),
            customdata=prov_geo[["provinsi", "responden", "value"]].values,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Total Responden: %{customdata[1]}<br>"
                "Avg Score: %{customdata[2]}<extra></extra>"
            ),
        ))

        fig_map.update_geos(
            scope="asia",
            center=dict(lat=-2.5, lon=118),
            projection_scale=1.0,
            bgcolor="rgba(0,0,0,0)",
            showland=False,
            showocean=True,
            oceancolor="#0f172a",
            showcoastlines=False,
            showcountries=False,
            showframe=False,
            lonaxis=dict(range=[94, 142]),
            lataxis=dict(range=[-11, 6]),
            visible=False
        )

        fig_map.update_layout(
            **PLOT,
            height=500,
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False
        )
        st.plotly_chart(fig_map, use_container_width=True)
    elif indonesia_geojson is None:
        st.warning("Berkas `indonesia_provinces.json` tidak ditemukan di folder utama. Silakan unggah berkas GeoJSON terlebih dahulu.")
    else:
        st.markdown("<div style='color:#000000;font-size:12px;padding:20px;'>Tidak ada data untuk filter yang dipilih.</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 2. BRANCH RANKING
# ════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("Branch Ranking"), unsafe_allow_html=True)

rank_top = st.columns([1, 3])
with rank_top[0]:
    rank_metric = st.selectbox("Ranking berdasarkan", ["CSI", "NPS", "CLI", "CES"], key="rank_metric")
metric_col_rank = METRIC_COL[rank_metric]
suffix_rank = "" if rank_metric == "NPS" else "%"

valid_rank = branch_stats.dropna(subset=[metric_col_rank]) if len(branch_stats) > 0 else branch_stats
col_top, col_bot = st.columns(2)

with col_top:
    with st.container(border=True):
        st.markdown(f'<div class="idx-title">▲ Top 10 Cabang — {rank_metric}</div>', unsafe_allow_html=True)
        if len(valid_rank) > 0:
            top10 = valid_rank.nlargest(10, metric_col_rank).sort_values(metric_col_rank)
            fig_top = go.Figure(go.Bar(
                x=top10[metric_col_rank], y=top10["nama_cabang"], orientation="h",
                marker_color="#15803D",
                text=[f"<b>{v:.1f}{suffix_rank}</b>" for v in top10[metric_col_rank]],
                textposition="outside", textfont=dict(color="#000000", size=10)
            ))
            fig_top.update_layout(**PLOT,
                                  xaxis=dict(color="#3D0812", gridcolor="#EEE4D8", tickfont=dict(size=11, weight="bold"), range=[0, 115]),
                                  yaxis=dict(color="#3D0812", tickfont=dict(size=11, weight="bold")),
                                  margin=dict(t=20, b=20, l=20, r=90), height=340)
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.markdown("<div style='color:#000000;font-size:12px;'>Data tidak tersedia.</div>", unsafe_allow_html=True)

with col_bot:
    with st.container(border=True):
        st.markdown(f'<div class="idx-title">▼ Bottom 10 Cabang — {rank_metric}</div>', unsafe_allow_html=True)
        if len(valid_rank) > 0:
            bot10 = valid_rank.nsmallest(10, metric_col_rank).sort_values(metric_col_rank, ascending=False)
            fig_bot = go.Figure(go.Bar(
                x=bot10[metric_col_rank], y=bot10["nama_cabang"], orientation="h",
                marker_color="#B91C1C",
                text=[f"<b>{v:.1f}{suffix_rank}</b>" for v in bot10[metric_col_rank]],
                textposition="outside", textfont=dict(color="#000000", size=10)
            ))
            fig_bot.update_layout(**PLOT,
                                  xaxis=dict(color="#3D0812", gridcolor="#EEE4D8", tickfont=dict(size=11, weight="bold"), range=[0, 115]),
                                  yaxis=dict(color="#3D0812", tickfont=dict(size=11, weight="bold")),
                                  margin=dict(t=20, b=20, l=20, r=90), height=340)
            st.plotly_chart(fig_bot, use_container_width=True)
        else:
            st.markdown("<div style='color:#000000;font-size:12px;'>Data tidak tersedia.</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 3. BRANCH DRIVER ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("Branch Driver Analysis"), unsafe_allow_html=True)

DRIVER_TP = [
    ("Teller", "overall_teller_xyz_pct"), ("CS", "overall_cs_xyz_pct"),
    ("ATM", "overall_atm_xyz_pct"), ("Security", "overall_sekuriti_xyz_pct"),
    ("Banking Hall", "overall_banking_hall_xyz_pct"), ("CA", "overall_ca_xyz_pct"),
    ("Operasional", "overall_operasional_xyz_pct"),
]
DRIVER_TP = [(lbl, c) for lbl, c in DRIVER_TP if c in df.columns]

with st.container(border=True):
    if len(branch_stats) > 0:
        branch_list_sorted = branch_stats.sort_values("csi_pct")["nama_cabang"].tolist()
        sel_driver_branch = st.selectbox("Pilih Cabang untuk Dianalisis", branch_list_sorted, index=0, key="driver_branch")
        st.markdown(f'<div class="idx-title">Mengapa performa cabang ini seperti ini? — {sel_driver_branch}</div>', unsafe_allow_html=True)

        branch_df_sel = df[df["nama_cabang"] == sel_driver_branch]
        network_avg = {lbl: round(safe_mean(df[col]), 1) for lbl, col in DRIVER_TP}
        branch_val = {lbl: round(safe_mean(branch_df_sel[col]), 1) for lbl, col in DRIVER_TP}

        labels_d = list(branch_val.keys())
        vals_d = [branch_val[l] for l in labels_d]
        avg_d = [network_avg[l] for l in labels_d]
        colors_d = [tier_color("CSI", v) for v in vals_d]

        fig_drv = go.Figure()
        fig_drv.add_trace(go.Bar(
            x=labels_d, y=vals_d, name=sel_driver_branch, marker_color=colors_d,
            text=[f"<b>{v}%</b>" for v in vals_d], textposition="outside",
            textfont=dict(color="#000000", size=10),
        ))
        fig_drv.add_trace(go.Scatter(
            x=labels_d, y=avg_d, name="Rata-rata Network", mode="lines+markers",
            line=dict(color="#3D0812", dash="dash", width=1.5),
            marker=dict(color="#3D0812", size=6),
        ))
        fig_drv.update_layout(**PLOT,
                              yaxis=dict(range=[0, 118], color="#000000", gridcolor="#EEE4D8", title="%"),
                              xaxis=dict(color="#000000"),
                              legend=dict(font=dict(size=10, color="#000000"), orientation="h", x=0, y=1.14),
                              margin=dict(t=46, b=10, l=10, r=10), height=340)
        st.plotly_chart(fig_drv, use_container_width=True)

        if vals_d:
            weakest_lbl, weakest_val = min(branch_val.items(), key=lambda x: x[1])
            st.markdown(f"""<div class="insight-box">
                💡 Touchpoint paling lemah di <b>{sel_driver_branch}</b> adalah
                <b style="color:#B91C1C;">{weakest_lbl}</b> ({weakest_val}%) —
                masalah cabang ini kemungkinan besar berasal dari area tersebut, bukan dari keseluruhan operasional cabang.
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#000000;font-size:12px;'>Tidak ada data untuk filter yang dipilih.</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 4. SERVICE BOTTLENECK
# ════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("Service Bottleneck"), unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)
with col_g1:
    with st.container(border=True):
        st.markdown('<div class="idx-title">⏱ Worst Waiting Time — Teller</div>', unsafe_allow_html=True)
        gt = branch_stats.dropna(subset=["gap_teller"]) if len(branch_stats) > 0 else branch_stats
        if len(gt) > 0:
            worst_teller = gt.nlargest(10, "gap_teller").sort_values("gap_teller")
            fig_gt = go.Figure(go.Bar(
                x=worst_teller["gap_teller"], y=worst_teller["nama_cabang"], orientation="h",
                marker_color=["#B91C1C" if v > 0 else "#15803D" for v in worst_teller["gap_teller"]],
                text=[f"<b>{'+' if v >= 0 else ''}{v:.1f} mnt</b>" for v in worst_teller["gap_teller"]],
                textposition="outside", textfont=dict(size=9, color="#000000"),
            ))
            fig_gt.update_layout(**PLOT, height=320, margin=dict(t=10, b=10, l=10, r=60),
                                 xaxis=dict(title="Gap Aktual − Toleransi (menit)", color="#000000", gridcolor="#EEE4D8"),
                                 yaxis=dict(tickfont=dict(size=9), color="#000000"))
            st.plotly_chart(fig_gt, use_container_width=True)
        else:
            st.markdown("<div style='color:#000000;font-size:12px;'>Data tidak tersedia.</div>", unsafe_allow_html=True)

with col_g2:
    with st.container(border=True):
        st.markdown('<div class="idx-title">⏱ Worst Waiting Time — CS</div>', unsafe_allow_html=True)
        gc = branch_stats.dropna(subset=["gap_cs"]) if len(branch_stats) > 0 else branch_stats
        if len(gc) > 0:
            worst_cs = gc.nlargest(10, "gap_cs").sort_values("gap_cs")
            fig_gc = go.Figure(go.Bar(
                x=worst_cs["gap_cs"], y=worst_cs["nama_cabang"], orientation="h",
                marker_color=["#B91C1C" if v > 0 else "#15803D" for v in worst_cs["gap_cs"]],
                text=[f"<b>{'+' if v >= 0 else ''}{v:.1f} mnt</b>" for v in worst_cs["gap_cs"]],
                textposition="outside", textfont=dict(size=9, color="#000000"),
            ))
            fig_gc.update_layout(**PLOT, height=320, margin=dict(t=10, b=10, l=10, r=60),
                                 xaxis=dict(title="Gap Aktual − Toleransi (menit)", color="#000000", gridcolor="#EEE4D8"),
                                 yaxis=dict(tickfont=dict(size=9), color="#000000"))
            st.plotly_chart(fig_gc, use_container_width=True)
        else:
            st.markdown("<div style='color:#000000;font-size:12px;'>Data tidak tersedia.</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 5. REGIONAL COMPARISON (DIPERBAIKI DENGAN RATA-RATA TERTIMBANG)
# ════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("Regional Comparison"), unsafe_allow_html=True)

reg_metric = st.selectbox("Metric", ["CSI", "NPS", "CLI", "CES"], key="reg_metric")
metric_col_reg = METRIC_COL[reg_metric]

col_pr, col_kr = st.columns(2)

with col_pr:
    with st.container(border=True):
        st.markdown(f'<div class="idx-title">Provinsi Ranking — {reg_metric}</div>', unsafe_allow_html=True)

        if len(branch_stats) > 0:
            # Perbaikan Statistik: Groupby provinsi menggunakan weighted average berdasarkan responden cabang
            prov_rank = branch_stats.groupby("provinsi").apply(
                lambda x: pd.Series({
                    "responden": x["responden"].sum(),
                    "value": (x[metric_col_reg] * x["responden"]).sum() / x["responden"].sum() if x["responden"].sum() > 0 else 0.0
                })
            ).reset_index().dropna(subset=["value"]).sort_values("value", ascending=False)

            fig_pr = go.Figure(
                go.Bar(
                    x=prov_rank["value"],
                    y=prov_rank["provinsi"],
                    orientation="h",
                    marker_color=[tier_color(reg_metric, v) for v in prov_rank["value"]],
                    text=[f"<b>{v:.1f}</b>" for v in prov_rank["value"]],
                    textposition="outside"
                )
            )
            fig_pr.update_layout(**PLOT, height=420, margin=dict(t=10, b=10, l=10, r=70), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_pr, use_container_width=True, key="prov_chart")
        else:
            st.markdown("<div style='color:#000000;font-size:12px;'>Data tidak tersedia.</div>", unsafe_allow_html=True)

with col_kr:
    with st.container(border=True):
        st.markdown(f'<div class="idx-title">Kota/Kabupaten Ranking — {reg_metric}</div>', unsafe_allow_html=True)

        if len(branch_stats) > 0:
            # Perbaikan Statistik: Groupby kab_kota menggunakan weighted average berdasarkan responden cabang
            kota_rank = branch_stats.groupby("kab_kota").apply(
                lambda x: pd.Series({
                    "responden": x["responden"].sum(),
                    "value": (x[metric_col_reg] * x["responden"]).sum() / x["responden"].sum() if x["responden"].sum() > 0 else 0.0
                })
            ).reset_index().dropna(subset=["value"]).sort_values("value", ascending=False).head(15)

            fig_kr = go.Figure(
                go.Bar(
                    x=kota_rank["value"],
                    y=kota_rank["kab_kota"],
                    orientation="h",
                    marker_color=[tier_color(reg_metric, v) for v in kota_rank["value"]],
                    text=[f"<b>{v:.1f}</b>" for v in kota_rank["value"]],
                    textposition="outside"
                )
            )
            fig_kr.update_layout(**PLOT, height=420, margin=dict(t=10, b=10, l=10, r=70), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_kr, use_container_width=True, key="kota_chart")
        else:
            st.markdown("<div style='color:#000000;font-size:12px;'>Data tidak tersedia.</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# APPENDIX — BRANCH DATA TABLE
# ════════════════════════════════════════════════════════════════════════════
st.markdown(section_label("Appendix — Branch Data Table"), unsafe_allow_html=True)

with st.container(border=True):
    if len(branch_stats) > 0:
        tbl = branch_stats[["nama_cabang", "provinsi", "kab_kota", "responden", "nps_score",
                            "csi_pct", "cli_pct", "ces_pct", "wait_teller", "wait_cs"]].copy()
        tbl.columns = ["Cabang", "Provinsi", "Kota/Kab", "Responden", "NPS", "CSI (%)", "CLI (%)", "CES (%)",
                       "Wait Teller (mnt)", "Wait CS (mnt)"]
        for c in ["NPS", "CSI (%)", "CLI (%)", "CES (%)", "Wait Teller (mnt)", "Wait CS (mnt)"]:
            tbl[c] = tbl[c].round(1)
        tbl = tbl.sort_values("CSI (%)", ascending=False).reset_index(drop=True)
        tbl.index += 1
        st.dataframe(tbl, use_container_width=True, height=380)
    else:
        st.markdown("<div style='color:#000000;font-size:12px;padding:10px;'>Tidak ada data untuk filter yang dipilih.</div>", unsafe_allow_html=True)