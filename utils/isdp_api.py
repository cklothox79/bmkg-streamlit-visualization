import requests
from typing import Optional, Dict, Any

# Base URL API ISDP BMKG
BASE_URL = "https://cuaca.bmkg.go.id/api/df/v1"


def _fetch_json(endpoint: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Helper untuk GET request dan memastikan response JSON.
    """
    url = f"{BASE_URL}{endpoint}"
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Gagal mengambil data: {e}")

    # Pastikan API memang mengembalikan JSON
    if not r.headers.get("Content-Type", "").lower().startswith("application/json"):
        raise RuntimeError(f"Response bukan JSON:\n{r.text[:200]}")
    return r.json()


def get_wilayah(adm1: str = "",
                adm2: str = "",
                adm3: str = "",
                adm4: str = "") -> Dict[str, Any]:
    """
    Mengambil daftar kode wilayah bertingkat.
    - Isi hanya adm1 → dapat daftar kab/kota
    - Isi adm1 + adm2 → dapat daftar kecamatan
    - Dst.
    """
    params = {}
    if adm1: params["adm1"] = adm1
    if adm2: params["adm2"] = adm2
    if adm3: params["adm3"] = adm3
    if adm4: params["adm4"] = adm4

    return _fetch_json("/adm/list", params)


def get_forecast(adm1: str = "",
                 adm2: str = "",
                 adm3: str = "",
                 adm4: str = "") -> Dict[str, Any]:
    """
    Mengambil prakiraan cuaca untuk wilayah tertentu.
    Isi kode wilayah sesuai level yang diinginkan:
    - adm1 saja → seluruh provinsi
    - adm1 + adm2 → kab/kota
    - dst.
    """
    params = {}
    if adm1: params["adm1"] = adm1
    if adm2: params["adm2"] = adm2
    if adm3: params["adm3"] = adm3
    if adm4: params["adm4"] = adm4

    return _fetch_json("/forecast/adm", params)


# ------------------------------
# Contoh penggunaan (uji lokal)
# ------------------------------
if __name__ == "__main__":
    # Ambil daftar kab/kota di Jawa Timur (adm1=35)
    try:
        kab = get_wilayah(adm1="35")
        print("Daftar kab/kota Jawa Timur:", kab[:3])  # tampilkan 3 teratas
    except Exception as e:
        print("Error wilayah:", e)

    # Ambil prakiraan cuaca contoh (isi kode yang valid)
    try:
        prakiraan = get_forecast(adm1="35", adm2="35.15", adm3="35.15.02", adm4="35.15.02.2018")
        print("Contoh prakiraan:", list(prakiraan.keys()))
    except Exception as e:
        print("Error prakiraan:", e)
