import sqlite3
import json
import datetime
### NOTE: Cron needs absolute paths
# To run replace the base_path or remove it from api_file and con calls


### PARAMETERS
base_path = '/Users/emil/Documents/code/open_data/open_sthml/bus_delay/bus_get_raw/'
create_table_file = 'stop_area_table.sql'
clean_table = True # Flag to drop table before
table_name = 'stop_area'
data_in_file = 'stop_area.json'
db_file = base_path + 'bus_raw_1week.db'
batch_size = 1000

json_keys = ["StopPointNumber"
,"StopPointName"
,"StopAreaNumber"
,"LocationNorthingCoordinate"
,"LocationEastingCoordinate"
,"ZoneShortName"
,"StopAreaTypeCode"
,"LastModifiedUtcDateTime"
,"ExistsFromDate"]


query_insert_stop_base = '''INSERT INTO stop_area
	VALUES '''



# Read files
with open(create_table_file ,'r') as f:
	query_create_stop_area = f.read()

with open(data_in_file,'r') as f:
	stop_area_data = f.read()
	json_stop_area_data = json.loads(stop_area_data)


# GET cursur to db
conn = sqlite3.connect(db_file)
cwrite = conn.cursor()

# Create table 
if clean_table:
	cwrite.executescript('DROP TABLE IF EXISTS '+table_name+';')
cwrite.executescript(query_create_stop_area)
conn.commit()


# extract values from json and format them form insert.
insert_values = ''
for idx,stop_area in enumerate(json_stop_area_data['ResponseData']['Result']):

	stop_area_info = [stop_area[i] for i in json_keys]
	# Reformat time
	if insert_values != '':
		insert_values += ','

	
	insert_values += "(%s,'%s',%s,%s,%s,'%s','%s',strftime('%s'),strftime('%s'))" % tuple(stop_area_info)


	# Insert into db at batch size
	if (idx+1)%batch_size==0:
		print(idx)
		cwrite.executescript(query_insert_stop_base+insert_values+';')
		insert_values = ''		

# Insert any leftovers
if (idx+1)%batch_size!=0:
	cwrite.executescript(query_insert_stop_base+insert_values+';')

conn.commit()
conn.close()
