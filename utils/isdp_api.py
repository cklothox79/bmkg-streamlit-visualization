import requests
import pandas as pd

BASE_URL = "https://cuaca.bmkg.go.id/api/df/v1"

def get_wilayah(adm1=None, adm2=None, adm3=None, adm4=None):
    """
    Mengambil daftar kode wilayah berdasarkan level administrasi.
    """
    params = {}
    if adm1: params["adm1"] = adm1
    if adm2: params["adm2"] = adm2
    if adm3: params["adm3"] = adm3
    if adm4: params["adm4"] = adm4

    r = requests.get(f"{BASE_URL}/adm/list", params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def get_forecast(adm1=None, adm2=None, adm3=None, adm4=None):
    """
    Mengambil data prakiraan cuaca berdasarkan kode wilayah.
    """
    params = {}
    if adm1: params["adm1"] = adm1
    if adm2: params["adm2"] = adm2
    if adm3: params["adm3"] = adm3
    if adm4: params["adm4"] = adm4

    r = requests.get(f"{BASE_URL}/forecast/adm", params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    # contoh sederhana: ekstrak semua forecast menjadi DataFrame
    records = []
    for lokasi in data.get("lokasi", []):
        name = lokasi.get("lokasi")
        for fc in lokasi.get("cuaca", []):
            records.append({
                "lokasi": name,
                "waktu": fc.get("local_datetime"),
                "suhu": fc.get("t"),
                "cuaca": fc.get("weather_desc"),
                "kelembapan": fc.get("hu"),
                "angin": fc.get("ws"),
            })
    return pd.DataFrame(records)
