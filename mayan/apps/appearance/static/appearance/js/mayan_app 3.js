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

    static setupDropdownDirectionChange () {
        $('body').on('shown.bs.dropdown', '.dropdown', function () {
            var $this = $(this);
            var $elementMenu = $this.children('.dropdown-menu');
            var $elementMenuButton = $this.children('.dropdown-toggle');
            var elemenMenuOffset = $elementMenu.offset();
            var sizeDownwards = elemenMenuOffset.top + $elementMenu.height() + 5;
            var sizeUpwards = elemenMenuOffset.top - $elementMenu.height() - $elementMenuButton.height();

            var spaceDownwards = $(window).scrollTop() + $(window).height() - sizeDownwards;
            var spaceUpwards = sizeUpwards - $(window).scrollTop();

            if ((spaceUpwards >= 0 || spaceUpwards > spaceDownwards) && spaceDownwards < 0) {
              $this.addClass('dropup');
            }
        });

        $('body').on('hidden.bs.dropdown', '.dropdown', function() {
            $(this).removeClass('dropup');
        });
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
        $('body').on('click', '#accordion-sidebar a', function (event) {
            $('#accordion-sidebar a').each(function (index, value) {
                $(this).parents('li').removeClass('active');
            });

            $(this).parents('li').addClass('active');
        });
    }

    static updateNavbarState () {
        var uri = new URI(window.location.hash);
        var uriFragment = uri.fragment();
        $('#accordion-sidebar a').each(function (index, value) {
            if (value.pathname === uriFragment) {
                var $this = $(this);

                $this.closest('.collapse').addClass('in').parent().find('.collapsed').removeClass('collapsed').attr('aria-expanded', 'true');
                $this.parents('li').addClass('active');
            }
        });
    }

    // Instance methods

    callbackAJAXSpinnerUpdate () {
        if (this.ajaxExecuting) {
            $(this.ajaxSpinnerSeletor).fadeIn(50);
        }
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

        $('#div-javascript-dynamic-content').html('\
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

        $('#style-javascript').html('\
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
        MayanApp.setupDropdownDirectionChange();
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

    setupListToolbar () {
        var $listToolbar = $('#list-toolbar');

        if ($listToolbar.length !== 0) {
            var $listToolbarClearfix = $listToolbar.closest('.clearfix');
            var $listToolbarSpacer = $('#list-toolbar-spacer');
            var navBarOuterHeight = $('.navbar-fixed-top').outerHeight();

            $listToolbarSpacer.height($listToolbarClearfix.height()).hide();

            $listToolbar.css(
                {
                    width: $listToolbarClearfix.width(),
                }
            );

            $listToolbar.affix({
                offset: {
                    top: $listToolbar.offset().top - navBarOuterHeight,
                },
            });

            $listToolbar.on('affix.bs.affix', function () {
                $listToolbarSpacer.show();

                $listToolbar.css(
                    {
                        width: $listToolbarClearfix.width(),
                    }
                );
            });


            $listToolbar.on('affix-top.bs.affix', function () {
                $listToolbarSpacer.hide();
            });

            this.window.on('resize', function () {
                $listToolbar.css(
                    {
                        width: $listToolbarClearfix.width(),
                    }
                );
            });
        }
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

        // Small screen main menu toggle to open
        $('body').on('click', '#main-menu-button-open', function (event) {
            $('#menu-main').addClass('menu-main-opened');
            $('#ajax-header').addClass('overlay-gray');
        });

        // Small screen main menu toggle to close
        $('body').on('click', '#menu-main-button-close', function (event) {
            $('#menu-main').removeClass('menu-main-opened');
            $('#ajax-header').removeClass('overlay-gray');
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
            var targetSelection = window.getSelection().toString();
            if (!targetSelection) {
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
