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

var bind_stock_form = function($form) {
    var get_stock_url = $form.attr("data-get-stock-url");

    var $fieldsets_container = $("#extra_fields");

    var $btn_stock = $("#change_supply");

    var validator = $form.validate({
        ignore: [],
        errorPlacement:  function(error, element) {
            element.parent().toggleClass("has-error", true);
        },
        success: function(label, element) {
            $(element).parent().toggleClass("has-error", false);
        }
    });

    var bind_fieldset = function($fieldset) {
        var $body = $fieldset.find('[data-role="form-body"]');
        var $title = $fieldset.find('[data-role="fieldset-title"]');
        var $collapse = $fieldset.find('[data-action="collapse"]');

        var $name_source = $fieldset.find('[data-role="fieldset-name-source"]');

        var $fields = $fieldset.find("input, select");

        if ($name_source.is("select")) {
            $name_source.on("change", function() {
                $title.html($name_source.find(":selected").text());
            });
        } else {
            $name_source.on("change", function(){
                $title.html($name_source.val());
            });
        }

        $fieldset.find('[data-action="remove"]').on("click",function() {
            $fieldset.remove();
        });

        $collapse.on("click", function() {
            var valid = true;
            $fields.each(function(i, el) {
                valid = validator.element($fields.eq(i)) === false ? false : valid;
            });
            if (valid === true) {
                $body.toggleClass("collapse");
                $collapse.toggle();
            }
        });

        $fieldsets_container.append($fieldset);
    };

    var insert_fieldset = function(url) {
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: getCookie("csrftoken")
            },

            success: function (data) {
                if (data["html"]) {
                    bind_fieldset($(data["html"]));
                } else {
                    alert("Что-то пошло не так!(((");
                }
            },
            error: function (textStatus) {
                try {
                    console.log(textStatus)
                } catch (e) {
                }
            }
        });
    };

    $form.find('[name="date"]').datepicker(datepicker_defaults);

    $btn_stock.on("click", function () {
        insert_fieldset(get_stock_url);
    });
};

$(document).ready(function() {
    var $form = $("#report_form");
    $form.find('[name="date_from"],[name="date_to"]').datepicker(datepicker_defaults);
    var $supply_form = $("#supply_form");

    if ($supply_form.length>0) {
        bind_stock_form($supply_form);
    }
});