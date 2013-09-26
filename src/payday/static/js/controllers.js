angular.module("payday").controller("TimeCtrl", [
    "$scope", 
    "PaydayResource",
    function TimeCtrl($scope, PaydayResource) {
        $scope.allWorkHours = [];
        $scope.updateImportantDates = function updateImportantDates() {
            PaydayResource.allHours().get().$then(function(response) {
                $scope.allWorkHours = [];
                var dates = [];
                for(var i = 0; i < response.data.length; i++) {
                    var date = response.data[i].date;
                    var dateObj = new Date(date.year, date.month - 1, date.day);
                    dates.push(dateObj);
                    if($scope.datesMatch(dateObj, $scope.WorkDate.date)) {
                        $scope.submitText = "Update";
                        $scope.WorkDate.hours = response.data[i].hours;
                        $scope.WorkDate.description = response.data[i].description;
                        console.log($scope.WorkDate);
                    }
                    $scope.allWorkHours.push(response.data[i]);
                }
                $scope.allDates = dates;
            });
        };
        $scope.datesMatch = function datesMatch(a, b) {
            if((a.year || a.getFullYear()) === (b.year || b.getFullYear())) {
                if((a.month || (a.getMonth() + 1)) === (b.month || (b.getMonth() + 1))) {
                    return (a.day || a.getDate()) === (b.day || b.getDate());
                }
            }
            return false;
        };
        $scope.allDates = [];
        $scope.WorkDate = {
            "date": new Date(),
            "hours": 0,
            "description": ""
        };
        $scope.submitText = "Save";
        $scope.$watch("WorkDate.date", function(date) {
            $scope.submitText = "Save";
            $scope.WorkDate.hours = 0;
            $scope.WorkDate.description = "";
            for(var i = 0; i < $scope.allWorkHours.length; i++) {
                if($scope.datesMatch($scope.allWorkHours[i].date, $scope.WorkDate.date)) {
                    $scope.submitText = "Update";
                    $scope.WorkDate.hours = $scope.allWorkHours[i].hours;
                    $scope.WorkDate.description = $scope.allWorkHours[i].description;
                    break;
                }
            }
        });
        
        $scope.submitForm = function submitForm() {
            var date = $scope.WorkDate.date;
            var year = date.getFullYear();
            var month = date.getMonth() + 1;
            var day = date.getDate();
            var data = {
                hours: $scope.WorkDate.hours,
                description: $scope.WorkDate.description
            };
            PaydayResource.hours(year, month, day).save(data, function(data) {
                console.log(data);
            });
            $scope.updateImportantDates();
        };

        $scope.updateImportantDates();
    }
]);
