import streamlit as st
from data_preprocessing import load_and_preprocess


st.set_page_config(
    page_title="Cek Data Preprocessing",
    layout="wide"
)

st.title("🔍 Cek Data Hasil Preprocessing")

with st.spinner("Mengambil & memproses data dari MySQL..."):
    df = load_and_preprocess()

st.success("✅ Data berhasil dimuat")

# Info cepat
st.write("Jumlah baris:", len(df))
st.write("Jumlah kolom:", df.shape[1])

# Tampilkan 100 baris pertama
st.dataframe(df.head(100), use_container_width=True)

# Cek tipe data
st.subheader("Tipe Data Kolom")
st.dataframe(df.dtypes.astype(str))
