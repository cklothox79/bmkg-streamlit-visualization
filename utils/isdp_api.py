import streamlit as st
import pandas as pd
from utils.isdp_api import get_wilayah, get_forecast

st.set_page_config(page_title="BMKG ISDP Forecast", page_icon="🌦️", layout="wide")
st.title("🌦️ BMKG ISDP Forecast Viewer")

st.sidebar.header("Pilih Wilayah")

# 1. Dropdown Provinsi
prov_df = get_wilayah()
prov_dict = {row["provinsi"]: row["adm1"] for _, row in prov_df.iterrows()}
provinsi = st.sidebar.selectbox("Provinsi", list(prov_dict.keys()))

# 2. Dropdown Kabupaten/Kota
kab_df = get_wilayah(adm1=prov_dict[provinsi])
kab_dict = {row["kotkab"]: row["adm2"] for _, row in kab_df.iterrows()}
kab = st.sidebar.selectbox("Kabupaten/Kota", list(kab_dict.keys()))

# 3. Dropdown Kecamatan
kec_df = get_wilayah(adm1=prov_dict[provinsi], adm2=kab_dict[kab])
kec_dict = {row["kecamatan"]: row["adm3"] for _, row in kec_df.iterrows()}
kec = st.sidebar.selectbox("Kecamatan", list(kec_dict.keys()))

# 4. Dropdown Desa/Kelurahan
kel_df = get_wilayah(adm1=prov_dict[provinsi], adm2=kab_dict[kab], adm3=kec_dict[kec])
kel_dict = {row.get("kelurahan", row.get("desa", "-")): row["adm4"] for _, row in kel_df.iterrows()}
kel = st.sidebar.selectbox("Kelurahan/Desa", list(kel_dict.keys()))

if st.sidebar.button("Ambil Data Prakiraan"):
    with st.spinner("Mengambil data dari BMKG ISDP..."):
        df = get_forecast(prov_dict[provinsi], kab_dict[kab], kec_dict[kec], kel_dict[kel])

    st.subheader(f"Prakiraan Cuaca: {kel}, {kec}, {kab}, {provinsi}")

    # Tabel Data
    st.dataframe(df[["local_datetime", "t", "hu", "weather_desc", "ws", "wd"]])

    # Grafik Suhu
    st.line_chart(df.set_index("local_datetime")["t"], height=300)

    # Grafik Kelembapan
    st.line_chart(df.set_index("local_datetime")["hu"], height=300)
