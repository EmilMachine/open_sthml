CREATE TABLE IF NOT EXISTS journey (
id integer primary key
,line varchar
, direction varchar
, goto_station varchar
, time_last_updated datetime
, time_timetable datetime
, time_expected datetime
, time_delta double
, UNIQUE(line,direction,goto_station,time_last_updated,time_timetable) ON CONFLICT IGNORE
);