angular.module("payday").filter("select", function($parse) {
    var lastInput = undefined;
    var lastOutput = undefined;
    //We need to memoize the previous output of the select filter
    //otherwise angular will get into a digest loop
    var memoize = function(func) {
        return function memoized(input, _, __) {
            var same = true;
            if(lastInput && lastOutput && lastInput.length === input.length) {
                for(var i = 0; i < input.length; i++) {
                    if(input[i] != lastInput[i]) {
                        same = false;
                        break;
                    }
                }
            } else {
                same = false;
            }
            if(!same) {
                lastOutput = func(input, _, __);
                lastInput = input;
            }
            return lastOutput;
        };
    };

    return memoize(function select(input, itemName, expression) {
        if(!expression) {
            return input;
        }

        var items = [];
        for(i = 0; i < input.length; i++) {
            var context = {};
            context[itemName] = input[i];
            var item = $parse(expression)(context);
            items.push(item);
        }
        lastInput = input;
        lastOutput = items;
        return items;
    });
});
