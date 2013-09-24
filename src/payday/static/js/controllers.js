angular.module("payday").controller("TimeCtrl", [
    "$scope", 
    "PaydayResource",
    function TimeCtrl($scope, PaydayResource) {
        $scope.WorkDate = {
            "date": Date(),
            "hours": 9,
        };
        $scope.submitText = "Save";
        $scope.$watch("WorkDate.date", function(newVal) {
            console.log(newVal);
        });
        
        $scope.submitForm = function submitForm() {
            var date = $scope.WorkDate.date;
            var year = date.getFullYear();
            var month = date.getMonth() + 1;
            var day = date.getDate();
            var data = {
                hours: $scope.WorkDate.hours
            };
            PaydayResource.hours(year, month, day).post(data, function(data) {
                console.log(data);
            });
        }
    }
]);
