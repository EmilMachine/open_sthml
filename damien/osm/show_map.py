#!/usr/bin/python

import sqlite3
import folium
from folium import plugins

#https://github.com/python-visualization/folium/blob/master/folium/plugins/heat_map.py
def heatmap_restaurant(conn, map ):
    cur = conn.execute("select lat,lon,name from entity where type = 'restaurant'")
    data = []
    for row in cur.fetchall():
        data.append([row[0], row[1], 1])
    #folium.CircleMarker(location=[row[0], row[1]], popup=row[2], radius=0.5,  color='#ff0000').add_to(map)
    map.add_child(plugins.HeatMap(data, min_opacity=0))
    map.save('restaurant.html')
    cur.close()

def heatmap_subway(conn, map):
    cur = conn.execute("select lat,lon,name from entity where type = 'subway_entrance'")
    data = []
    for row in cur.fetchall():
        data.append([row[0], row[1], 1])
    map.add_child(plugins.HeatMap(data, min_opacity=0.2, radius=50))
    map.save('metro.html')

def heatmap_school(conn, map):
    cur = conn.execute("select lat,lon,name from entity where type = 'school'")
    data = []
    for row in cur.fetchall():
        data.append([row[0], row[1], 1])
    map.add_child(plugins.HeatMap(data, min_opacity=0.3, radius=50))
    map.save('school.html')

def heatmap_parking(conn, map):
    cur = conn.execute("select lat,lon,name from entity where type = 'parking'")
    data = []
    for row in cur.fetchall():
        data.append([row[0], row[1], 1])
    map.add_child(plugins.HeatMap(data, min_opacity=0.3, radius=50))
    map.save('parking.html')

centerx=18.06912
centery=59.32379
xmin, xmax = 17.9129, 18.2617
ymin, ymax = 59.3720, 59.2708

conn = sqlite3.connect("osm.db")
map = folium.Map(location=(centery, centerx), zoom_start=13, tiles='cartodbdark_matter')

#heatmap_restaurant(conn, map)
#heatmap_subway(conn, map)
#heatmap_school(conn, map)
heatmap_parking(conn, map)

conn.close()