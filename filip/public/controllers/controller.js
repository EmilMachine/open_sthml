var myApp = angular.module('myApp', ['ngRoute']);
myApp.controller('AppCtrl', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from controller");

// Detta är ett get request till urlen /contacts och serverns kommer 
// skicka tillbaka ett response
/*$http.get('/contacts').success(function(response){
	console.log("i got the data");
	$scope.contacts = response;
});*/


$scope.initiateApp = function(){
    console.log('inne i initation')
    
};

}]).config(function($routeProvider){
    $routeProvider.when('/',
        {
            templateUrl: 'views/hem.client.html'
        })
            
    });