angular.module("payday").service("PaydayResource", [
    "$location",
    "$resource",
    function ($location, $resource) {
        var self = this;
        this.port = "8000";
        this.host = $location.host();
        this.endpoint = "http://" + this.host + "\\:" + this.port + "/api/";

        return {
            allHours: function() {
                return $resource(self.endpoint + "hours/",
                    {},
                    {
                        get: {method: "GET", isArray: true}
                    }
                );
            },
            hours: function(year, month, day) {
                console.log(self.endpoint + "hours/:year/:month/:day/");
                return $resource(self.endpoint + "hours/:year/:month/:day/",
                    {year: year, month: month, day: day}
                );
            }
        };
    }
]);

angular.module("payday").factory("ImportantDates", function($q, PaydayResource) {
    var deferred = $q.defer();
    PaydayResource.allHours().get().$then(function success(response) {
        var dates = [];
        for(var i = 0; i < response.data.length; i++) {
            var item = response.data[i];
            var date = item.date;
            var dateObj = new Date(date.year, date.month - 1, date.day);
            item.date = dateObj;
            dates.push(item);
        }
        deferred.resolve(dates);
    }, function error(response) {
        deferred.reject("error retrieving important dates!");
    });
    return deferred.promise;
});
