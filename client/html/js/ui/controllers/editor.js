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
.controller('EditorEditorCtrl', function($state, $scope, Spiff, SpiffRestangular, $stateParams) {
  $scope.type = $stateParams.type;
  Spiff.getSchema($stateParams.type).then(function(schema) {
    $scope.schema = schema;
    console.log($scope.schema);
    if ('id' in $stateParams) {
      $scope.id = $stateParams.id;
      SpiffRestangular.one($stateParams.type, $stateParams.id).get().then(function(object) {
        $scope.object = object;
      });
    } else {
      $scope.object = {};
    }
  });

  $scope.submit = function() {
    if ('id' in $stateParams) {
      $scope.object.save();
    } else {
      SpiffRestangular.all($scope.type).post($scope.object).then(function(result) {
        console.log(result);
        $state.go('editor.edit', {type: $scope.type, id: result.id});
      });
    }
  };
});
