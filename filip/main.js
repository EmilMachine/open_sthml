
var caller = require("./api_caller");

function handle_data(data){
	console.log("yay" + data)
}


// get 
var body = '<REQUEST><LOGIN authenticationkey="5b1a60214fdd45b5bfc5166d2c95d30d" /><QUERY objecttype="Situation" limit="5"><FILTER><WITHIN name="Deviation.Geometry.SWEREF99TM" shape="center" value="674585 6580201" radius="10000" /></FILTER><INCLUDE>Deviation.Header</INCLUDE><INCLUDE>Deviation.IconId</INCLUDE><INCLUDE>Deviation.Message</INCLUDE><INCLUDE>Deviation.MessageCode</INCLUDE><INCLUDE>Deviation.MessageType</INCLUDE></QUERY></REQUEST>';

caller.make_call(body, handle_data);