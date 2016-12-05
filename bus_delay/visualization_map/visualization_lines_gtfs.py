#!/usr/bin/python

#import psycopg2 as pg
import folium
from folium import plugins

data2 =[[18.1179752, 59.3415023, 'Stockholm Frihamnen'], [18.1141778, 59.3404651, 'Frihamnsporten'], [18.1120296, 59.3422273, 'Sehlstedtsgatan'], [18.110355, 59.3429394, 'Osthammarsgatan'], [18.1095174, 59.344849, 'Rokubbsgatan']]
data = [[i[1],i[0],i[2]] for i in data2]

#https://github.com/python-visualization/folium/blob/master/folium/plugins/heat_map.py
def heatmap_bus_line(con, map, query):


    #data = data[0:5]
    #print(data)

    #map.add_child(plugins.HeatMap(data, min_opacity=0))
    map.add_child(folium.PolyLine(data, weight=5))

    for row in data:
        folium.CircleMarker(location=[row[0], row[1]], popup=str(row[2]), radius=5,  color='#ff0000').add_to(map)


    map.save('heatmap_bus.html')
    #cur.close()

centerx=18.06912
centery=59.32379
xmin, xmax = 17.9129, 18.2617
ymin, ymax = 59.3720, 59.2708


filename='../sweden_gtfs/get_single_stop.sql'
query=''
with open(filename, 'r') as fd:
    query = fd.read().replace('\n', ' ')

filename='stupid.csv'
with open(filename, 'r') as fd:
    stupid = fd.read().split('\n')
    station = map(lambda x: x.split(';'), stupid)
    
    data = [[float(i[1]),float(i[0]),i[4]] for i in station]
    print(data)

#conn = sqlite3.connect("../bus_get_raw/bus_raw_1week.db")
# conn = pg.connect(host='localhost', database='trafiklab', user='postgres')

# print(query)
# cur = con.cursor()
# cur.execute('''with base as (
# select 
# s.stop_sequence
# ,s.stop_id
# ,st.stop_name
# ,t.trip_headsign
# ,t.service_id
# ,count(*)
# from stop_times s
# left join trips t on t.trip_id = s.trip_id
# left join stops st on st.stop_id = s.stop_id
# left join routes r on t.route_id = r.route_id
# left join agency a on a.agency_id = r.agency_id 
# where route_short_name = '1'
# and a.agency_name = 'SL'
# and t.service_id = '001191'
# GROUP BY s.stop_sequence,s.stop_id,st.stop_name,t.trip_headsign, t.service_id
# --having count(*) = 811
# --order by cast(s.stop_sequence as INT)
# )
# select b.*, s.stop_lat::DOUBLE PRECISION, s.stop_lon::DOUBLE PRECISION 
# from base b
# left join stops s using (stop_id)
# ORDER BY trip_headsign,stop_sequence::numeric''')
# data = []
# for row in cur.fetchall():
#     data.append([row[6], row[7], row[2]])

# with open("local_data.csv","w") as f:



map = folium.Map(location=(centery, centerx), zoom_start=13, tiles='cartodbdark_matter')

#heatmap_restaurant(conn, map)
#heatmap_subway(conn, map)
#heatmap_school(conn, map)
conn = None
heatmap_bus_line(conn, map, query)

#conn.close()