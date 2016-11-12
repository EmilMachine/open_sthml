#!/usr/bin/python

import sqlite3
import folium
from folium import plugins

query2 = '''SELECT 
 LocationNorthingCoordinate
, LocationEastingCoordinate
, stopAreaNumber
from stops s
join stop_area sp on 
    s.journey_pattern_point_number = sp.StopPointNumber
    where s.line_number = 1 and direction_code = 1
    ORDER BY LocationEastingCoordinate
'''

query = '''
SELECT 
 max(LocationNorthingCoordinate)
, max(LocationEastingCoordinate)
, l.id
from stop_area sa
join line_1 l
    on sa.StopPointName = l.stop_name
group by l.id
ORDER BY l.id
'''
#https://github.com/python-visualization/folium/blob/master/folium/plugins/heat_map.py
def heatmap_bus_line(conn, map, query):
    cur = conn.execute(query)
    data = []
    for row in cur.fetchall():
        data.append([row[0], row[1], row[2]])
    #map.add_child(plugins.HeatMap(data, min_opacity=0))
    map.add_child(folium.PolyLine(data, weight=5))

    for row in data:
        folium.CircleMarker(location=[row[0], row[1]], popup=str(row[2]), radius=5,  color='#ff0000').add_to(map)


    map.save('heatmap_bus.html')
    cur.close()

centerx=18.06912
centery=59.32379
xmin, xmax = 17.9129, 18.2617
ymin, ymax = 59.3720, 59.2708

conn = sqlite3.connect("../bus_get_raw/bus_raw_1week.db")
map = folium.Map(location=(centery, centerx), zoom_start=13, tiles='cartodbdark_matter')

#heatmap_restaurant(conn, map)
#heatmap_subway(conn, map)
#heatmap_school(conn, map)
heatmap_bus_line(conn, map, query)

conn.close()