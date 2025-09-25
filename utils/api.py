import requests
import streamlit as st


BASE = "https://api.bmkg.go.id/publik/prakiraan-cuaca"


@st.cache_data(ttl=300)
def get_prakiraan(adm4: str):
"""Ambil data prakiraan cuaca BMKG untuk kode adm4. Mengembalikan JSON atau None."""
try:
params = { 'adm4': adm4 }
resp = requests.get(BASE, params=params, timeout=10)
resp.raise_for_status()
return resp.json()
except Exception as e:
st.error(f"Error saat fetch: {e}")
return None
