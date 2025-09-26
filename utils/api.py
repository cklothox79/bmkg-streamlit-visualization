import requests
import pandas as pd

BASE_URL = "https://api.bmkg.go.id/publik/prakiraan-cuaca"


def get_prakiraan(adm4: str) -> pd.DataFrame:
    """
    Mengambil data prakiraan cuaca BMKG untuk wilayah adm4.
    - adm4: kode administrasi (contoh: '35.15.06.1001')

    Return: DataFrame berisi jamCuaca, tempC, humidity, dsb.
    """
    url = f"{BASE_URL}?adm4={adm4}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    # BMKG biasanya punya struktur nested: ambil dengan hati-hati
    try:
        cuaca_list = data["data"][0]["cuaca"]
    except Exception:
        raise ValueError("Format JSON BMKG berubah atau data tidak tersedia")

    df = pd.DataFrame(cuaca_list)
    return df
