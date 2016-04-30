var app = angular.module("Wishlist",['ui.bootstrap']);


app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  });

app.controller('NavCtrl', function($scope){
  
  $scope.logout = function(){
    localStorage.removeItem('user');
    window.location.href = '/login'
  }
  
});
app.controller('NewItemCtrl', function($scope, $http, $uibModal){
    $scope.item_url = "";
    $scope.img_url = "";
    $scope.selectedimg = "";

    $scope.prod_url = "";
    $scope.images = [];
    $scope.params= ["Test", "*", "Test2"];

    $scope.get_thumbs = function(){
        if($scope.prod_url == ""){
            alert("No url entered.");
        } else {
            var base = "http://info3180-project2-drellimal2-1.c9users.io:8080/";
            var route = "/api/thumbnail/process?url=";
            var data_url = route + $scope.prod_url;
            
            for(var x = 0; x < 4;x++){
                $http.get(data_url).success(function(data){
                    console.log(data);
                    if (data.data != {}){
                        $scope.images = data.data.thumbails;
                    }
                });
            }

            console.log($scope.images);
        }
      
    };
    
    $scope.search= function(){
          // $scope.get_thumbs();
          $scope.open();
   
    }
    $scope.open = function (size) {

    $scope.animationsEnabled = true;
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'ThumbnailCtrl',
      resolve: {
          prod_url: function () {
          return $scope.prod_url;
        }

        }
      
    });
    
    modalInstance.result.then(function (img) {
      $scope.img_url = img;
      $scope.selectedimg = img;
    }, function () { 
      
    });
    
    }
});

app.controller('ThumbnailCtrl', function ($scope, $http, $uibModalInstance, prod_url) {

  $scope.images = [];
  $scope.prod_url = prod_url;

    $scope.get_thumbs = function(){
        if($scope.prod_url == ""){
            alert("No url entered.");
        } else {
            var base = "http://info3180-project2-drellimal2-1.c9users.io:8080/";
            var route = "/api/thumbnail/process?url=";
            var data_url = route + $scope.prod_url;
            console.log(data_url);
            console.log(data_url);
            for(var x = 0; x < 1;x++){
                $http.get(data_url).success(function(data){
                    console.log(data);
                    if (data.data != {}){
                        $scope.images = data.data.thumbails;
                    }
                });
            }

            console.log($scope.images);
        }
      
    };
    
  $scope.get_thumbs();
  $scope.selected = "";

  $scope.selectimg = function(imgurl){
    $scope.selected = imgurl;
    console.log(imgurl);
    console.log($scope.selected);
  }
  $scope.ok = function () {
    if($scope.selected == ""){
      alert("Please choose an image");
    }else{
  
      $uibModalInstance.close($scope.selected);
    }
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});

app.controller('WishlistsCtrl', function($scope, $http, $uibModal){
    $scope.wishlists = []
    var userid = localStorage.getItem('user')
    var data_url= '/api/user/' + userid + '/wishlists'
    var get_wishlists = function(){
    $http.get(data_url).success(function(data){
      
      $scope.wishlists = data.data;
      console.log($scope.wishlists);
    });
    }
    
    get_wishlists();
    
    $scope.open = function (size) {

    $scope.animationsEnabled = true;
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'NewWishlistCtrl',
      resolve: {
        
        }
      
    });
    
    modalInstance.result.then(function (new_wishlist) {
      
      $scope.wishlists.push(new_wishlist);
      get_wishlists();      
    }, function () { 
      
    });
    
    }
});

app.controller('NewWishlistCtrl', function ($scope, $http, $uibModalInstance) {

  $scope.title = "";
  $scope.desc = "";
  $scope.private = "";
  $scope.userid = localStorage.getItem('user');
  $scope.created_on = Date.now();
  $scope.new_wishlist = {};
  $scope.ok = function () {
    var base = "http://info3180-project2-drellimal2-1.c9users.io:8080/";
    var route = "/api/wishlist/new?";
    var data_url = route + 'title=' + $scope.title + '&desc=' + $scope.desc;
    if($scope.private==true){
      $scope.private =1;
    }else{
      $scope.private=0;
    }
    data_url += '&private=' + $scope.private + '&userid=' + $scope.userid + '&created_on=' + $scope.created_on;
    $http.get(data_url).success(function(data){
        console.log(data);
        if (data.data != {}){
            $scope.new_wishlist = data.data;
        }
    });  
    console.log(data_url);
    $uibModalInstance.close($scope.new_wishlist);
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});
app.controller('LoginCtrl', function($scope){
  var uid = localStorage.getItem('user') ;
  if(uid !== null){
    var path ='/user/'+uid+'/wishlists';
    window.history.pushState({'user' : uid}, 'user', path );
    window.location.href = path;
  }
});

app.controller('WishlistCtrl', function($scope, $http, $uibModal){
    $scope.items = [
            ];
    
    var url = window.location.pathname;
    var wishlist_id = url.split('/').pop();
    var userid = localStorage.getItem('user')
    var data_url= '/api/user/'+ userid + '/wishlist/' + wishlist_id + '/items'
    console.log(data_url);
    var get_wishlist_items = function(){
    $http.get(data_url).success(function(data){
      
      $scope.items = data.data;
      console.log($scope.items);
    });
    }
    
    get_wishlist_items();
    
    
    
    
});