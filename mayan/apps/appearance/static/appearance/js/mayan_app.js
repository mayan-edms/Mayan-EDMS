'use strict';

var App = function (parameters) {
    var self = this;

    parameters = parameters || {}

    this.window = $(window);
}

// Class methods and variables

App.tagSelectionTemplate = function (tag, container) {
  var $tag = $(
    '<span class="label label-tag" style="background: ' + tag.element.style.color + ';"> ' + tag.text + '</span>'
  );
  container[0].style.background = tag.element.style.color;
  return $tag;
}

App.tagResultTemplate = function (tag) {
  if (!tag.element) { return ''; }
  var $tag = $(
    '<span class="label label-tag" style="background: ' + tag.element.style.color + ';"> ' + tag.text + '</span>'
  );
  return $tag;
}

// Instance methods

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
            options['timeOut'] = 10000;
        }
        toastr[value.tags](value.message, '', options);
    });
}

App.prototype.setupAutoSubmit = function () {
    $('.select-auto-submit').change(function () {
        if ($(this).val()) {
            this.form.submit();
        }
    });
}

App.prototype.setupNewWindowAnchor = function () {
    $('a.new_window').click(function (event) {
        var newWindow = window.open($(this).attr('href'), '_blank');
        newWindow.focus();
    });
}

App.prototype.setupScrollView = function () {
    $('.scrollable').scrollview();
}

App.prototype.setupTableSelector = function () {
    $('th input:checkbox').click(function(e) {
        var table = $(e.target).closest('table');
        var checked = $(e.target).prop('checked');
        $('td input:checkbox', table).prop('checked', checked);
    });
}

App.prototype.setupItemsSelector = function () {
    $('.check-all').click(function(e) {
        var parent = $(e.target).closest('.well');
        var checked = $(e.target).prop('checked');
        $('.panel-item input:checkbox', parent).prop('checked', checked);
    });
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
