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
        '<QUERY objecttype="TrainAnnouncement" orderby="AdvertisedTimeAtLocation" limit="20">' +
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
        //console.log(data)
        stations = []
        departures = JSON.parse(data).RESPONSE.RESULT[0].TrainAnnouncement
        for (var i = 0; i < departures.length; i++) {
            departure = departures[i];
            //console.log(departure);
            stationSign = departure.LocationSignature;
            goingTo = departure.ToLocation.LocationName;
            station = staionHandler.getStation(stationSign);
            //console.log(station);
            /*console.log("Train " + departure.AdvertisedTrainIdent + " departured from " + station.name + " (" + station.lon +","+ station.lat + ")");
            console.log("at " + departure.TimeAtLocation + ",but should have departured at " + departure.AdvertisedTimeAtLocation);
            console.log("after this it will go to:");
            for (j=0; j< departure.ToLocation.length;j++){
                console.log(staionHandler.getStation(departure.ToLocation[j]).name + "("+staionHandler.getStation(departure.ToLocation[j]).lon + "," + staionHandler.getStation(departure.ToLocation[j]).lat + ")");
            }
            console.log("--------------------------------------------")
            */
            stations.push(station)
        };
        res.send(stations);
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




