import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database_vaksin import get_engine

import streamlit as st
from PIL import Image
import os

# =====================================================
# PATH & ASSETS
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")

icon_path = os.path.join(ASSET_DIR, "dinpert.png")
logo_path = os.path.join(ASSET_DIR, "dinpert.png")

page_icon = Image.open(icon_path) if os.path.exists(icon_path) else "🐄"

# =====================================================
# PAGE CONFIG (HARUS PALING ATAS)
# =====================================================
st.set_page_config(
    page_title="Dashboard Vaksinasi Ternak Kab. Sidoarjo",
    page_icon=page_icon,
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
/* === Background utama === */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        90deg,
        rgba(30,59,46,1) 2%,
        rgba(34,56,46,1) 57%,
        rgba(29,133,112,1) 100%
    );
}

/* === Sidebar === */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        rgba(19,38,30,1) 0%,
        rgba(29,133,112,1) 100%
    );
}

/* Padding konten */
.block-container {
    padding-top: 3rem;
}

/* Judul utama */
.big-title {
    font-size: 40px;
    font-weight: 700;
    text-align: center;
    color: white;
    line-height: 1.2;
}

/* Subjudul */
.sub-text {
    font-size: 16px;
    text-align: center;
    color: #e6e6e6;
    margin-top: 6px;
}

/* Card deskripsi */
.home-card {
    background: rgba(255,255,255,0.06);
    padding: 24px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(6px);
    width: 70%;
    margin: 25px auto;
}
.logo-padding {
    width: 20px;
    color: transparent;
    height: 20px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONTENT
# =====================================================

# Logo
if os.path.exists(logo_path):
    st.markdown('<div class="logo-padding"></div>', unsafe_allow_html=True)
    st.image(logo_path, width=160)
    st.markdown("</div>", unsafe_allow_html=True)


# Title
st.markdown(
    '<div class="big-title">Dashboard Vaksinasi Ternak<br>Kabupaten Sidoarjo</div>',
    unsafe_allow_html=True
)

# Subtitle
st.markdown(
    '<div class="sub-text">Sistem Informasi & Monitoring Program Vaksinasi Ternak</div>',
    unsafe_allow_html=True
)

# Description Card
st.markdown("""
<div class="home-card">
    <p style="color:white; text-align:center; font-size:15px;">
        Dashboard Vaksinasi Ternak Kabupaten Sidoarjo digunakan untuk mendukung pemantauan, pengelolaan, serta analisis data pelaksanaan vaksinasi ternak secara terintegrasi, interaktif, dan berbasis data, guna mendukung pengambilan keputusan dan evaluasi program kesehatan hewan.
    </p>
</div>
""", unsafe_allow_html=True)


# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="Dashboard Vaksin Ternak",
    layout="wide"
)

# ======================================
# LOAD DATA
# ======================================
engine = get_engine()

query = """
SELECT 
    program_vaksinasi,
    penyakit,
    provinsi,
    kabupaten,
    kecamatan,
    desa,
    tanggal_vaksinasi,
    bulan,
    bulan_numerik,
    tahun,
    hewan,
    jenis_kelamin,
    umur
FROM vaksin
"""

df = pd.read_sql(query, engine)

# ======================================
# PREPROCESSING (WAJIB)
# ======================================
df["bulan_numerik"] = df["bulan_numerik"].astype(int)
df["tahun"] = df["tahun"].astype(int)

urutan_bulan = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

bulan_available = (
    df[["bulan_numerik"]]
    .drop_duplicates()
    .sort_values("bulan_numerik")["bulan_numerik"]
    .tolist()
)

# ======================================
# NORMALISASI JENIS HEWAN
# ======================================

# Samakan format huruf (capitalize)
df["hewan"] = (
    df["hewan"]
    .astype(str)
    .str.strip()
    .str.lower()
    .str.capitalize()
)

# Standarisasi nilai (jaga-jaga typo)
mapping_hewan = {
    "Sapi": "Sapi",
    "Kambing": "Kambing",
    "Domba": "Domba",
    "Kerbau": "Kerbau",
    "Burung": "Burung",
    "Rusa": "Rusa"
}

df["hewan"] = df["hewan"].map(mapping_hewan).fillna("Lainnya")


# ======================================
# FILTER BAR (BI STYLE + OPSI "SEMUA")
# ======================================
st.markdown("### 🔎 Filter Data")

f1, f2, f3, f4 = st.columns(4)

# ---------- TAHUN ----------
with f1:
    tahun_options = ["Semua"] + sorted(df["tahun"].dropna().unique().tolist())

    tahun = st.multiselect(
        "📅 Tahun",
        options=tahun_options,
        default=["Semua"],
        placeholder="Pilih tahun"
    )

# ---------- BULAN ----------
with f2:
    bulan_options = ["Semua"] + bulan_available

    bulan = st.selectbox(
        "🗓️ Bulan",
        options=bulan_options,
        format_func=lambda x: urutan_bulan[x] if x != "Semua" else "Semua",
        index=0
    )

# ---------- KECAMATAN ----------
with f3:
    kecamatan_options = ["Semua"] + sorted(df["kecamatan"].dropna().unique().tolist())

    kecamatan = st.selectbox(
        "📍 Kecamatan",
        options=kecamatan_options,
        index=0
    )

