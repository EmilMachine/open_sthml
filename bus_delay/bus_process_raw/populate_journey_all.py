
import sqlite3
import json
import datetime
### SIMPLE READ

### NOTE: Cron needs absolute paths
# To run replace the base_path or remove it from api_file and con calls

with open('create_journey_table.sql','r') as f:
	query_create_jouney = f.read()

query_get_json = 'SELECT raw FROM busraw'




base_path = '/Users/emil/Documents/code/open_data/open_sthml/bus_delay/bus_get_raw/'


conn = sqlite3.connect(base_path + 'bus_raw_1week.db')

cwrite = conn.cursor()
cread = conn.cursor()

cwrite.executescript(query_create_jouney)
conn.commit()

cread.execute(query_get_json)

bus_keys = ["JourneyDirection",
"StopAreaName",
"TimeTabledDateTime",
"ExpectedDateTime",
"LineNumber"]


query_insert_bus_base = '''INSERT INTO journey (
	direction
	, goto_station 
	, time_timetable 
	, time_expected 
	, line 
	, time_last_updated 
	, time_delta) 
	VALUES '''


bus_values = ''
batch_size = 10

for idx,row in enumerate(cread.fetchall()):
	j = json.loads(row[0])
	print(idx)
	if ('ResponseData' in j) and ('LatestUpdate' in j['ResponseData']) and ('Buses' in j['ResponseData']):
		pass
	else:
		print('=== SPECIAL CASE ===')
		print(j)
		continue

	time_last_updated = j['ResponseData']['LatestUpdate']
	t_last_updated = datetime.datetime.strptime(time_last_updated, '%Y-%m-%dT%H:%M:%S')


	for bus in j['ResponseData']['Buses']:
		bus_info = [bus[i] for i in bus_keys]
		# Reformat time
		t_table = datetime.datetime.strptime(bus_info[2], '%Y-%m-%dT%H:%M:%S')
		t_expect = datetime.datetime.strptime(bus_info[3], '%Y-%m-%dT%H:%M:%S')
		bus_info[2] = t_table
		bus_info[3] = t_expect

		### Append info
		bus_info.append(t_last_updated)
		# Do time delta		
		bus_info.append((t_expect - t_table).total_seconds())

		if bus_values != '':
			bus_values += ','
		
		bus_values += "(%s,'%s',strftime('%s'),strftime('%s'),'%s',strftime('%s'),%s)" % tuple(bus_info)

		if (idx+1)%batch_size==0:
			cwrite.executescript(query_insert_bus_base+bus_values+';')
			bus_values = ''
			

conn.commit()
conn.close()
'''
ORDER IN businfo
, direction
, goto_station 
, time_timetable 
, time_expected 
, line 


, time_last_updated 
, time_delta 



85072
506428
'''

		






# PARSE DATA

# STORE DATA







