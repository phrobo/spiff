var Spiff = angular.module('spiff', [
  'restangular',
  'spaceapi'
]);

Spiff.directive('checkPermission', function(Spiff, $rootScope) {
  return {
    link: function(scope, element, attrs) {
      Spiff.$watch('currentUser', function(user) {
        if (attrs.checkPermission != undefined) {
          Spiff.checkPermission(scope.$eval(attrs.checkPermission)).then(function (result) {
            scope.hasPermission = result;
          });
        } else {
          scope.hasPermission = false;
        }
      });
    },
  };
});

Spiff.directive('requireApp', function(Spiff, $rootScope) {
  return {
    link: function(scope, element, attrs) {
      Spiff.$watch('apps', function(apps) {
        if (attrs.requireApp != undefined) {
          var found = false;
          apps.forEach(function(app) {
            if (app.id == scope.$eval(attrs.requireApp))
              found = true;
          });
          scope.hasApp = found;
        } else {
          scope.hasApp = false;
        }
      });
    }
  };
});

Spiff.factory('SpiffRestangular', function(SpiffConfig, Restangular) {
  return Restangular.withConfig(function(RestangularConfigurer) {
    RestangularConfigurer.setBaseUrl(SpiffConfig.baseUrl);
    RestangularConfigurer.setParentless(false);
    RestangularConfigurer.setRequestSuffix('/');

    RestangularConfigurer.addFullRequestInterceptor(function(element, operation, route, url, headers, params, httpConfig) {
      var currentHeaders = headers;
      if (SpiffConfig.getAuthToken()) {
        currentHeaders.Authorization = 'Bearer '+SpiffConfig.getAuthToken();
      }
      return {
        element: element,
        params: params,
        headers: currentHeaders 
      };
    });

    RestangularConfigurer.setErrorInterceptor(function(response) {
      var $injector = angular.element('body').injector();
      if (response.status == 401) {
        $injector.get('$rootScope').$broadcast('loginRequired', response);
      } else {
        console.log(response);
        $injector.get('$rootScope').$broadcast('error', response);
      }
      return true;
    });

    RestangularConfigurer.addElementTransformer('member', true, function(member) {
      if (member.addRestangularMethod) {
        member.addRestangularMethod('login', 'post', 'login');
        member.addRestangularMethod('search', 'get', 'search');
        member.addRestangularMethod('requestPasswordReset', 'post', 'requestPasswordReset');
      }
      return member;
    });

    RestangularConfigurer.addElementTransformer('member', false, function(member) {
      if (member.addRestangularMethod) {
        member.addRestangularMethod('getStripeCards', 'get', 'stripeCards');
        member.addRestangularMethod('addStripeCard', 'post', 'stripeCards');
        member.addRestangularMethod('removeStripeCard', 'remove', 'stripeCards');
      }
      return member;
    });

    RestangularConfigurer.setResponseExtractor(function(response, operation, what, url) {
      var newResponse;
      if (operation == 'getList') {
        newResponse = response.objects;
        newResponse.meta = response.meta;
        newResponse.meta.pages = [];
        for(var i = 0;i<newResponse.meta.total_count/newResponse.meta.limit;i++) {
          newResponse.meta.pages.push(i);
        }
      } else {
        newResponse = response;
      }
      return newResponse;
    });

  });
});

Spiff.provider('SpiffConfig', function() {
  var baseUrl = null;
  this.setBaseUrl = function(url) {
    baseUrl = url;
  }

  var authToken = null;
  var setAuthToken = function(token) {
    authToken = token;
  }

  this.$get = function() {
    return {
      baseUrl: baseUrl,
      getAuthToken: function() {return authToken;},
      setAuthToken: setAuthToken
    }
  };
});

Spiff.provider('Spiff', function() {

  this.$get = function(SpaceAPI, SpiffRestangular, SpiffConfig, $q, $rootScope, $http) {
    var scope = $rootScope.$new();

    scope.getSchemas = function() {
      var ret = $q.defer();
      var authHeader = 'Bearer '+SpiffConfig.getAuthToken();

      $http.get(SpiffConfig.baseUrl+'/', {'headers': {'Authorization': authHeader}}).success(function(schema) {
        ret.resolve(schema);
      });
      //FIXME: handle error

      return ret.promise;
    };

    scope.federations = [];
    SpiffRestangular.all('federation').getList().then(function(federations) {
      scope.federations = federations;
    });

    scope.apps = [];
    SpiffRestangular.all('app').getList().then(function(apps) {
      scope.apps = apps;
    });

    scope.getSchema = function(type) {
      var ret = $q.defer();
      var authHeader = 'Bearer '+SpiffConfig.getAuthToken();

      $http.get(SpiffConfig.baseUrl+'/'+type+'/schema/', {'headers': {'Authorization': authHeader}}).success(function(schema) {
        ret.resolve(schema);
      });
      //FIXME: handle error

      return ret.promise;
    };

    scope.refreshUser = function() {
      return SpiffRestangular.one('member', 'self').get().then(function(user) {
        scope.currentUser = user;
      });
    };

    scope.getCurrentUser = function() {
      var ret = $q.defer();
      if (scope.currentUser) {
        ret.resolve(scope.currentUser);
      } else {
        scope.login().then(function() {
          ret.resolve(scope.currentUser);
        });
      }
      return ret.promise;
    };

    scope.login = function(username, password) {
      if (password === undefined) {
        return scope.refreshUser();
      } else {
        return SpiffRestangular.all('member').login({
          username: username,
          password: password
        }).then(function(data) {
          scope.$broadcast('loginSuccess', data.token);
          if (data.passwordReset) {
            scope.$broadcast('passwordResetRequested');
          }
          SpiffConfig.setAuthToken(data.token);
          scope.refreshUser();
          return data;
        }, function(reason) {
          scope.$broadcast('loginFailed');
          return reason;
        });
      }
    };

    scope.logout = function() {
      SpiffConfig.setAuthToken(null);
      scope.refreshUser();
      scope.$broadcast('loggedOut');
    };
    scope.currentUser = null;

    scope.checkPermission = function(perm) {
      var member = SpiffRestangular.one('member', 'self');
      var ret = $q.defer();
      var authHeader = 'Bearer '+SpiffConfig.getAuthToken();
      $http.get(member.getRestangularUrl()+'/has_permission/'+perm+'/', {'headers': {'Authorization': authHeader}}).success(function() {
        ret.resolve(true);
      }).error(function() {
        ret.resolve(false);
      });
      return ret.promise;
    }

    return scope;
  }
});
