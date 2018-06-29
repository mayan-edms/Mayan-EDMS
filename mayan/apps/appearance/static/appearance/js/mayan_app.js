'use strict';

var App = function (parameters) {
    var self = this;

    parameters = parameters || {}

    this.window = $(window);
}

// Class methods and variables

App.mayanNotificationBadge = function (options, data) {
    // Callback to add the notifications count inside a badge markup
    var notifications = data[options.attributeName];

    if (notifications > 0) {
        // Save the original link text before adding the initial badge markup
        if (!options.element.data('mn-saved-text')) {
            options.element.data('mn-saved-text', options.element.html());
        }

        options.element.html(
            options.element.data('mn-saved-text') + ' <span class="badge">' + notifications + '</span>'
        );
    } else {
        if (options.element.data('mn-saved-text')) {
            // If there is a saved original link text, restore it
            options.element.html(
                options.element.data('mn-saved-text')
            );
        }
    }
}

App.MultiObjectFormProcess = function ($form, options) {
    /*
     * ajaxForm callback to add the external item checkboxes to the
     * submitted form
     */

    if ($form.hasClass('form-multi-object-action')) {
        // Turn form data into an object
        var formArray = $form.serializeArray().reduce(function (obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});

        // Add all checked checkboxes to the form data
        $('.form-multi-object-action-checkbox:checked').each(function() {
            var $this = $(this);
            formArray[$this.attr('name')] = $this.attr('value');
        });

        // Set the form data as the data to send
        options.data = formArray;
    }
}

App.tagSelectionTemplate = function (tag, container) {
  var $tag = $(
    '<span class="label label-tag" style="background: ' + tag.element.dataset.color + ';"> ' + tag.text + '</span>'
  );
  container[0].style.background = tag.element.dataset.color;
  return $tag;
}

App.tagResultTemplate = function (tag) {
  if (!tag.element) { return ''; }
  var $tag = $(
    '<span class="label label-tag" style="background: ' + tag.element.dataset.color + ';"> ' + tag.text + '</span>'
  );
  return $tag;
}

// Instance methods

App.prototype.AJAXperiodicWorker = function (options) {
    var app = this;

    $.ajax({
        complete: function() {
            if (!options.app) {
                // Preserve the app reference between consecutive calls
                options.app = app;
            }
            setTimeout(options.app.AJAXperiodicWorker, options.interval, options);
        },
        success: function(data) {
            if (options.callback) {
                // Conver the callback string to an actual function
                var callbackFunction = window;

                $.each(options.callback.split('.'), function (index, value) {
                    callbackFunction = callbackFunction[value]
                });

                callbackFunction(options, data);
            } else {
                options.element.text(data[options.attributeName]);
            }
        },
        url: options.APIURL
  });
}

App.prototype.doToastrMessages = function () {
    toastr.options = {
        'closeButton': true,
        'debug': false,
        'newestOnTop': true,
        'positionClass': 'toast-top-right',
        'preventDuplicates': false,
        'onclick': null,
        'showDuration': '300',
        'hideDuration': '1000',
        'timeOut': '5000',
        'extendedTimeOut': '1000',
        'showEasing': 'swing',
        'hideEasing': 'linear',
        'showMethod': 'fadeIn',
        'hideMethod': 'fadeOut'
    }

    // Add invisible bootstrap messages to copy the styles to toastr.js

    $('body').append('\
        <div class="hidden alert alert-success">\
            <p>text</p>\
        </div>\
        <div class="hidden alert alert-info">\
            <p>text</p>\
        </div>\
        <div class="hidden alert alert-danger">\
            <p>text</p>\
        </div>\
        <div class="hidden alert alert-warning">\
            <p>text</p>\
        </div>\
    ');

    // Copy the bootstrap style from the sample alerts to toaster.js via
    // dynamic document style tag

    $('head').append('\
        <style>\
            .toast-success {\
                background-color: ' + $('.alert-success').css('background-color') +'\
            }\
            .toast-info {\
                background-color: ' + $('.alert-info').css('background-color') +'\
            }\
            .toast-error {\
                background-color: ' + $('.alert-danger').css('background-color') +'\
            }\
            .toast-warning {\
                background-color: ' + $('.alert-warning').css('background-color') +'\
            }\
        </style>\
    ');

    $.each(DjangoMessages, function (index, value) {
        var options = {};

        if (value.tags === 'error') {
            // Error messages persist
            options['timeOut'] = 0;
        }
        if (value.tags === 'warning') {
            // Error messages persist
            options['timeOut'] = 10000;
        }

        toastr[value.tags](value.message, '', options);
    });
}

App.prototype.setupAJAXperiodicWorkers = function () {
    var app = this;

    $('a[data-apw-url]').each(function() {
        var $this = $(this);

        app.AJAXperiodicWorker({
            attributeName: $this.data('apw-attribute'),
            APIURL: $this.data('apw-url'),
            callback: $this.data('apw-callback'),
            element: $this,
            interval: $this.data('apw-interval'),
        });
    });
}

App.prototype.setupAutoSubmit = function () {
    $('body').on('change', '.select-auto-submit', function () {
        if ($(this).val()) {
            $(this.form).trigger('submit');
        }
    });
}

App.prototype.setupNavbarCollapse = function () {
    $(document).keyup(function(e) {
        if (e.keyCode === 27) {
            $('.navbar-collapse').collapse('hide');
        }
    });

    $('body').on('click', 'a', function (event) {
        if (!$(this).hasAnyClass(['dropdown-toggle'])) {
            $('.navbar-collapse').collapse('hide');
        }
    });
}

App.prototype.setupNewWindowAnchor = function () {
    $('body').on('click', 'a.new_window', function (event) {
        event.preventDefault();
        var newWindow = window.open($(this).attr('href'), '_blank');
        newWindow.focus();
    });
}

App.prototype.setupScrollView = function () {
    $('.scrollable').scrollview();
}

App.prototype.setupItemsSelector = function () {
    var app = this;
    app.lastChecked = null;

    $('body').on('click', '.check-all', function (event) {
        var checked = $(event.target).prop('checked');
        var $checkBoxes = $('.check-all-slave');

        $checkBoxes.prop('checked', checked);
        $checkBoxes.trigger('change');
    });

    $('body').on('click', '.check-all-slave', function(e) {
        if(!app.lastChecked) {
            app.lastChecked = this;
            return;
        }
        if(e.shiftKey) {
            var $checkBoxes = $('.check-all-slave');

            var start = $checkBoxes.index(this);
            var end = $checkBoxes.index(app.lastChecked);

            $checkBoxes.slice(
                Math.min(start,end), Math.max(start,end) + 1
            ).prop('checked', app.lastChecked.checked).trigger('change');
        }
        app.lastChecked = this;
    })
}

App.prototype.setupSelect2 = function () {
    $('.select2').select2({
        dropdownAutoWidth: true,
        width: '100%'
    });

    $('.select2-tags').select2({
        templateSelection: App.tagSelectionTemplate,
        templateResult: App.tagResultTemplate,
        width: '100%'
    });
}

App.prototype.setupFullHeightResizing = function () {
    var self = this;

    this.resizeFullHeight();

    this.window.resize(function() {
        self.resizeFullHeight();
    });
}

App.prototype.resizeFullHeight = function () {
    $('.full-height').height(this.window.height() - $('.full-height').data('height-difference'));
}
