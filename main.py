import pandas as pd
import numpy as np
import folium
import webbrowser
import os

df = pd.read_csv("par_team_city.csv")

# to be fetched automatically
team_weight = {
    "Atalanta": 7.47,
    "Bologna": 3.47,
    "Cagliari": 0.02,
    "Como": 0.60,
    "Cremonese": 0.11,
    "Fiorentina": 2.25,
    "Genoa": 0.12,
    "Hellas Verona": 0,
    "Inter": 25.14,
    "Milan": 5.13,
    "Juventus": 13.01,
    "Lazio": 3.34,
    "Lecce": 0,
    "Napoli": 20.86,
    "Parma": 0.07,
    "Pisa": 0,
    "Roma": 17.97,
    "Sassuolo": 0,
    "Torino": 0.25,
    "Udinese": 0.19
}

# add team's weights (title chances)
df['weight'] = df['Squadra'].map(team_weight)

# get lat/lon/weight
lat = df['Latitudine'].values
lon = df['Longitudine'].values
weight = df['weight'].values

# calculate weighted center
avg_lat = np.average(lat, weights=weight)
avg_lon = np.average(lon, weights=weight)

# get Roma's coordinates to centre map
roma_row = df[df['Città'] == "Roma"].iloc[0]
lat_roma = float(roma_row['Latitudine'])
lon_roma = float(roma_row['Longitudine'])

# create map
m = folium.Map(location=[lat_roma, lon_roma], zoom_start=6, tiles='Esri.WorldImagery')

scudetto_image = "Scudetto.png"

icon = folium.CustomIcon(
    scudetto_image,
    icon_size=(25, 25),
    icon_anchor=(25, 25)
)

folium.Marker(
    location=[avg_lat, avg_lon],
    icon=icon
).add_to(m)

football_design = {"prefix": "fa", "color": "blue", "icon": "futbol"}
football_icon = folium.Icon(**football_design)

for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitudine'], row['Longitudine']],
        icon=football_icon
    ).add_to(m)

# save map
map_file = "wits.html"
m.save(map_file)

# open map in browser
webbrowser.open('file://' + os.path.realpath(map_file))
