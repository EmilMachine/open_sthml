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


create table stop_times (
trip_id text,
arrival_time text,
departure_time text,
stop_id text,
stop_sequence text,
pickup_type text,
drop_off_type text )


create table stops (
stop_id text,
stop_name text,
stop_lat text,
stop_lon text,
location_type text
)


create table agency (
agency_id text,
agency_name text,
agency_url text,
agency_timezone text,
agency_lang text
)
