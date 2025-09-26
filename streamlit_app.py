import streamlit as st
import pandas as pd
from utils.isdp_api import get_wilayah, get_forecast

st.set_page_config(page_title="BMKG – Prakiraan Cuaca ISDP", layout="wide")
st.title("🌦️ Prakiraan Cuaca BMKG (API ISDP)")

st.sidebar.header("Pilih Wilayah")

# --- Input kode wilayah ---
prov_code = st.sidebar.text_input("Kode Provinsi (adm1)", "35")  # contoh Jawa Timur
kab_code  = st.sidebar.text_input("Kode Kabupaten/Kota (adm2)", "")
kec_code  = st.sidebar.text_input("Kode Kecamatan (adm3)", "")
kel_code  = st.sidebar.text_input("Kode Kelurahan (adm4)", "")

if st.sidebar.button("Ambil Data Wilayah"):
    with st.spinner("Mengambil daftar wilayah..."):
        try:
            wilayah = get_wilayah(prov_code or None,
                                  kab_code or None,
                                  kec_code or None,
                                  kel_code or None)
            st.subheader("Daftar Wilayah")
            st.write(pd.DataFrame(wilayah))
        except Exception as e:
            st.error(f"Gagal mengambil wilayah: {e}")

if st.sidebar.button("Ambil Data Prakiraan"):
    with st.spinner("Mengambil prakiraan cuaca..."):
        try:
            df = get_forecast(prov_code or None,
                               kab_code or None,
                               kec_code or None,
                               kel_code or None)
            if df.empty:
                st.warning("Tidak ada data prakiraan.")
            else:
                st.subheader("Prakiraan Cuaca")
                st.dataframe(df)

                # Contoh visualisasi suhu
                st.line_chart(df.pivot_table(index="waktu",
                                             values="suhu",
                                             aggfunc="mean"))
        except Exception as e:
            st.error(f"Gagal mengambil prakiraan: {e}")
