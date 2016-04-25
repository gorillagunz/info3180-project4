var app = angular.module("Wishlist",[]);


app.controller('NewItemCtrl', function($scope, $http){
    $scope.img_url = "";
    $scope.images = [];
    $scope.params= ["Test", "*", "Test2"];

    $scope.get_thumbs = function(){
        if($scope.img_url == ""){
            alert("No url entered.");
        } else {
            var base = "http://info3180-project2-drellimal2-1.c9users.io:8080/";
            var route = "api/thumbnail/process?url=";
            var data_url = base + route + $scope.img_url;
            console.log(data_url);
            for(var x = 0; x < 4;x++){
                $http.get(data_url).success(function(data){
                    if (data.data != {}){
                        $scope.images = data.data.thumbails;
                    }
                });
            }
                
                
            console.log($scope.images);
        }
      
    };
    
    
    
});