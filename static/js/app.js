"use strict";

/**
 * get cookie by name
 *
 * @param {string} name - cookie name
 */
var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

//var csrftoken = getCookie('csrftoken');

var datepicker_defaults = {
        format: "dd/mm/yyyy",
        weekStart: 1,
        todayBtn: "linked",
        language: "ru"
    };

/**
 * run function "f" if $container is found
 *
 * @param {object} $container - object to be tested
 * @param {function} f - function to run
 */
var rice = function($container, f) {
    if ($container.length>0) {f($container)}
};

$(document).ready(function() {

});