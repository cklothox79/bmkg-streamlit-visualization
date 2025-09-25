import pandas as pd
import plotly.express as px
import pydeck as pdk




def plot_time_series(df: pd.DataFrame):
"""Buat grafik waktu untuk suhu dan kelembapan. Mengharapkan kolom 'jamCuaca', 'tempC', 'humidity'."""
df2 = df.copy()
# memastikan kolom waktu
if 'jamCuaca' in df2.columns:
df2['jamCuaca'] = pd.to_datetime(df2['jamCuaca'])
else:
df2.index = pd.to_datetime(df2.index)


fig = px.line(df2, x='jamCuaca', y=['tempC', 'humidity'], labels={'value':'Nilai','variable':'Parameter','jamCuaca':'Waktu'})
fig.update_layout(margin=dict(l=10,r=10,t=30,b=10), height=350)
return fig




def make_map(df: pd.DataFrame):
"""Buat pydeck map sederhana dari koordinat jika tersedia di df (lat, lon)."""
# ambil titik pertama sebagai pusat bila ada
lat = None
lon = None
if 'latitude' in df.columns and 'longitude' in df.columns:
lat = float(df['latitude'].iloc[0])
lon = float(df['longitude'].iloc[0])
else:
# fallback: pusat Indonesia
lat, lon = -2.548926, 118.0148634


view = pdk.ViewState(latitude=lat, longitude=lon, zoom=6, pitch=0)
layer = pdk.Layer('ScatterplotLayer', data=[{'lat': lat, 'lon': lon}], get_position='[lon, lat]', get_radius=50000, pickable=True)
r = pdk.Deck(layers=[layer], initial_view_state=view)
return r
