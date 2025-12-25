import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

# Load data
df = pd.read_csv("data_vaksinasi.csv")

st.set_page_config(page_title="Dashboard Vaksinasi Ternak", layout="wide")

# Sidebar Filters
st.sidebar.header("Filter Data")
tahun = st.sidebar.multiselect("Tahun", df['tahun'].unique(), default=df['tahun'].unique())
bulan = st.sidebar.multiselect("Bulan", df['bulan'].unique(), default=df['bulan'].unique())
kec = st.sidebar.multiselect("Kecamatan", df['kecamatan'].unique())
hewan = st.sidebar.multiselect("Jenis Hewan", df['hewan'].unique())

# Apply filter
filtered = df[
    df['tahun'].isin(tahun) &
    df['bulan'].isin(bulan) &
    df['hewan'].isin(hewan if hewan else df['hewan'])
]

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Hewan Vaksin", len(filtered))
col2.metric("Sapi", (filtered['hewan'] == "Sapi").sum())
col3.metric("Kambing", (filtered['hewan'] == "Kambing").sum())
col4.metric("Domba", (filtered['hewan'] == "Domba").sum())
col5.metric("Kerbau", (filtered['hewan'] == "Kerbau").sum())

# Chart Pola Bulanan
bulan_plot = filtered.groupby("bulan_numerik")['id'].count().reset_index()
fig1 = px.bar(bulan_plot, x='bulan_numerik', y='id', title="Pola Vaksinasi per Bulan")
st.plotly_chart(fig1, use_container_width=True)

# Pie Chart
fig2 = px.pie(filtered, names='hewan', title="Distribusi Jenis Hewan")
st.plotly_chart(fig2, use_container_width=True)

# Map
st.subheader("Peta Persebaran Vaksinasi")
m = folium.Map(location=[-7.45, 112.6], zoom_start=10)
for _, row in filtered.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=row['hewan'],
        color="blue"
    ).add_to(m)
st_folium(m, width=900)
