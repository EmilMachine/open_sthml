
var caller = require("./api_caller");

function handle_train_data(data){
	trainlist = JSON.parse(data).RESPONSE.RESULT[0].TrainAnnouncement
	console.log(trainlist);
	trainlist.keys(obj).forEach(function (key) {
        i++;
        console.log;
        console.log(key);
        console.log(obj[key]);
    });
}

function handle_trafic_data(data){
	
	traficlist = JSON.parse(data).RESPONSE.RESULT[0].Situation
	console.log(typeof traficlist);
	console.log(traficlist)
	
		//console.log(list[0]);
		/*list.keys(obj).forEach(function (key) {
	        i++;
	        console.log;
	        console.log(key);
	        console.log(obj[key]);
	    });*/
	}
		
}

var body_trafic = '<REQUEST><LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" /><QUERY objecttype="Situation" limit="5"><FILTER><WITHIN name="Deviation.Geometry.SWEREF99TM" shape="center" value="674585 6580201" radius="10000" /></FILTER><INCLUDE>Deviation.Header</INCLUDE><INCLUDE>Deviation.IconId</INCLUDE><INCLUDE>Deviation.Message</INCLUDE><INCLUDE>Deviation.MessageCode</INCLUDE><INCLUDE>Deviation.MessageType</INCLUDE></QUERY></REQUEST>';

var body_train = '<REQUEST><LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" /><QUERY objecttype="TrainAnnouncement" orderby="AdvertisedTimeAtLocation"><FILTER><AND><EQ name="ActivityType" value="Avgang" /><EQ name="LocationSignature" value="Cst" /><OR><AND><GT name="AdvertisedTimeAtLocation" value="$dateadd(-0.00:15:00)" /><LT name="AdvertisedTimeAtLocation" value="$dateadd(14:00:00)" /></AND><AND><LT name="AdvertisedTimeAtLocation" value="$dateadd(00:30:00)" /><GT name="EstimatedTimeAtLocation" value="$dateadd(-0.00:15:00)" /></AND></OR></AND></FILTER><INCLUDE>AdvertisedTrainIdent</INCLUDE><INCLUDE>AdvertisedTimeAtLocation</INCLUDE><INCLUDE>TrackAtLocation</INCLUDE><INCLUDE>ToLocation</INCLUDE></QUERY></REQUEST>'



caller.make_call(body_trafic, handle_trafic_data);

