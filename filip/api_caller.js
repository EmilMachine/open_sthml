//http://stackoverflow.com/questions/14018269/how-to-post-xml-data-in-node-js-http-request

var http = require('http');
var request = require('request')
//var body = '<REQUEST><LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" /><QUERY objecttype="Situation" limit="5"><FILTER><WITHIN name="Deviation.Geometry.SWEREF99TM" shape="center" value="674585 6580201" radius="10000" /></FILTER><INCLUDE>Deviation.Header</INCLUDE><INCLUDE>Deviation.IconId</INCLUDE><INCLUDE>Deviation.Message</INCLUDE><INCLUDE>Deviation.MessageCode</INCLUDE><INCLUDE>Deviation.MessageType</INCLUDE></QUERY></REQUEST>';

function make_call(query, callback){
	var postRequest = {
	    host: "api.trafikinfo.trafikverket.se",
	    path: "/v1/data.json",
	    port: 80,
	    method: "POST",
	    headers: {
	        'Content-Type': 'text/xml',
	        'Content-Length': Buffer.byteLength(query)
	    }
	};

	var buffer = "";
	var req = http.request(postRequest, function( res )    {

		console.log( res.statusCode );
		var buffer = "";
		res.on( "data", function( data ) { buffer = buffer + data; } );
		res.on( "end", 
			function( data ) { 
			   	callback(buffer); //return response values
			} 
		);

	});

	req.on('error', function(e) {
	    console.log('problem with request: ' + e.message);
	});

	req.write( query );
	req.end();

}


module.exports = {
  make_call: make_call
};




// ------ old working
/*

var postRequest = {
    host: "api.trafikinfo.trafikverket.se",
    path: "/v1/data.json",
    port: 80,
    method: "POST",
    headers: {
        'Content-Type': 'text/xml',
        'Content-Length': Buffer.byteLength(body)
    }
};

var buffer = "";
var req = http.request(postRequest, function( res )    {

   console.log( res.statusCode );
   var buffer = "";
   res.on( "data", function( data ) { buffer = buffer + data; } );
   res.on( "end", function( data ) { console.log( buffer ); } );

});

req.on('error', function(e) {
    console.log('problem with request: ' + e.message);
});

req.write( body );
req.end();


function test(){
	console.log("hej")
}
module.exports = {
  test: test
};

*/