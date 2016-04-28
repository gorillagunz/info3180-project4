var app = angular.module("Wishlist",['ui.bootstrap']);


app.controller('NewItemCtrl', function($scope, $http){
    $scope.item_url = "";
    $scope.img_url = "";
    $scope.images = [];
    $scope.params= ["Test", "*", "Test2"];

    $scope.get_thumbs = function(){
        if($scope.img_url == ""){
            alert("No url entered.");
        } else {
            var base = "http://info3180-project2-drellimal2-1.c9users.io:8080/";
            var route = "api/thumbnail/process?url=";
            var data_url = base + route + $scope.item_url;
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
    
    $scope.search= function(){
        
    }
});

app.controller('WishlistsCtrl', function($scope, $http, $uibModal){
    $scope.open = function (size) {

    $scope.animationsEnabled = true;
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'NewWishlistCtrl',
      resolve: {
        
        }
      
    });
    
    }
});

app.controller('NewWishlistCtrl', function ($scope, $http, $uibModalInstance) {

  

  $scope.ok = function () {
      
    $uibModalInstance.close();
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});