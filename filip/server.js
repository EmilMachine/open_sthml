var express = require("express")
var app = express();


app.use(express.static(__dirname + "/public"))


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




