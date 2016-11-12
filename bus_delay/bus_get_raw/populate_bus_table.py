import urllib2
import time
import sqlite3
### SIMPLE READ

bus_stations = [
{'name': 'Slussen', 'siteid':9192}
,{'name': 'Odenplan', 'siteid':9117}
,{'name': 'Liljeholmen', 'siteid':9294}
]

raw_format = 'json' 	# json or xml
timewindow = '60' 		# timewindow in min (max 60)
api_base = 'http://api.sl.se/api2/realtimedepartures.%s?key=%s&siteid=%s&timewindow=%s'

### NOTE: Cron needs absolute paths
# To run replace the base_path or remove it from api_file and con calls
base_path = '/Users/emil/Documents/code/open_data/open_sthml/emil/bus_notification/'

### NOTE: bus_api_key.txt is an txt file where first line is the api key for trafiklab
api_file = base_path + 'bus_api_key.txt' 
with open(api_file,'r') as f:
	api_key = f.readline().strip()


conn = sqlite3.connect(base_path + 'bus_raw_1.db')
c = conn.cursor()

for station in bus_stations:
	api_call = api_base % (raw_format,api_key,station['siteid'],timewindow)

	# read the homepage
	raw = urllib2.urlopen(api_call).read()
	
	# GET current time (local)
	call_time = time.strftime("%Y-%m-%M %H:%M:%S", time.localtime())

	query_store_data = ''' --
     	INSERT INTO busraw
 		(request_time, name, siteid, raw)
     	VALUES ('%s', '%s', %i, '%s');
     	''' % (call_time,station['name'],station['siteid'],raw)


	c.execute(query_store_data)

conn.commit()
conn.close()