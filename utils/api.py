import requests
import streamlit as st

# Endpoint dasar API BMKG
BASE = "https://api.bmkg.go.id/publik/prakiraan-cuaca"


@st.cache_data(ttl=300)
def get_prakiraan(adm4: str):
    """
    Mengambil data prakiraan cuaca BMKG untuk kode wilayah tingkat IV (adm4).

    Parameters
    ----------
    adm4 : str
        Kode wilayah tingkat IV, contoh: "31.71.03.1001"

    Returns
    -------
    dict | None
        Data JSON hasil request, atau None jika gagal.
    """
    try:
        params = {"adm4": adm4}
        resp = requests.get(BASE, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error saat mengambil data BMKG: {e}")
        return None
