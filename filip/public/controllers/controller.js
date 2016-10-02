var myApp = angular.module('myApp', ['ngRoute']);
myApp.controller('AppCtrl', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from controller");

// Detta är ett get request till urlen /contacts och serverns kommer 
// skicka tillbaka ett response
/*$http.get('/contacts').success(function(response){
	console.log("i got the data");
	$scope.contacts = response;
});*/

$scope.getTrafik = function(){
	console.log('getTrafik is running');
	//window.alert("yay")
	$http.get('/trafik').success(function(response){
		//error handling
		if (response.success){
			$scope.departures = response.data;
			console.log(response.message);

		}else{
			console.log(response.message);
			alert(response.message +"\n" + "Source: " + response.data.SOURCE + "\nMessage: " + response.data.MESSAGE);
		}

		console.log("det gick bra? " + response.success)
	
	});
};

$scope.initiateApp = function(){
    console.log('inne i initation')
    
};








}]).config(function($routeProvider){
    $routeProvider.when('/',
        {
            templateUrl: 'views/hem.client.html'
        })
            
    });