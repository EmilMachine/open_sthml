
var caller = require("./api_caller");
var staionHandler = require("./train_stations");


//train.getStationCoordinates("Mst")





function handle_train_departures(data){
	//console.log(data)
	departures = JSON.parse(data).RESPONSE.RESULT[0].TrainAnnouncement
	for (var i = 0; i < departures.length; i++) {
		departure = departures[i];
		//console.log(departure);
		stationSign = departure.LocationSignature;
		goingTo = departure.ToLocation.LocationName;
		station = staionHandler.getStation(stationSign);
		//console.log(station);
		console.log("Train " + departure.AdvertisedTrainIdent + " departured from " + station.name + " at " + departure.TimeAtLocation);
		console.log("but should have departured at " + departure.AdvertisedTimeAtLocation);
		console.log("next station is " + staionHandler.getStation(departure.ToLocation[0]).name);
		console.log("--------------------------------------------")
		//console.log("Tran departuring from " + station.name + " (" + station.lon + ", " + station.lat + ")");
		//console.log("going to" /*+(staionHandler.getStationCoordinates(goingTo)).name*/);
		//console.log()
	};
}

var body_train_departures = 
'<REQUEST>' +
'<LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" />' +
'<QUERY objecttype="TrainAnnouncement" orderby="AdvertisedTimeAtLocation" limit="20">' +
'<FILTER>' +
'<AND>' +
'<EQ name="ActivityType" value="Avgang" />' +
//'<EQ name="LocationSignature" value="Cst" />' +
'<OR>' +
'<AND>' +
'<GT name="AdvertisedTimeAtLocation" value="$dateadd(-0.00:15:00)" />' +
'<LT name="AdvertisedTimeAtLocation" value="$dateadd(14:00:00)" />' +
'</AND>' +
'<AND>' +
'<LT name="AdvertisedTimeAtLocation" value="$dateadd(00:30:00)" />' +
'<GT name="EstimatedTimeAtLocation" value="$dateadd(-0.00:15:00)" />' +
'</AND>' +
'</OR>' +
'</AND>' +
'</FILTER>' +
'<INCLUDE>AdvertisedTrainIdent</INCLUDE>' +
'<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>' +
'<INCLUDE>TrackAtLocation</INCLUDE>' +
'<INCLUDE>ToLocation</INCLUDE>' +
'<INCLUDE>TimeAtLocation</INCLUDE>' +
//'<INCLUDE>FromLocation</INCLUDE>' +

'<INCLUDE>LocationSignature</INCLUDE>' +
'</QUERY>' +
'</REQUEST>';

caller.make_call(body_train_departures, handle_train_departures);





function handle_train_station(data){
	//console.log(data)
	station_list = JSON.parse(data).RESPONSE.RESULT[0].TrainStation
	console.log(station_list);
	//console.log(station_list.length);
	for (var i = 0; i <= station_list.length - 1; i++) {
		//console.log("------------" + i + "-----------")
		//console.log(station_list[i]);
		//console.log(station_list[i].Advertised)
	};
	/*trainlist.keys(obj).forEach(function (key) {
        i++;
        console.log;
        console.log(key);
        console.log(obj[key]);
    });*/
}

//var body_trafic = '<REQUEST><LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" /><QUERY objecttype="Situation" limit="5"><FILTER><WITHIN name="Deviation.Geometry.SWEREF99TM" shape="center" value="674585 6580201" radius="10000" /></FILTER><INCLUDE>Deviation.Header</INCLUDE><INCLUDE>Deviation.IconId</INCLUDE><INCLUDE>Deviation.Message</INCLUDE><INCLUDE>Deviation.MessageCode</INCLUDE><INCLUDE>Deviation.MessageType</INCLUDE></QUERY></REQUEST>';
var body_train_stations = 
'<REQUEST>' + 
'<LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" />' + 
'<QUERY objecttype="TrainStation">' + 
'<FILTER />' + 
'</QUERY>' + 
'</REQUEST>' 
//caller.make_call(body_train_stations, handle_train_station);


