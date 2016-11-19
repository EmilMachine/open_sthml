create table routes (
route_id text,
agency_id text,
route_short_name text,
route_long_name text,
route_type text,
route_url text
)


create table trips (
route_id text,
service_id text,
trip_id text,
trip_headsign text,
trip_short_name text 
)



select * from routes where route_short_name = '160' and agency_id = '275'

route_id,agency_id,route_short_name,route_long_name,route_type,route_url
"6024";"275";"160";"";"700";"http://www.resrobot.se/"