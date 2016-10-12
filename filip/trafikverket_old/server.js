var express = require("express")
var caller = require("./trafikverket_caller");
var trafiklab_caller = require("./trafiklab_caller");
//var trafikverket = require("./trafikverket_main");
var staionHandler = require("./train_stations");
var app = express();


app.use(express.static(__dirname + "/public"))
app.get("/trafik", function (req, res) {
    var body_train_departures = 
        '<REQUEST>' +
        '<LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" />' +
        '<QUERY objecttype="TrainAnnouncement" orderby="TimeAtLocation" >' +
        '<FILTER>' +
        '<AND>' +
        '<EQ name="ActivityType" value="Avgang" />' +
        '<NE name="TimeAtLocation" value=""/>' +
        //'<GT name="TimeAtLocation" value="2016-10-01T08:28:00" />'+
        //'<LT name="TimeAtLocation" value="2016-10-01T08:32:00" />'+
        '<GT name="TimeAtLocation" value="$dateadd(-0.00:03:00)" />'+
        //'<ST name="TimeAtLocation" value="$now" />'+
        '</AND>' +
        '</FILTER>' +
        '<INCLUDE>AdvertisedTrainIdent</INCLUDE>' +
        '<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>' +
        '<INCLUDE>TrackAtLocation</INCLUDE>' +
        '<INCLUDE>ToLocation</INCLUDE>' +
        '<INCLUDE>TimeAtLocation</INCLUDE>' +
        '<INCLUDE>LocationSignature</INCLUDE>' +
        '</QUERY>' +
        '</REQUEST>';

    var handleResponse = function(responseData){
        json_response = JSON.parse(responseData).RESPONSE.RESULT[0];
        //console.log(responseData);


        if(json_response.hasOwnProperty('ERROR')){ //check if an ERRROR was returned by trafikverket
            console.log(json_response.ERROR)
                res.json({
                success: false,
                message: "somthing went wrong :/",
                data: json_response.ERROR
            });
        }else{
            departures_trafikverket = json_response.TrainAnnouncement;
            departures = staionHandler.addStationsToDepartures(departures_trafikverket);
            console.log(departures)
            console.log("successfully got departures");
            res.json({
                success: true,
                message: "successfully got departures",
                data: departures
            });
        }
    }   
    caller.make_call(body_train_departures,handleResponse)
});

app.get("/trafiklab", function (req, res) {
    var query = query = {
        "siteId":9192,
        "timeWindow":5
    }
        
    var handleResponse = function(responseData){
        console.log("inside trafiklab handle response");
        console.log(responseData);
        res.json({
            success: true,
            message: "somthing went wrong :/",
            data: responseData
        });
        /*
        if(json_response.hasOwnProperty('ERROR')){ //check if an ERRROR was returned by trafikverket
            console.log(json_response.ERROR)
                res.json({
                success: false,
                message: "somthing went wrong :/",
                data: json_response.ERROR
            });
        }else{
            departures_trafikverket = json_response.TrainAnnouncement;
            departures = staionHandler.addStationsToDepartures(departures_trafikverket);
            console.log(departures)
            console.log("successfully got departures");
            res.json({
                success: true,
                message: "successfully got departures",
                data: departures
            });
        }
        */
    }   
    trafiklab_caller.getTraficlab(query,handleResponse)
});







app.listen(3000);

console.log("Running as port 3000")




