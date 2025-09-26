import requests
import pandas as pd

BASE_URL = "https://api.bmkg.go.id/publik/prakiraan-cuaca"

def get_prakiraan(adm4: str) -> pd.DataFrame:
    """
    Ambil prakiraan cuaca BMKG untuk kode adm4.
    Contoh: '35.15.06.1001'
    """
    url = f"{BASE_URL}?adm4={adm4}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    try:
        cuaca_list = data["data"][0]["cuaca"]
    except Exception:
        raise ValueError("Format JSON BMKG berubah atau data tidak ditemukan")

    return pd.DataFrame(cuaca_list)
