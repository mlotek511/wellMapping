import folium
from numpy import less_equal
import pandas as pd
import os
import json
import numpy as np

# Function that returns color of bubble based on well yield (GPM)
def wellColor(wellYield):
    if wellYield <= 2:
        return 'red'
    elif 2 < wellYield <= 5:
        return 'orange'
    else:
        return 'green'

pd.set_option('display.max_rows', None)  # or 1000
os.chdir(os.path.dirname(__file__))

startingLocation = [40.45250475241304, -80.01745415566245]
notification = "Well Marker"

# Read in an parse well data
print('# READING IN FILES.....', end = '')
df = pd.read_csv("C:/Users/mlote/Desktop/python_code/well_mapping/well_data_large.csv")
print(' COMPLETED!')

print('## PARSING WELL YIELD DATA.....', end = '')
df = df[pd.to_numeric(df['WellYield(gpm)'], errors='coerce').notnull()]
df['WellYield(gpm)'] = df['WellYield(gpm)'].astype(float, errors = 'raise')
print(' COMPLETED!')

print('### PARSING LAT AND LONG DATA.....', end = '')
df = df[pd.to_numeric(df['LatitudeDD'], errors='coerce').notnull()]
df['LatitudeDD'] = df['LatitudeDD'].astype(float, errors = 'raise')

df = df[pd.to_numeric(df['LongitudeDD'], errors='coerce').notnull()]
df['LongitudeDD'] = df['LongitudeDD'].astype(float, errors = 'raise')
print(' COMPLETED!')

print(df.dtypes)

# Well details in lists
lat              = list(df["LatitudeDD"])
lon              = list(df["LongitudeDD"])
wellYield        = list(df["WellYield(gpm)"])
name             = list(df["DateDrilled"])
wellDepth        = list(df["WellDepth(ft)"])
driller          = list(df["Driller"])
county           = list(df["County"])
municipality     = list(df["Municipality"])
depthbedrock     = list(df["DepthToBedrock(ft)"])
waterlevelstatic = list(df["StaticWaterLevel(ft)"])
casingdiameter   = list(df["CasingDiameter(in)"])

# Call folium and populate map
map = folium.Map(location = startingLocation, zoom_start = 11,  max_zoom=14, tiles = "Stamen Terrain")
fgv = folium.FeatureGroup(name="Well Map")

for lt, ln, wy, wd, nm, cy, my, db, wl, cd, dr in zip(lat, lon, wellYield, wellDepth, name, county, municipality, depthbedrock, waterlevelstatic, casingdiameter, driller):
    iframe = folium.IFrame(str(my).title() + "- " + str(cy).title() + " County<br>" + "Date Drilled: " + str(nm) + "<br>" + "Well Yield: " + str(wy)+ " gpm<br>" 
    + "Well Depth: " + str(wd) + " ft<br>" + "Static Water Level: " + str(wl) + "ft<br>" + "Casing Diameter: " + str(cd) + "in<br>" +"Depth to Bedrock: " + str(db) + " ft<br>" +"Drill Company: " + str(dr))
    
    popup = folium.Popup(iframe, min_width=300, max_width=500)
    
    marker = folium.CircleMarker([lt, ln], popup=popup, fill_color = wellColor(wy), color = 'grey', fill_opacity = 0.7).add_to(map)

# Write out .html
print('#### SAVING MAP DATA.....', end = '')
map.save("Well_Map.html")
print(' COMPLETED!')