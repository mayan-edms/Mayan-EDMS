'use strict';

class MayanApp {
    constructor (options) {
        var self = this;

        this.options = options || {
            ajaxMenusOptions: []
        }

        this.ajaxExecuting = false;
        this.ajaxMenusOptions = options.ajaxMenusOptions;
        this.ajaxMenuHashes = {};
        this.ajaxSpinnerSeletor = '#ajax-spinner';
        this.window = $(window);
    }

    // Class methods and variables

    static countChecked() {
        var checkCount = $('.check-all-slave:checked').length;

        if (checkCount) {
            $('#multi-item-title').hide();
            $('#multi-item-actions').show();
        } else {
            $('#multi-item-title').show();
            $('#multi-item-actions').hide();
        }
    }

    static setupMultiItemActions () {
        $('body').on('change', '.check-all-slave', function () {
            MayanApp.countChecked();
        });

        $('body').on('click', '.btn-multi-item-action', function (event) {
            var id_list = [];
            $('.check-all-slave:checked').each(function (index, value) {
                //Split the name (ie:"pk_200") and extract only the ID
                id_list.push(value.name.split('_')[1]);
            });
            event.preventDefault();
            partialNavigation.setLocation(
                $(this).attr('href') + '?id_list=' + id_list.join(',')
            );
        });
    }

    static setupNavBarState () {
        $('body').on('click', '.a-main-menu-accordion-link', function (event) {
            var $this = $(this);

            $('.a-main-menu-accordion-link').each(function (index, value) {
                $this.parent().removeClass('active');
            });

            $this.parent().addClass('active');
        });
    }

    static updateNavbarState () {
        var uri = new URI(window.location.hash);
        var uriFragment = uri.fragment();
        $('.a-main-menu-accordion-link').each(function (index, value) {
            if (value.pathname === uriFragment) {
                var $this = $(this);

                $this.closest('.collapse').addClass('in').parent().find('.collapsed').removeClass('collapsed').attr('aria-expanded', 'true');
                $this.parent().addClass('active');
            }
        });
    }

    // Instance methods

    callbackAJAXSpinnerUpdate () {
        if (this.ajaxExecuting) {
            $(this.ajaxSpinnerSeletor).fadeIn(50);
        }
    }

    doBodyAdjust () {
        // Adjust the height of the body-spacer to move content elements
        // up or down when the navbar changes size.
        const navbarSize = 60;
        $('.body-spacer').css('height', $('.navbar').height() - navbarSize);
    }

    doRefreshAJAXMenu (options) {
        $.ajax({
            complete: function() {
                setTimeout(app.doRefreshAJAXMenu, options.interval, options);
            },
            success: function(data) {
                var menuHash = options.app.ajaxMenuHashes[data.name];

                if ((menuHash === undefined) || (menuHash !== data.hex_hash)) {
                    $(options.menuSelector).html(data.html);
                    options.app.ajaxMenuHashes[data.name] = data.hex_hash;
                    if (options.callback !== undefined) {
                        options.callback(options);
                    }
                }
            },
            url: options.url,
        });
    }

