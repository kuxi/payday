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
                        get: {method: "GET", isArray: true},
                    }
                );
            },
            hours: function(year, month, day) {
                console.log(self.endpoint + "hours/:year/:month/:day/");
                return $resource(self.endpoint + "hours/:year/:month/:day/",
                    {year: year, month: month, day: day},
                    {
                        post: {method: "POST"}
                    }
                );
            }
        };
    }
]);
