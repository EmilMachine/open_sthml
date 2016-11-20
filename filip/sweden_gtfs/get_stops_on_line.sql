
with base as (
select 
row_number() over (partition by trip_headsign) rn
, * from trips t
left join routes r on t.route_id = r.route_id
left join agency a on a.agency_id = r.agency_id
where route_short_name = '160'
and agency_name = 'SL'
and service_id = '000102'
)
,stops as (
select * from base b
left join stop_times st on b.trip_id = st.trip_id
left join stops s on st.stop_id = s.stop_id
)
select distinct on (stop_sequence::numeric)
route_short_name
, agency_name
, stop_name
, stop_sequence
, trip_headsign
 from stops 
 order by stop_sequence::numeric