    doToastrMessages () {
        toastr.options = {
            'closeButton': true,
            'debug': false,
            'newestOnTop': true,
            'positionClass': 'toast-' + this.options.messagePosition,
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

    initialize () {
        var self = this;

        this.setupAJAXSpinner();
        this.setupBodyAdjust();
        this.setupFormHotkeys();
        this.setupFullHeightResizing();
        this.setupItemsSelector();
        MayanApp.setupMultiItemActions();
        this.setupNavbarCollapse();
        MayanApp.setupNavBarState();
        this.setupNewWindowAnchor();
        $.each(this.ajaxMenusOptions, function(index, value) {
            value.app = self;
            app.doRefreshAJAXMenu(value);
        });
        this.setupPanelSelection();
        partialNavigation.initialize();
    }

    setupAJAXSpinner () {
        var self = this;

        $(document).ajaxStart(function() {
            self.ajaxExecuting = true;
            setTimeout(
                function () {
                    self.callbackAJAXSpinnerUpdate();
                }, 450
            );
        });

        $(document).ready(function() {
            $(document).ajaxStop(function() {
                $(self.ajaxSpinnerSeletor).fadeOut();
                self.ajaxExecuting = false;
            });
        });
    }

    setupBodyAdjust () {
        var self = this;

        this.window.resize(function() {
            self.doBodyAdjust();
        });
    }

    setupFormHotkeys () {
        $('body').on('keypress', '.form-hotkey-enter', function (e) {
            if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
                $(this).find('.btn-hotkey-default').click();
                return false;
            } else {
                return true;
            }
        });
        $('body').on('dblclick', '.form-hotkey-double-click', function (e) {
            $(this).find('.btn-hotkey-default').click();
            return false;
        });
    }

    setupFullHeightResizing () {
        var self = this;

        this.resizeFullHeight();

        this.window.resize(function() {
            self.resizeFullHeight();
        });
    }

    setupItemsSelector () {
        var app = this;
        app.lastChecked = null;

        $('body').on('click', '.check-all', function (event) {
            var $this = $(this);
            var checked = $(event.target).prop('checked');
            var $checkBoxes = $('.check-all-slave');

            if (checked === undefined) {
                checked = $this.data('checked');
                checked = !checked;
                $this.data('checked', checked);

                if (checked) {
                    $this.find('[data-fa-i2svg]').addClass($this.data('icon-checked')).removeClass($this.data('icon-unchecked'));
                } else {
                    $this.find('[data-fa-i2svg]').addClass($this.data('icon-unchecked')).removeClass($this.data('icon-checked'));
                }
            }

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

    setupNavbarCollapse () {
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

    setupNewWindowAnchor () {
        $('body').on('click', 'a.new_window', function (event) {
            event.preventDefault();
            var newWindow = window.open($(this).attr('href'), '_blank');
            newWindow.focus();
        });
    }

    setupPanelSelection () {
        var app = this;

        // Setup panel highlighting on check
        $('body').on('change', '.check-all-slave', function (event) {
            var checked = $(event.target).prop('checked');
            if (checked) {
                $(this).closest('.panel-item').addClass('panel-highlighted');
            } else {
                $(this).closest('.panel-item').removeClass('panel-highlighted');
            }
        });

        $('body').on('click', '.panel-item', function (event) {
            var $this = $(this);
            var targetSrc = $(event.target).prop('src');
            var targetHref = $(event.target).prop('href');
            var targetIsButton = event.target.tagName === 'BUTTON';
            var lastChecked = null;

            if ((targetSrc === undefined) && (targetHref === undefined) && (targetIsButton === false)) {
                var $checkbox = $this.find('.check-all-slave');
                var checked = $checkbox.prop('checked');

                if (checked) {
                    $checkbox.prop('checked', '');
                    $checkbox.trigger('change');
                } else {
                    $checkbox.prop('checked', 'checked');
                    $checkbox.trigger('change');
                }

                if(!app.lastChecked) {
                    app.lastChecked = $checkbox;
                }

                if (event.shiftKey) {
                    var $checkBoxes = $('.check-all-slave');

                    var start = $checkBoxes.index($checkbox);
                    var end = $checkBoxes.index(app.lastChecked);

                    $checkBoxes.slice(
                        Math.min(start, end), Math.max(start, end) + 1
                    ).prop('checked', app.lastChecked.prop('checked')).trigger('change');
                }
                app.lastChecked = $checkbox;
                window.getSelection().removeAllRanges();
            }
        });
    }

    setupScrollView () {
        $('.scrollable').scrollview();
    }

    setupSelect2 () {
        $('.select2').select2({
            dropdownAutoWidth: true,
            width: '100%'
        });
    }

    resizeFullHeight () {
        $('.full-height').height(this.window.height() - $('.full-height').data('height-difference'));
    }
}
