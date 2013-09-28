angular.module("payday").controller("TimeCtrl", [
    "$scope", 
    "PaydayResource",
    "ImportantDates",
    function TimeCtrl($scope, PaydayResource, ImportantDates) {
        $scope.allWorkHours = [];
        $scope.gettingAllDates = false;
        $scope.WorkDate = {
            "date": new Date(),
            "hours": 0,
            "description": ""
        };
        $scope.submitText = "Save";

        var updateSelectedDate = function updateSelectedDate(workHours) {
            $scope.submitText = "Save";
            $scope.WorkDate.hours = 0;
            $scope.WorkDate.description = "";
            for(var i = 0; i < workHours.length; i++) {
                if($scope.datesMatch(workHours[i].date, $scope.WorkDate.date)) {
                    $scope.submitText = "Update";
                    $scope.WorkDate.hours = workHours[i].hours;
                    $scope.WorkDate.description = workHours[i].description;
                }
            }
        };

        $scope.updateImportantDates = function updateImportantDates() {
            $scope.loadingAllDates = true;
            ImportantDates.then(function(allWorkHours) {
                $scope.allWorkHours = allWorkHours;
                updateSelectedDate(allWorkHours);
            }).always(function() {
                $scope.loadingAllDates = false;
            });
        };
        $scope.datesMatch = function datesMatch(a, b) {
            if(a.getFullYear() === b.getFullYear()) {
                if(a.getMonth() + 1 === b.getMonth() + 1) {
                    return a.getDate() === b.getDate();
                }
            }
            return false;
        };
        $scope.$watch("WorkDate.date", function(date) {
            updateSelectedDate($scope.allWorkHours);
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
