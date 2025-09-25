import streamlit as st
import pandas as pd
from utils.api import get_prakiraan
from utils.visuals import plot_time_series, make_map


st.set_page_config(page_title="BMKG Visualizer", layout="wide")


st.title("BMKG — Visualisasi Prakiraan Cuaca")
st.caption("Sumber: API Publik BMKG · https://github.com/infoBMKG/data-cuaca")


with st.sidebar:
st.header("Kontrol")
adm4 = st.text_input("Kode wilayah (adm4)", value="31.71.03.1001")
btn = st.button("Ambil Data")


if btn and adm4:
with st.spinner("Mengambil data..."):
data = get_prakiraan(adm4)


if not data:
st.error("Gagal pengambilan data. Pastikan kode adm4 valid atau cek koneksi.")
else:
# Tampilkan ringkasan lokasi
lokasi = data.get('lokasi', {})
st.subheader(f"{lokasi.get('kota', '')} — {lokasi.get('kecamatan', '')}")


# Data waktu cuaca ke DataFrame
records = data.get('data', [])
df = pd.DataFrame(records)


col1, col2 = st.columns([1,2])
with col1:
st.metric("Cuaca sekarang", df.iloc[0].get('cuaca', '-'))
st.metric("Suhu (C)", df.iloc[0].get('tempC', '-'))
st.metric("Kelembapan (%)", df.iloc[0].get('humidity', '-'))


with col2:
st.plotly_chart(plot_time_series(df), use_container_width=True)


st.markdown("---")
st.subheader("Peta Lokasi")
st.pydeck_chart(make_map(df))


st.markdown("---")
st.subheader("Data mentah (JSON)")
st.json(data)
