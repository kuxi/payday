angular.module("payday").controller("TimeCtrl", [
    "$scope",
    "$modal",
    "PaydayResource",
    "ImportantDates",
    function TimeCtrl($scope, $modal, PaydayResource, ImportantDates) {
        $scope.allWorkHours = [];
        $scope.gettingAllDates = false;
        $scope.currentLogs = [];
        $scope.currentDate = new Date();
        $scope.submitText = "Save";
        $scope.currentLog = {
            "id": undefined,
            "hours": "",
            "description": ""
        };
        $scope.showForm = false;

        var updateCurrentLogs = function updateCurrentLogs(workHours) {
            $scope.currentLogs = [];
            for(var i = 0; i < workHours.length; i++) {
                if(datesMatch(workHours[i].date, $scope.currentDate)) {
                    var log = {
                        "id": workHours[i].id,
                        "hours": workHours[i].hours,
                        "description": workHours[i].description,
                        "hidden": false
                    };
                    $scope.currentLogs.push(log);
                }
            }
        };

        var updateImportantDates = function updateImportantDates() {
            $scope.loadingAllDates = true;
            ImportantDates().then(function(allWorkHours) {
                $scope.allWorkHours = allWorkHours;
                updateCurrentLogs(allWorkHours);
            }).finally(function() {
                $scope.loadingAllDates = false;
            });
        };

        var datesMatch = function datesMatch(a, b) {
            if(a.getFullYear() === b.getFullYear()) {
                if(a.getMonth() + 1 === b.getMonth() + 1) {
                    return a.getDate() === b.getDate();
                }
            }
            return false;
        };

        //**** Form stuff ****//

        $scope.openForm = function logHours() {
            $scope.showForm = true;
        };

        $scope.closeForm = function closeForm() {
            $scope.resetForm();
            $scope.showForm = false;
        };

        $scope.cancel = function cancel() {
            for(var i = 0; i < $scope.currentLogs.length; i++) {
                if($scope.currentLogs[i].id === $scope.currentLog.id) {
                    $scope.currentLogs[i].hidden = false;
                    break;
                }
            }
            $scope.closeForm();
        };

        $scope.resetForm = function resetForm() {
            $scope.currentLog = {
                "id": undefined,
                "hours": "",
                "description": ""
            };
        };

        $scope.submitForm = function submitForm(form) {
            if(form.$valid) {
                var date = $scope.currentDate;
                var year = date.getFullYear();
                var month = date.getMonth() + 1;
                var day = date.getDate();
                var data = {
                    "id": $scope.currentLog.id,
                    "hours": $scope.currentLog.hours,
                    "description": $scope.currentLog.description
                };
                PaydayResource.hours(year, month, day).save(data, function(data) {
                    console.log(data);
                    updateImportantDates();
                });
                $scope.resetForm();
                $scope.hoursForm.$setPristine();
                $scope.closeForm()
            }
        };

        $scope.editLog = function editLog(workDate) {
            $scope.cancel();
            workDate.hidden = true;
            $scope.currentLog = angular.copy(workDate);
            $scope.openForm();
        };

        $scope.confirmDelete = function confirmDelete(id) {
            console.log('yo');
            modalResponse = $modal.open({
                templateUrl: "/static/partials/confirm.html",
                controller: "ConfirmCtrl",
                resolve: {
                    "message": function() {
                        return "Are you sure you want to delete this log?";
                    }
                }
            });

            modalResponse.result.then(function () {
                deleteLog(id);
            });
        };

        var deleteLog = function deleteLog(id) {
            var date = $scope.currentDate;
            var year = date.getFullYear();
            var month = date.getMonth() + 1;
            var day = date.getDate();
            var data = {
                "id": id
            };
            PaydayResource.hours(year, month, day).delete(data, function(data) {
                console.log(data);
                updateImportantDates();
            });
        };

        //**** Initialization ****//

        $scope.$watch("currentDate", function(date) {
            updateCurrentLogs($scope.allWorkHours);
        });
        

        updateImportantDates();
    }
]);
angular.module("payday").controller("ConfirmCtrl", [
    "$scope",
    "$modalInstance",
    "message",
    function TimeCtrl($scope, $modalInstance, message) {
        $scope.message = message;

        $scope.ok = function ok() {
            $modalInstance.close();
        };

        $scope.cancel = function() {
            $modalInstance.dismiss();
        };
    }
]);
