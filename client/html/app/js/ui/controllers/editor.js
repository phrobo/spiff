angular.module('spiff.editor', [
    'spiff',
    'restangular'
])

.controller('EditorDashboardCtrl', function($scope, Spiff, SpaceAPI) {
  SpaceAPI.ready(function(api) {
    $scope.spaceAPI = api.data;
  });
  Spiff.getSchemas().then(function(s) {
    $scope.schemas = s;
  });
})
.controller('EditorListCtrl', function($scope, SpiffRestangular, $stateParams) {
  $scope.type = $stateParams.type;
  SpiffRestangular.all($stateParams.type).getList().then(function (objs) {
    $scope.objects = objs;
  });
})
.controller('EditorEditorCtrl', function($scope, Spiff, SpiffRestangular, $stateParams) {
  $scope.type = $stateParams.type;
  $scope.id = $stateParams.id;
  SpiffRestangular.one($stateParams.type, $stateParams.id).get().then(function(object) {
    $scope.object = object;
    Spiff.getSchema($stateParams.type).then(function(schema) {
      $scope.schema = schema;
    });

  });

  $scope.submit = function() {
    console.log($scope.object);
    $scope.object.save();
  };
});
