var payday = angular.module("payday", [
    "ui.bootstrap.datetimepicker",
    "ngResource",
    "ngRoute"
]);

payday.config([
    "$routeProvider",
    function($routeProvider) {
        $routeProvider.
            when("/", {
                templateUrl: "/static/partials/calendar.html",
                controller: "TimeCtrl"
            });
    }
]);
