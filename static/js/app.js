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

$(document).ready(function() {
    var $form = $("#report_form");
    $form.find('[name="date_from"],[name="date_to"]').datepicker(datepicker_defaults);
});