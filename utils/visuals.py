import pandas as pd
import plotly.express as px
import pydeck as pdk


def plot_time_series(df: pd.DataFrame):
    """
    Membuat grafik garis (line chart) suhu dan kelembapan
    berdasarkan waktu dari DataFrame BMKG.

    Kolom yang diperlukan:
    - jamCuaca : waktu prakiraan
    - tempC    : suhu (°C)
    - humidity : kelembapan (%)
    """
    df2 = df.copy()

    # Pastikan kolom jamCuaca menjadi datetime
    if "jamCuaca" in df2.columns:
        df2["jamCuaca"] = pd.to_datetime(df2["jamCuaca"])
    else:
        df2.index = pd.to_datetime(df2.index)

    fig = px.line(
        df2,
        x="jamCuaca",
        y=["tempC", "humidity"],
        labels={
            "value": "Nilai",
            "variable": "Parameter",
            "jamCuaca": "Waktu",
        },
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        height=350
    )
    return fig


def make_map(df: pd.DataFrame):
    """
    Membuat peta sederhana dengan PyDeck.
    Menggunakan kolom latitude & longitude
    (ambil baris pertama jika tersedia).
    """
    lat, lon = -2.548926, 118.0148634  # fallback: pusat Indonesia

    if "latitude" in df.columns and "longitude" in df.columns:
        try:
            lat = float(df["latitude"].iloc[0])
            lon = float(df["longitude"].iloc[0])
        except Exception:
            pass

    view = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=6,
        pitch=0
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"lat": lat, "lon": lon}],
        get_position="[lon, lat]",
        get_radius=50000,
        pickable=True,
        get_fill_color=[255, 0, 0, 160],
    )

    return pdk.Deck(layers=[layer], initial_view_state=view)
