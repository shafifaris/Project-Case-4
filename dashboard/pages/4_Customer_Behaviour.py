import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import re
import os

# ════════════════════════════════════════════════════════════════════════════
# CSS & STYLE
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background-color: #F8F4F0 !important; }
.block-container { padding: 1.2rem 2rem 2.5rem; background: #F8F4F0; max-width: 1400px; }

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

.page-header {
    background: linear-gradient(135deg, #3D0812 0%, #6B1020 60%, #8B1A2E 100%);
    border-radius: 16px; padding: 24px 30px; margin-bottom: 16px;
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
    letter-spacing: 0.14em; color: #C9932A; margin-bottom: 6px;
}
.page-header h2 {
    font-family: 'DM Serif Display', serif;
    color: #FDF0DC; font-size: 23px; font-weight: 400; margin: 0 0 4px 0;
}
.page-header p { color: rgba(253,240,220,0.50); font-size: 12px; margin: 0; }

.intel-note {
    background: #FDF6EE; border-left: 3px solid #C9932A; border-radius: 8px;
    padding: 9px 16px; font-size: 11.5px; color: #7A5100;
    margin-bottom: 16px; line-height: 1.5;
}
.intel-note b { color: #3D0812; }

.section-block { margin-bottom: 24px; }

.section-label {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 3px; margin-top: 2px;
}
.section-label-text {
    color: #3D0812; font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; white-space: nowrap;
}
.section-label-line {
    flex: 1; height: 1px; background: linear-gradient(90deg, #C4A882, transparent);
}
.section-caption { font-size: 11px; color: #9B7B5A; margin: 0 0 10px 0; }

/* ===== BUBBLE CARD untuk setiap chart Plotly (st.container(border=True)) ===== */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid #E8D9C8 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px rgba(61,8,18,0.06) !important;
    padding: 4px 10px 0px !important;
}
div[data-testid="stHorizontalBlock"] { gap: 14px; }

.comp-table-wrap {
    background: white; border-radius: 14px; padding: 14px 18px;
    border: 1px solid #E8D9C8; box-shadow: 0 2px 12px rgba(61,8,18,0.06);
    height: 100%;
}
.comp-table { width: 100%; border-collapse: collapse; }
.comp-table th {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: #9B7B5A; padding: 8px 10px;
    border-bottom: 2px solid #E8D9C8; text-align: left;
}
.comp-table th.right { text-align: right; }
.comp-table td { padding: 9px 10px; border-bottom: 1px solid #F3EBE1; font-size: 12.5px; vertical-align: middle; }
.comp-table tr:last-child td { border-bottom: none; }
.comp-table td.metric-name { font-weight: 600; color: #1A0A10; }
.comp-table td.val-r { text-align: right; font-weight: 700; color: #3D0812; }
.comp-table-scroll { max-height: 320px; overflow-y: auto; }

.risk-pill {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 10.5px; font-weight: 700; color: white;
}

[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #E8D9C8; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════════════════════════════════════
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

    for c in ['csi_xyz', 'cli_xyz']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
        df[c + '_pct'] = (df[c] / 6 * 100).round(1)

    cef_cols = ['cef_dihargai_xyz', 'cef_percaya_xyz',
                'cef_frustasi_xyz', 'cef_kecewa_xyz', 'cef_diabaikan_xyz']
    for c in cef_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    return df

df_raw = load_data()

def usia_sort_key(s):
    m = re.search(r'\d+', str(s))
    return int(m.group()) if m else 999

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
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
        active = "active" if name == "Customer Behaviour" else ""
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

# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════
def safe_mean(s):
    s2 = s.dropna()
    return float(s2.mean()) if len(s2) > 0 else 0.0

def pct_color(v):
    if pd.isna(v): return "#9B7B5A"
    return "#15803D" if v >= 80 else ("#B45309" if v >= 65 else "#B91C1C")

def nps_color(v):
    if pd.isna(v): return "#9B7B5A"
    if v >= 70: return "#15803D"
    if v >= 50: return "#4D9B3F"
    if v >= 0:  return "#C9932A"
    return "#B91C1C"

def mini_bar(pct, color):
    if pd.isna(pct):
        return '<span style="color:#9B7B5A;font-size:11.5px;">N/A</span>'
    w = max(2, min(100, pct))
    return (f'<div style="display:flex;align-items:center;gap:8px;">'
            f'<div style="flex:1;background:#F3EBE1;border-radius:6px;height:7px;overflow:hidden;">'
            f'<div style="width:{w}%;background:{color};height:100%;border-radius:6px;"></div></div>'
            f'<span style="font-weight:700;color:{color};font-size:12px;min-width:42px;text-align:right;">{pct:.1f}%</span></div>')

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(family="Inter", color="#5C3D2E", size=11),
)

PALETTE = ["#3D0812", "#8B1A2E", "#C9932A", "#0F5E5A", "#312E81"]
OTHER_COLOR = "#B0A18E"

def card(fig, key=None):
    """Bungkus chart Plotly dalam bubble card putih."""
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True, key=key)

def donut_capped(data, col, title, max_slices=4, height=205):
    """Donut chart, maks `max_slices` kategori bernama + 1 'Lainnya'. Tanpa legend,
    label & persen langsung di slice, detail lengkap saat hover."""
    counts = data[col].dropna().astype(str).value_counts()
    if len(counts) > max_slices:
        top = counts.iloc[:max_slices]
        other_sum = counts.iloc[max_slices:].sum()
        counts = pd.concat([top, pd.Series({"Lainnya": other_sum})])

    has_other = "Lainnya" in counts.index
    n_named = len(counts) - (1 if has_other else 0)
    colors = PALETTE[:n_named] + ([OTHER_COLOR] if has_other else [])

    fig = go.Figure(go.Pie(
        labels=counts.index.tolist(), values=counts.values.tolist(),
        hole=0.62, sort=False,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="label+percent", textposition="outside",
        textfont=dict(size=9.5, color="#3D0812"),
        hovertemplate="<b>%{label}</b><br>%{value} responden · %{percent}<extra></extra>",
    ))
    fig.update_layout(**PLOT, height=height, showlegend=False,
        margin=dict(t=38, b=14, l=30, r=30),
        title=dict(text=title, font=dict(color="#1A0A10", size=12, family="Inter"), x=0.5, y=0.98))
    return fig

def hbar(series, color, title="", fmt="{:.1f}%", height=250, top_n=None):
    """Horizontal bar — value langsung tertulis di ujung bar, axis angka disembunyikan
    biar tidak redundan. Tanpa legend (single trace)."""
    s = series.dropna()
    if top_n:
        s = s.sort_values(ascending=False).head(top_n).sort_values(ascending=True)
    else:
        s = s.sort_values(ascending=True)
    fig = go.Figure(go.Bar(
        x=s.values, y=s.index.astype(str), orientation="h",
        marker=dict(color=color),
        text=[fmt.format(v) for v in s.values],
        textposition="outside", textfont=dict(color="#5C3D2E", size=10),
        hovertemplate="<b>%{y}</b><br>%{x}<extra></extra>",
    ))
    fig.update_layout(**PLOT, showlegend=False,
        xaxis=dict(color="#9B7B5A", gridcolor="#EEE4D8", showticklabels=False),
        yaxis=dict(color="#374151", tickfont=dict(size=10)),
        margin=dict(t=34, b=10, l=10, r=55), height=height,
        title=dict(text=title, font=dict(color="#1A0A10", size=12, family="Inter"), x=0.02, y=0.97))
    return fig

def min_n_filter(g_df, seg_col, min_n=5):
    counts = g_df[seg_col].value_counts()
    valid = counts[counts >= min_n].index
    return g_df[g_df[seg_col].isin(valid)]

# ════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="page-header-tag">◉ Bank XYZ · Customer Experience Intelligence</div>
    <h2>Customer Intelligence</h2>
    <p>{n:,} responden terfilter &nbsp;·&nbsp; siapa di balik angka-angka di Overview</p>
</div>""", unsafe_allow_html=True)

if n == 0:
    st.warning("Tidak ada data untuk kombinasi filter ini.")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# RENDER HELPER (fix markdown-as-code-block bug)
# ════════════════════════════════════════════════════════════════════════════
def render_html(html: str, container=None):
    cleaned = "\n".join(line.lstrip() for line in html.strip().split("\n"))
    target = container if container is not None else st
    target.markdown(cleaned, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# HELPER: income bucket
# ════════════════════════════════════════════════════════════════════════════
def _income_bucket(val):
    nums = re.findall(r'\d+', str(val).replace(".", "").replace(",", ""))
    if nums:
        v = int(nums[0])
        if v < 3_000_000:   return "< Rp3 juta"
        if v < 6_000_000:   return "Rp3–6 juta"
        if v < 10_000_000:  return "Rp6–10 juta"
        if v < 15_000_000:  return "Rp10–15 juta"
        return "> Rp15 juta"
    return str(val)

INCOME_ORDER = ["< Rp3 juta", "Rp3–6 juta", "Rp6–10 juta", "Rp10–15 juta", "> Rp15 juta"]


# ════════════════════════════════════════════════════════════════════════════
# HELPER: hbar card & kpi card
# ════════════════════════════════════════════════════════════════════════════
def cc_hbar(title, series, top_n=None, bucket_fn=None, custom_order=None, container=None):
    counts = series.dropna().astype(str).value_counts()
    if bucket_fn is not None:
        counts = series.dropna().apply(bucket_fn).value_counts()
    if custom_order is not None:
        ordered = {k: counts.get(k, 0) for k in custom_order if k in counts.index}
        for k in counts.index:
            if k not in ordered:
                ordered[k] = counts[k]
        counts = pd.Series(ordered)
    counts = counts.sort_values(ascending=False)
    if top_n:
        counts = counts.head(top_n)

    total = counts.sum()
    max_v = counts.iloc[0] if len(counts) > 0 else 1

    rows_html = ""
    for i, (lbl, v) in enumerate(counts.items()):
        pct   = v / total * 100
        bar_w = v / max_v * 100
        lbl_safe = str(lbl).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        lbl_style  = "font-size:11px;font-weight:700;color:#1A0A10;" if i == 0 else "font-size:11px;font-weight:400;color:#374151;"
        fill_color = "#3D0812" if i == 0 else "#C4A882"
        pct_color_ = "#3D0812" if i == 0 else "#5C3D2E"
        rows_html += f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:7px;">
        <div style="width:140px;flex-shrink:0;white-space:nowrap;overflow:hidden;
        text-overflow:ellipsis;{lbl_style}" title="{lbl_safe}">{lbl_safe}</div>
        <div style="flex:1;background:#F3EBE1;border-radius:4px;height:6px;overflow:hidden;">
        <div style="width:{bar_w:.1f}%;height:100%;background:{fill_color};border-radius:4px;"></div>
        </div>
        <div style="font-size:11px;font-weight:700;color:{pct_color_};min-width:38px;text-align:right;">{pct:.1f}%</div>
        </div>"""

    render_html(f"""
    <div style="background:#fff;border:1px solid #E8D9C8;border-radius:14px;
    box-shadow:0 2px 12px rgba(61,8,18,0.06);padding:16px 18px;margin-bottom:4px;">
    <div style="font-size:11.5px;font-weight:700;color:#1A0A10;margin-bottom:12px;">{title}</div>
    {rows_html}
    </div>""", container=container)


def cc_kpi(label, value, sub="", badge="", container=None):
    val_len = len(str(value))
    val_fs = "23px" if val_len <= 15 else ("19.45px" if val_len <= 20 else "11.3px")
    
    badge_h = f'<div style="display:inline-block;margin-top:5px;background:#FDF3E3;color:#C9932A;font-size:9px;font-weight:700;padding:2px 8px;border-radius:20px;">{badge}</div>' if badge else ""
    render_html(f"""
    <div style="background:#fff;border:1px solid #E8D9C8;border-radius:14px;
    box-shadow:0 2px 12px rgba(61,8,18,0.06);padding:14px 16px;margin-bottom:4px;">
    <div style="font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:#9B7B5A;margin-bottom:5px;">{label}</div>
    <div style="font-size:{val_fs};font-weight:700;color:#3D0812;line-height:1.2;">{value}</div>
    <div style="font-size:10px;color:#9B7B5A;margin-top:2px;">{sub}</div>
    {badge_h}
    </div>""", container=container)

def cc_atm(ya_n, total_n, container=None):
    no_n = total_n - ya_n
    pct  = ya_n / total_n * 100 if total_n > 0 else 0
    render_html(f"""
    <div style="background:#fff;border:1px solid #E8D9C8;border-radius:14px;
    box-shadow:0 2px 12px rgba(61,8,18,0.06);padding:16px 18px;margin-bottom:4px;">
    <div style="font-size:11.5px;font-weight:700;color:#1A0A10;margin-bottom:14px;">Penggunaan ATM</div>
    <div style="display:flex;justify-content:space-around;align-items:center;">
    <div style="text-align:center;">
    <div style="font-size:28px;font-weight:700;color:#3D0812;line-height:1;">{pct:.1f}%</div>
    <div style="font-size:10px;color:#9B7B5A;margin-top:3px;">Menggunakan ATM</div>
    <div style="font-size:11px;font-weight:600;color:#5C3D2E;margin-top:1px;">{ya_n:,} nasabah</div>
    </div>
    <div style="width:1px;height:48px;background:#E8D9C8;"></div>
    <div style="text-align:center;">
    <div style="font-size:28px;font-weight:700;color:#C4A882;line-height:1;">{no_n:,}</div>
    <div style="font-size:10px;color:#9B7B5A;margin-top:3px;">Tidak pakai ATM</div>
    </div>
    </div>
    <div style="height:6px;background:#F3EBE1;border-radius:6px;overflow:hidden;margin-top:14px;">
    <div style="width:{pct:.1f}%;height:100%;background:#3D0812;border-radius:6px;"></div>
    </div>
    </div>""", container=container)

# ════════════════════════════════════════════════════════════════════════════
# 1 — CUSTOMER COMPOSITION
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-block">', unsafe_allow_html=True)
render_html("""
<div class="section-label">
<span class="section-label-text">Customer Composition</span>
<div class="section-label-line"></div>
</div>""")
render_html('<p class="section-caption">Profil demografi &amp; perilaku dasar nasabah.</p>')

# hitung dominan
def _dom(series):
    vc = series.dropna().astype(str).value_counts()
    if len(vc) == 0: return "—", "—"
    return str(vc.index[0]), f"{vc.iloc[0]/vc.sum()*100:.1f}%"

dom_g_lbl, dom_g_pct = _dom(df["jenis_kelamin"])
dom_u_lbl, dom_u_pct = _dom(df["range_usia"])
dom_s_lbl, dom_s_pct = _dom(df["kategori_nasabah"])
dom_t_lbl, dom_t_pct = _dom(df["lama_menjadi_nasabah"])
dom_f_lbl, _         = _dom(df["frekuensi_transaksi_xyz"])

_avc      = df["penggunaan_atm"].dropna().astype(str).str.strip().str.lower().value_counts()
_atm_ya_n = int(_avc.get("ya", 0))
_atm_pct  = f"{_atm_ya_n/n*100:.1f}%" if n > 0 else "—"

# headline
render_html(
    f'<div class="intel-note">'
    f'<b>Customer Snapshot:</b> Mayoritas nasabah <b>{dom_g_lbl} ({dom_g_pct})</b>, '
    f'usia <b>{dom_u_lbl}</b>, lama menjadi nasabah <b>{dom_t_lbl}</b>, '
    f'bertransaksi <b>{dom_f_lbl.lower()}</b>. '
    f'Segmen dominan: <b>{dom_s_lbl} ({dom_s_pct})</b>.'
    f'</div>'
)

# baris 1: KPI
k1, k2, k3, k4, k5 = st.columns(5)
cc_kpi("Gender Dominan", dom_g_lbl, f"dari {n:,} responden", dom_g_pct, container=k1)
cc_kpi("Usia Terbanyak", dom_u_lbl, "Tahun",                  dom_u_pct, container=k2)
cc_kpi("Segmen Utama",   dom_s_lbl, "Kategori nasabah",       dom_s_pct, container=k3)
cc_kpi("Lama Nasabah",   dom_t_lbl, "Mayoritas tenure",       "Loyal",   container=k4)
cc_kpi("Pengguna ATM",   _atm_pct,  "Dari total nasabah",     "Aktif",   container=k5)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# baris 2: Usia + Pekerjaan
r2a, r2b = st.columns(2)
cc_hbar("Kelompok Usia",     df["range_usia"],   container=r2a)
cc_hbar("Pekerjaan (Top 8)", df["pekerjaan"],    top_n=8, container=r2b)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# baris 3: Kategori + Penghasilan + Frekuensi
r3a, r3b, r3c = st.columns(3)
cc_hbar("Lama Jadi Nasabah", df["lama_menjadi_nasabah"], top_n=4, container=r3a)
cc_hbar("Penghasilan Bulanan", df["penghasilan_bulanan"],
        bucket_fn=_income_bucket, custom_order=INCOME_ORDER, top_n=4, container=r3b)
cc_hbar("Frekuensi Transaksi", df["frekuensi_transaksi_xyz"], top_n=4, container=r3c)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# 2 — SEGMENT EXPLORER
# ════════════════════════════════════════════════════════════════════════════
SEG_DIMENSIONS = {
    "Usia": "range_usia",
    "Pekerjaan": "pekerjaan",
    "Kategori Nasabah": "kategori_nasabah",
    "Gender": "jenis_kelamin",
    "Lama Menjadi Nasabah": "lama_menjadi_nasabah",
}

col_title, col_filter = st.columns([3, 1])
with col_title:
    st.markdown("""<div class="section-label">
        <span class="section-label-text">Segment Explorer</span>
        <div class="section-label-line"></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<p class="section-caption">Segmen mana yang paling puas, loyal, dan merekomendasikan? Diurutkan dari CSI tertinggi.</p>', unsafe_allow_html=True)
with col_filter:
    seg_label = st.selectbox("Dimensi Segmen", list(SEG_DIMENSIONS.keys()), key="seg_dim_select")

seg_col = SEG_DIMENSIONS[seg_label]
seg_base = min_n_filter(df, seg_col, min_n=5)

def segment_metrics(data, seg_col):
    rows = []
    for val, g in data.groupby(seg_col):
        if pd.isna(val) or len(g) == 0:
            continue
        n_nps = g["nps_num"].notna().sum()
        if n_nps > 0:
            prom = (g["nps_category"] == "Promoter").sum()
            detr = (g["nps_category"] == "Detractor").sum()
            nps = round((prom - detr) / n_nps * 100, 1)
        else:
            nps = np.nan
        rows.append({
            "segment": str(val), "n": len(g),
            "nps": nps,
            "csi": round(safe_mean(g["csi_xyz_pct"]), 1),
            "cli": round(safe_mean(g["cli_xyz_pct"]), 1),
        })
    return pd.DataFrame(rows)

seg_metrics = segment_metrics(seg_base, seg_col)

if len(seg_metrics) == 0:
    st.info("Belum cukup data per segmen untuk dimensi ini (minimal 5 responden/segmen).")
else:
    seg_sorted = seg_metrics.sort_values("csi", ascending=False)
    rows_html = ""
    for r in seg_sorted.itertuples():
        nps_disp = f"{r.nps:+.0f}" if not pd.isna(r.nps) else "N/A"
        rows_html += f"""<tr>
            <td class="metric-name">{r.segment}</td>
            <td style="color:#9B7B5A;font-size:11.5px;">{r.n}</td>
            <td><span class="risk-pill" style="background:{nps_color(r.nps)};">{nps_disp}</span></td>
            <td style="min-width:140px;">{mini_bar(r.csi, pct_color(r.csi))}</td>
            <td style="min-width:140px;">{mini_bar(r.cli, pct_color(r.cli))}</td>
        </tr>"""
    st.markdown(f"""
    <div class="comp-table-wrap">
        <table class="comp-table">
            <thead><tr>
                <th>{seg_label}</th><th>N</th><th>NPS</th><th>CSI</th><th>CLI</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>""", unsafe_allow_html=True)
    st.caption("Minimal 5 responden/segmen · diurutkan dari CSI tertinggi ke terendah.")
# ════════════════════════════════════════════════════════════════════════════
# 3 — WHO CHOOSES US? / WHO USES COMPETITORS?
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">Who Chooses Us? / Who Uses Competitors?</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)
st.markdown(f'<p class="section-caption">Berdasarkan {seg_label.lower()} — siapa yang menjadikan XYZ bank utama, dan ke mana yang lain berpaling.</p>', unsafe_allow_html=True)

def xyz_main_by_segment(data, seg_col, col="bank_utama_simpan_dana", min_n=5):
    rows = []
    for val, g in data.groupby(seg_col):
        if pd.isna(val) or len(g) < min_n:
            continue
        s = g[col].dropna().astype(str).str.strip()
        if len(s) == 0:
            continue
        pct = round((s == "Bank XYZ").mean() * 100, 1)
        rows.append((str(val), pct))
    return pd.Series(dict(rows))

def top_competitor_by_segment(data, seg_col, col="bank_aktif_selain_xyz", min_n=5):
    rows = []
    for val, g in data.groupby(seg_col):
        if pd.isna(val) or len(g) < min_n:
            continue
        all_banks = []
        for v in g[col].dropna():
            parts = [p.strip() for p in str(v).split(";")
                     if p.strip() and p.strip().upper() not in ("BANK XYZ", "XYZ", "-", "TIDAK ADA")]
            all_banks.extend(parts)
        if not all_banks:
            continue
        counts = pd.Series(all_banks).value_counts()
        rows.append({"segment": str(val), "top_competitor": counts.index[0],
                      "share_pct": round(counts.iloc[0] / len(g) * 100, 1)})
    return pd.DataFrame(rows)

def is_xyz_only(val):
    if pd.isna(val): return "Tidak Diketahui"
    banks = [b.strip() for b in str(val).split(";") if b.strip()]
    xyz_banks = [b for b in banks if "XYZ" in b]
    return "XYZ Only" if len(banks) == 1 and len(xyz_banks) == 1 else "Multi Bank"

w2, w3 = st.columns(2)

with w2:
    comp_df = top_competitor_by_segment(df, seg_col)
    if len(comp_df) == 0:
        rows_html = '<tr><td colspan="3" style="text-align:center;color:#9B7B5A;">Data belum cukup</td></tr>'
    else:
        comp_df = comp_df.sort_values("share_pct", ascending=False)
        rows_html = "".join([
            f"""<tr>
                <td class="metric-name">{r.segment}</td>
                <td>{r.top_competitor}</td>
                <td class="val-r">{r.share_pct}%</td>
            </tr>""" for r in comp_df.itertuples()
        ])
    st.markdown(f"""
    <div class="comp-table-wrap">
        <div class="comp-table-scroll">
        <table class="comp-table">
            <thead><tr><th>Segmen</th><th>Top Kompetitor</th><th class="right">Share</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
    </div>""", unsafe_allow_html=True)
    st.caption(f"Kompetitor terbanyak dipakai by {seg_label}")

with w3:
    df["bank_usage_type"] = df["bank_aktif_digunakan"].apply(is_xyz_only)
    card(donut_capped(df, "bank_usage_type", "XYZ Only vs Multi Bank", height=300))

# ════════════════════════════════════════════════════════════════════════════
# 4 — LOYALTY RISK
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-label">
    <span class="section-label-text">Loyalty Risk</span>
    <div class="section-label-line"></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="section-caption">Siapa yang berisiko berpindah — kombinasi CSI, CLI, dan NPS.</p>',
    unsafe_allow_html=True
)

# ────────────────────────────────────────────────────────────────────────────
# Risk Classification
# ────────────────────────────────────────────────────────────────────────────
def switching_risk(row):
    csi = row["csi_xyz_pct"] if not pd.isna(row["csi_xyz_pct"]) else 0
    cli = row["cli_xyz_pct"] if not pd.isna(row["cli_xyz_pct"]) else 0
    nps = row["nps_num"] if not pd.isna(row["nps_num"]) else 5

    if csi >= 80 and cli >= 80 and nps >= 9:
        return "Loyal"
    elif csi >= 75 and nps < 7:
        return "Vulnerable"
    elif csi < 70 and cli < 70 and nps < 7:
        return "At Risk"
    else:
        return "Neutral"

df["switching_risk"] = df.apply(switching_risk, axis=1)

risk_colors = {
    "Loyal": "#15803D",
    "Neutral": "#0F5E5A",
    "Vulnerable": "#C9932A",
    "At Risk": "#B91C1C",
}

risk_order = ["Loyal", "Neutral", "Vulnerable", "At Risk"]

# ────────────────────────────────────────────────────────────────────────────
# Layout 35% : 65%
# ────────────────────────────────────────────────────────────────────────────
col_risk, col_segment = st.columns([1, 2])

# ════════════════════════════════════════════════════════════════════════
# LEFT : PIE CHART SWITCHING RISK
# ════════════════════════════════════════════════════════════════════════
with col_risk:

    risk_counts = df["switching_risk"].value_counts()
    risk_counts = risk_counts.reindex(
        [r for r in risk_order if r in risk_counts.index]
    )

    total_risk = risk_counts.sum()

    fig_risk = go.Figure(
        go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            hole=0.55,
            marker=dict(
                colors=[risk_colors[r] for r in risk_counts.index]
            ),
            textinfo="percent",
            textfont=dict(size=11),
            hovertemplate=
                "<b>%{label}</b><br>"
                "%{value} responden"
                "<br>%{percent}"
                "<extra></extra>",
        )
    )

    fig_risk.update_layout(
        **PLOT,
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            font=dict(size=10),
        ),
        margin=dict(t=40, b=40, l=10, r=10),
        height=320,
        title=dict(
            text="Switching Risk",
            font=dict(size=12, color="#1A0A10"),
            x=0.02,
            y=0.96,
        ),
        annotations=[
            dict(
                text=f"<b>{total_risk}</b><br>Resp.",
                showarrow=False,
                font=dict(size=13, color="#5C3D2E")
            )
        ]
    )

    card(fig_risk)

# ════════════════════════════════════════════════════════════════════════
# RIGHT : RISK SEGMENT
# ════════════════════════════════════════════════════════════════════════
with col_segment:

    risk_seg = (
        min_n_filter(df, seg_col, min_n=5)
        .groupby([seg_col, "switching_risk"])
        .size()
        .reset_index(name="count")
    )

    if len(risk_seg) > 0:

        pivot = (
            risk_seg
            .pivot(
                index=seg_col,
                columns="switching_risk",
                values="count"
            )
            .fillna(0)
        )

        pivot_pct = (
            pivot.div(pivot.sum(axis=1), axis=0) * 100
        )

        fig_stack = go.Figure()

        for risk_cat in ["At Risk", "Vulnerable", "Neutral", "Loyal"]:

            if risk_cat in pivot_pct.columns:

                vals = pivot_pct[risk_cat]

                fig_stack.add_trace(
                    go.Bar(
                        name=risk_cat,
                        y=pivot_pct.index.astype(str),
                        x=vals,
                        orientation="h",
                        marker_color=risk_colors[risk_cat],
                        text=[
                            (
                                f"{risk_cat}<br>{v:.0f}%"
                                if v >= 15
                                else (
                                    f"{v:.0f}%"
                                    if v >= 7
                                    else ""
                                )
                            )
                            for v in vals
                        ],
                        textposition="inside",
                        insidetextanchor="middle",
                        textfont=dict(
                            color="white",
                            size=9
                        ),
                        hovertemplate=
                            f"<b>{risk_cat}</b><br>"
                            "%{y}: %{x:.1f}%"
                            "<extra></extra>",
                    )
                )

        fig_stack.update_layout(
            **PLOT,
            barmode="stack",
            showlegend=False,
            xaxis=dict(
                title="% Responden",
                color="#9B7B5A",
                gridcolor="#EEE4D8",
                range=[0, 100]
            ),
            yaxis=dict(
                color="#374151",
                tickfont=dict(size=10.5)
            ),
            margin=dict(
                t=40,
                b=10,
                l=10,
                r=10
            ),
            height=max(
                320,
                42 * len(pivot_pct)
            ),
            title=dict(
                text=f"Risk Segment by {seg_label}",
                font=dict(
                    size=12,
                    color="#1A0A10"
                ),
                x=0.02,
                y=0.96
            )
        )

        card(fig_stack)

# ════════════════════════════════════════════════════════════════════════════
# 5 — EMOTIONAL SEGMENTATION (heatmap, bukan grouped bar)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="section-label">
    <span class="section-label-text">Emotional Segmentation</span>
    <div class="section-label-line"></div>
</div>""", unsafe_allow_html=True)
st.markdown(f'<p class="section-caption">Siapa yang merasa frustrasi vs dihargai, by {seg_label.lower()}. Merah = perlu perhatian, hijau = sehat.</p>', unsafe_allow_html=True)

NEG_COLS = {"cef_frustasi_xyz": "Frustrasi", "cef_kecewa_xyz": "Kecewa", "cef_diabaikan_xyz": "Diabaikan"}
POS_COLS = {"cef_dihargai_xyz": "Dihargai", "cef_percaya_xyz": "Percaya"}

def build_heatmap(data, seg_col, cols_map, title, reverse, min_n=5):
    """Heatmap beranotasi: baris=segmen, kolom=dimensi emosi, nilai dianotasi di sel.
    reverse=True -> nilai tinggi dianggap buruk (emosi negatif), warna merah di atas.
    reverse=False -> nilai tinggi dianggap baik (emosi positif), warna hijau di atas.
    Tanpa legend / colorbar — semua info ada di axis + anotasi + hover."""
    seg_base2 = min_n_filter(data, seg_col, min_n=min_n)
    segs, z = [], []
    for val, g in seg_base2.groupby(seg_col):
        if pd.isna(val):
            continue
        segs.append(str(val))
        z.append([round(safe_mean(g[c]), 2) if c in g.columns else np.nan for c in cols_map.keys()])
    if not segs:
        return None

    x_labels = list(cols_map.values())
    text = [[f"{v:.1f}" if not pd.isna(v) else "-" for v in row] for row in z]

    fig = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=segs,
        colorscale="RdYlGn", reversescale=reverse,
        zmin=1, zmax=6, showscale=False,
        text=text, texttemplate="%{text}",
        textfont=dict(size=11, color="#1A0A10"),
        xgap=5, ygap=5,
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f} / 6<extra></extra>",
    ))
    fig.update_layout(**PLOT, height=max(220, 46 * len(segs) + 70),
        xaxis=dict(color="#374151", tickfont=dict(size=11)),
        yaxis=dict(color="#374151", tickfont=dict(size=10.5), autorange="reversed"),
        margin=dict(t=34, b=10, l=10, r=10),
        title=dict(text=title, font=dict(size=12, color="#1A0A10"), x=0.02, y=0.97))
    return fig

f1, f2 = st.columns(2)
with f1:
    fig_neg = build_heatmap(df, seg_col, NEG_COLS, f"Emosi Negatif by {seg_label}", reverse=True)
    if fig_neg is None:
        st.info("Data belum cukup.")
    else:
        card(fig_neg)
with f2:
    fig_pos = build_heatmap(df, seg_col, POS_COLS, f"Emosi Positif by {seg_label}", reverse=False)
    if fig_pos is None:
        st.info("Data belum cukup.")
    else:
        card(fig_pos)

st.markdown('</div>', unsafe_allow_html=True)