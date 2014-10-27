var spiffApp = angular.module('spiffApp', [
  'restangular',
  'spiffDirectives',
  'spaceapi',
  'spiff',
  'spiff.dashboard',
  'spiff.epicenter',
  'spiff.identity',
  'spiff.resources',
  'spiff.donate',
  'spiff.sensors',
  'spiff.payment',
  'spiff.editor',
  'ngRoute',
  'ui.gravatar',
  'md5',
  'ui.bootstrap.modal',
  'ui.router',
  'btford.markdown',
  'template/modal/window.html',
  'template/modal/backdrop.html'
]);

spiffApp.config(function($stateProvider, $urlRouterProvider, RestangularProvider, SpiffProvider) {
  $urlRouterProvider.otherwise('/');
  $stateProvider
    .state('dashboard', {
      url: '/',
      templateUrl: 'dashboard/index.html',
      controller: 'DashboardCtrl',
    })
    .state('welcome', {
      url: '/welcome',
      templateUrl: 'dashboard/index-anonymous.html',
      controller: 'AnonDashCtrl'
    })
    .state('viewInvoice', {
      url: '/invoices/:invoiceID',
      templateUrl: 'invoices/detail.html',
      controller: 'InvoiceCtrl'
    })
    .state('listResources', {
      url: '/resources',
      templateUrl: 'resources/index.html',
      controller: 'ResourceListCtrl'
    })
    .state('addResource', {
      url: '/resources/add',
      templateUrl: 'resources/add.html',
      controller: 'AddResourceCtrl',
    })
    .state('viewResource', {
      url: '/resources/:resourceID',
      templateUrl: 'resources/detail.html',
      controller: 'ResourceCtrl',
    })
    .state('listMembers', {
      url: '/members',
      templateUrl: 'members/index.html',
      controller: 'MemberListCtrl',
    })
    .state('member', {
      url: '/members/:memberID',
      templateUrl: 'members/detail.html',
      controller: 'MemberViewCtrl'
    })
    .state('member.view', {
      url: '',
      templateUrl: 'members/view.html',
      controller: 'MemberViewCtrl',
    })
    .state('member.subscriptions', {
      url: '/subscriptions',
      templateUrl: 'members/subscriptions.html',
      controller: 'SubscriptionCtrl',
    })
    .state('member.edit', {
      url: '/edit',
      templateUrl: 'members/edit.html',
      controller: 'EditMemberCtrl'
    })
    .state('member.payments', {
      url: '/payment',
      templateUrl: 'members/payment.html',
      controller: 'MemberPaymentCtrl'
    })
    .state('listSensors', {
      url: '/sensors',
      templateUrl: 'sensors/index.html',
      controller: 'SensorListCtrl',
    })
    .state('viewSensor', {
      url: '/sensors/:sensorID',
      templateUrl: 'sensors/detail.html',
      controller: 'SensorCtrl'
    })
    .state('donate', {
      url: '/donate',
      templateUrl: 'donate/index.html',
      controller: 'DonateCtrl',
    })
    .state('donate.plans', {
      url: '',
      templateUrl: 'donate/plans.html',
    })
    .state('donate.register', {
      url: '/register/:planID',
      templateUrl: 'donate/register.html',
      controller: 'DonationRegistrationCtrl'
    })
    .state('register', {
      url: '/register',
      templateUrl: 'register.html',
      controller: 'DashboardRegistrationCtrl'
    })
    .state('editor', {
      url: '/editor',
      templateUrl: 'editor/index.html',
      controller: 'EditorDashboardCtrl',
    })
    .state('editor.new', {
      url: '/new/:type',
      templateUrl: 'editor/edit.html',
      controller: 'EditorEditorCtrl',
    })
    .state('editor.list', {
      url: '/list/:type',
      templateUrl: 'editor/list.html',
      controller: 'EditorListCtrl',
    })
    .state('editor.edit', {
      url: '/edit/:type/:id',
      templateUrl: 'editor/edit.html',
      controller: 'EditorEditorCtrl',
    });
});

spiffApp.config(function(SpaceAPIProvider, SpiffConfigProvider) {
  SpiffConfigProvider.setBaseUrl(CONFIG['spiff']+'v1');
  SpaceAPIProvider.setBaseUrl(CONFIG['spaceAPI']);
});

spiffApp.run(function(Spiff, SpiffConfig, $window) {
  if ($window.sessionStorage.token) {
    SpiffConfig.setAuthToken($window.sessionStorage.token);
  }
  Spiff.login();
  Spiff.$on('loginSuccess', function(element, token) {
    $window.sessionStorage.token = token;
  });

  Spiff.$on('loggedOut', function() {
    delete $window.sessionStorage.token;
  });
});
