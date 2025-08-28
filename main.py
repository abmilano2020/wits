import pandas as pd
import numpy as np
import folium
import webbrowser
import os

df = pd.read_csv("par_team_city.csv")

# to be fetched automatically
city_weight = {
    "Bergamo":8.82,
    "Bologna":2.34,
    "Cagliari":0.01,
    "Como":0.77,
    "Cremona":0.05,
    "Firenze":2.47,
    "Genova":0.11,
    "Verona":0.01,
    "Milano":44.05,
    "Lecce":0.02,
    "Napoli":16.61,
    "Parma":0.06,
    "Pisa":0.01,
    "Roma":0,
    "Sassuolo":0,
    "Torino":9.26,
    "Udine":0.07
}

# group lat & lon by city, for cities with > 1 team
df_grouped = df.groupby(df.columns[1]).agg({
    df.columns[2]: 'mean',
    df.columns[3]: 'mean'
}).reset_index()

df_grouped.columns = ['city', 'lat', 'lon']

# add weights
df_grouped['weight'] = df_grouped['city'].map(city_weight)

# get lat/lon/weight
lat = df_grouped['lat'].values
lon = df_grouped['lon'].values
weight = df_grouped['weight'].values

# calculate center
avg_lat = np.average(lat, weights=weight)
avg_lon = np.average(lon, weights=weight)

# get Roma's coordinates to centre map
roma_row = df[df.iloc[:,1] == "Roma"].iloc[0]
lat_roma = float(roma_row.iloc[2])
lon_roma = float(roma_row.iloc[3])

# create map
m = folium.Map(location=[lat_roma, lon_roma], zoom_start=6, tiles='Esri.WorldImagery')

kw = {"prefix": "fa", "color": "red", "icon": "trophy"}
icon = folium.Icon(**kw)
folium.Marker(
    location=[avg_lat, avg_lon],
    icon=icon
).add_to(m)

football_design = {"prefix": "fa", "color": "blue", "icon": "futbol"}
football_icon = folium.Icon(**football_design)

for _, row in df_grouped.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        icon=football_icon
    ).add_to(m)

# save map
map_file = "wits.html"
m.save(map_file)

# open map in browser
webbrowser.open('file://' + os.path.realpath(map_file))
