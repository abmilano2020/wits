import pandas as pd
import numpy as np
import folium
import webbrowser
import os

# import & clean file of title chances
df_chances = pd.read_excel('title_chances.xlsx')
df_chances = df_chances[['team', 'Title']]

df_chances['team'] = df_chances['team'].astype('string')
df_chances['team'] = df_chances['team'].str.strip().str.lower()

# import & clean file of teams stadium coordinates
df_teams = pd.read_csv('par_team_city.csv')
df_teams = df_teams.rename(columns={'Squadra': 'team'})
df_teams['team'] = df_teams['team'].astype('string')
df_teams['team'] = df_teams['team'].str.lower().str.strip()

mask = df_teams['team'] == 'hellas verona'

df_teams.loc[mask, 'team'] = df_teams.loc[mask, 'team'].apply(
    lambda x: ' '.join([w for w in x.split() if w != 'hellas'])
)

# merge teams and chances DFs
df_merged = pd.merge(df_teams, df_chances, on='team', how='inner')

# get lat/lon/weight
lat = df_merged['Latitudine'].values
lon = df_merged['Longitudine'].values
weight = df_merged['Title'].values

# calculate weighted center
avg_lat = np.average(lat, weights=weight)
avg_lon = np.average(lon, weights=weight)

# get Roma's coordinates to centre map
roma_row = df_merged[df_merged['Città'] == "Roma"].iloc[0]
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

for _, row in df_merged.iterrows():
    folium.Marker(
        location=[row['Latitudine'], row['Longitudine']],
        icon=football_icon
    ).add_to(m)

# save map
map_file = "wits.html"
m.save(map_file)

# open map in browser
webbrowser.open('file://' + os.path.realpath(map_file))