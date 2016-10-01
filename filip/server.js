var express = require("express")
var caller = require("./trafikverket_caller");
var trafikverket = require("./trafikverket_main");
var staionHandler = require("./train_stations");
var app = express();


app.use(express.static(__dirname + "/public"))

app.get("/trafik", function (req, res) {

    var body_train_departures = 
        '<REQUEST>' +
        '<LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" />' +
        '<QUERY objecttype="TrainAnnouncement" orderby="AdvertisedTimeAtLocation" limit="30">' +
        '<FILTER>' +
        '<AND>' +
        '<EQ name="ActivityType" value="Avgang" />' +
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

    var handle_train_departures = function handle_train_departures(data){
        console.log(data)
        trains = []
        train = {
            "trainNbr":"",
            "station":"",
            "departureTime":"",
            "advertisedTime":"",
            "nextStations":{}
        }
        departures_trafikverket = JSON.parse(data).RESPONSE.RESULT[0].TrainAnnouncement
        if (departures_trafikverket != undefined){
            for (var i = 0; i < departures_trafikverket.length; i++) {
                departure = departures_trafikverket[i];
                
                stationSign = departure.LocationSignature;
                goingTo = departure.ToLocation.LocationName;
                station = staionHandler.getStation(stationSign);
                temp_train = train;
                temp_train.trainNbr = departure.AdvertisedTrainIdent;
                temp_train.station = station;
                temp_train.departureTime = departure.TimeAtLocation;
                temp_train.advertisedTime = departure.AdvertisedTimeAtLocation;
                next_stations = []
                for (j=0; j< departure.ToLocation.length;j++){
                    next_stations.push(staionHandler.getStation(departure.ToLocation[j]));
                }
                temp_train.nextStations = next_stations;
                trains.push(temp_train)
            };
        };
        console.log(trains);
        res.json({
            success: true,
            message: "successfully got trains",
            data: trains
        });

    }

    caller.make_call(body_train_departures,handle_train_departures)

});




/*
app.get("/authorize", function (req, res) {
    //console.log(res)
    res.redirect(client.getAuthorizeUrl('activity heartrate location nutrition profile settings sleep social weight'
        , CALLBACK_URL));

});

app.get("/callback", function (req, res) {
    //console.log(req)
    console.log("req.query.code: " + req.query.code);
    client.getAccessToken(req.query.code, CALLBACK_URL).then(function (result) {
        access_token = result.access_token
        console.log("access token: " + result.access_token);
        res.redirect("/");
    }).catch(function (error) {
        res.send(error);
    });
});


app.get("/get_profile", function (req, res) {
    client.get("/profile.json", access_token).then(function (results) {
        console.log(results[0]);
        //res.send(results[0]);
    });
});

app.get("/get_steps", function (req, res) {
    client.get("/activities/steps/date/[today]/[1m].json", access_token).then(function (results) {
        console.log(results[0]);
        res.send(results[0]);
    });
});

*/
app.listen(3000);

console.log("Running as port 3000")