# ---------- JENIS HEWAN ----------
with f4:
    hewan_options = ["Semua"] + sorted(df["hewan"].unique().tolist())

    hewan = st.selectbox(
        "🐄 Jenis Hewan",
        options=hewan_options,
        index=0
    )


# ======================================
# APPLY FILTER
# ======================================
df_filter = df.copy()

if tahun and "Semua" not in tahun:
    df_filter = df_filter[df_filter["tahun"].isin(tahun)]

if bulan != "Semua":
    df_filter = df_filter[df_filter["bulan_numerik"] == bulan]

if kecamatan != "Semua":
    df_filter = df_filter[df_filter["kecamatan"] == kecamatan]

if hewan != "Semua":
    df_filter = df_filter[df_filter["hewan"] == hewan]


# ======================================
# KPI CARDS
# ======================================
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

total = len(df_filter)

sapi = len(df_filter[df_filter["hewan"] == "Sapi"])
kambing = len(df_filter[df_filter["hewan"] == "Kambing"])
domba = len(df_filter[df_filter["hewan"] == "Domba"])
kerbau = len(df_filter[df_filter["hewan"] == "Kerbau"])
burung = len(df_filter[df_filter["hewan"] == "Burung"])
rusa = len(df_filter[df_filter["hewan"] == "Rusa"])

col1.metric("💉 Total Vaksinasi", f"{total:,}")
col2.metric("🐄 Sapi", sapi)
col3.metric("🐐 Kambing", kambing)
col4.metric("🐑 Domba", domba)
col5.metric("🐃 Kerbau", kerbau)
col6.metric("🐦 Burung", burung)
col7.metric("🦌 Rusa", rusa)

st.markdown("<hr>", unsafe_allow_html=True)


# ======================================
# LAYOUT 2 KOLOM
# ======================================
kiri, kanan = st.columns([2, 1])
import plotly.express as px

# ======================================
# KOLOM KIRI — TOP 5 TABEL
# ======================================
# ======================================
# KOLOM KIRI — TOP 5 TABEL
# ======================================
with kiri:

    # ---------- TOP 5 PROGRAM VAKSINASI ----------
    st.subheader("📋 Top 5 Program Vaksinasi")

    top5_vaksin = (
        df_filter
        .groupby("program_vaksinasi")
        .size()
        .reset_index(name="Jumlah Vaksinasi")
        .sort_values("Jumlah Vaksinasi", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    st.dataframe(
        top5_vaksin,
        use_container_width=True,
        height=220,
        hide_index=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- TOP 5 PENYAKIT ----------
    st.subheader("🦠 Top 5 Penyakit")

    top5_penyakit = (
        df_filter
        .groupby("penyakit")
        .size()
        .reset_index(name="Jumlah Kasus")
        .sort_values("Jumlah Kasus", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    st.dataframe(
        top5_penyakit,
        use_container_width=True,
        height=220,
        hide_index=True
    )



with kanan:
    st.subheader("📍 Top 5 Kecamatan Vaksinasi")

    top5_kecamatan = (
        df_filter
        .groupby("kecamatan")
        .size()
        .reset_index(name="Jumlah Vaksinasi")
        .sort_values("Jumlah Vaksinasi", ascending=False)
        .head(5)
    )

    fig_pie = px.pie(
        top5_kecamatan,
        names="kecamatan",
        values="Jumlah Vaksinasi",
        hole=0.45
    )

    fig_pie.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Jumlah: %{value:,}<br>Persentase: %{percent}"
    )

    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",   # luar chart
        plot_bgcolor="rgba(0,0,0,0)",    # dalam chart
        height=480,
        margin=dict(t=30, b=30, l=10, r=10)
    )

    st.plotly_chart(fig_pie, use_container_width=True)

import plotly.express as px
import streamlit as st

st.subheader("📈 Tren Vaksinasi per Tahun & Jenis Hewan")

line = (
    df_filter
    .groupby(["tahun", "hewan"])
    .size()
    .reset_index(name="Jumlah Vaksinasi")
    .sort_values("tahun")
)

fig_line = px.line(
    line,
    x="tahun",
    y="Jumlah Vaksinasi",
    color="hewan",
    markers=True,
    custom_data=["hewan"]
)

# =============================
# STYLE BIAR NYATU DENGAN PAGE
# =============================
fig_line.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",   # luar chart
    plot_bgcolor="rgba(0,0,0,0)",    # dalam chart
    font=dict(
        color="white",
        size=13
    ),
    legend=dict(
        title="Jenis Hewan",
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0
    ),
    xaxis=dict(
        showgrid=True,
        dtick=1,          # 🔑 tiap 1 tahun
        gridcolor="rgba(255,255,255,0.15)",
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)",
        zeroline=False
    ),
)

# =============================
# HOVER TEMPLATE (BERSIH)
# =============================
fig_line.update_traces(
    hovertemplate=
    "<b>Jenis Hewan:</b> %{customdata[0]}<br>"
    "<b>Tahun:</b> %{x}<br>"
    "<b>Jumlah:</b> %{y:,}<extra></extra>"
)

st.plotly_chart(fig_line, use_container_width=True)
