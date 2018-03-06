'use strict';

$.fn.hasAnyClass = function() {
    for (var i = 0; i < arguments[0].length; i++) {
        if (this.hasClass(arguments[0][i])) {
            return true;
        }
    }
    return false;
}

var PartialNavigation = function (parameters) {
    parameters = parameters || {};

    this.initialURL = parameters.initialURL || null;
    this.excludeAnchorClasses = parameters.excludeAnchorClasses || [];

    if (!this.initialURL) {
        alert('Need to setup initialURL');
    }

    this.setupAjaxAnchors();
    this.setupHashLocation();
    this.setupAjaxForm();
}

PartialNavigation.prototype.filterLocation = function (location) {
    var uri = new URI(location);

    console.log('>> filterLocation.location: ' + location);
    console.log('>> filterLocation.uri.path(): ' + uri.path());
    if (uri.path() === '/') {
        // Root URL is not allowed
        return this.initialURL;
    }

    return location;
}

PartialNavigation.prototype.loadAjaxContent = function (url) {
    var app = this;

    console.log('>> loadAjaxContent.url: ' + url);
    url = this.filterLocation(url);
    console.log('>> loadAjaxContent.filterLocation.url: ' + url);
    $.ajax({
        async: true,
        mimeType: 'text/html; charset=utf-8', // ! Need set mimeType only when run from local file
        url: url,
        type: 'GET',
        success: function(data, textStatus, response){
            if (response.status == 278) {
                console.log('>> loadAjaxContent.ajax: got HTTP278');
                var newLocation = response.getResponseHeader('Location');

                console.log('>> loadAjaxContent.ajax.newLocation: ' + newLocation);

                app.setLocation(newLocation);
            } else {
                if (response.getResponseHeader('Content-Disposition')) {
                    window.location = this.url;
                } else {
                    $('#ajax-content').html(data);
                }
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            app.processAjaxRequestError(jqXHR);
        },
        dataType: 'html',
    });
}

PartialNavigation.prototype.onAnchorClick = function ($this, event) {
    console.log('>> onAnchorClick');
    var url;

    if ($this.hasAnyClass(this.excludeAnchorClasses)) {
        return true;
    }

    url = $this.attr('href');
    if (url === undefined) {
        return true;
    }

    event.preventDefault();

    console.log('>> onAnchorClick.url: ' + url);

    if ((url !== '#') && !($this.hasClass('disabled') || $this.parent().hasClass('disabled'))) {
        this.setLocation(url);
    }
}

PartialNavigation.prototype.processAjaxRequestError = function (jqXHR) {
    window.history.back();

    if (jqXHR.status == 0) {
        $('#modal-server-error .modal-body').html($('#template-error').html());
    } else {
        $('#modal-server-error .modal-body').html(jqXHR.responseText.replace(/\n/g, "<br />"));
    }

    $('#modal-server-error').modal('show')
}

PartialNavigation.prototype.setLocation = function (newLocation) {
    console.log('>> setLocation.newLocation: ' + newLocation);
    console.log('>> setLocation.location: ' + location);
    newLocation = this.filterLocation(newLocation);

    var currentLocationPath = new URI(location).fragment();
    var newLocationPath = new URI(newLocation).path();

    console.log(currentLocationPath);
    console.log(newLocationPath);
    if (currentLocationPath === newLocationPath) {
        // New location same as old, force a reload
        this.loadAjaxContent(newLocation);
    }
    window.location.hash = newLocation;
}

PartialNavigation.prototype.setupAjaxAnchors = function () {
    var app = this;
    $('body').on('click', 'a', function (event) {
        app.onAnchorClick($(this), event);
    });
}

PartialNavigation.prototype.setupAjaxForm = function () {
    var app = this;

    $('form').ajaxForm({
        async: true,
        beforeSubmit: function(arr, $form, options) {
            console.log('>> ajaxForm.beforeSubmit.$form.target: ' + $form.attr('action'));

            var uri = new URI(location);
            var uriFragment = uri.fragment();
            console.log('>>ajaxForm.$form.target.uriFragment:' + uriFragment);

            var url = $form.attr('action') || uriFragment;

            options.url = url;
            console.log('>>ajaxForm.url:' + url);
        },
        dataType: 'html',
        delegation: true,
        error: function(jqXHR, textStatus, errorThrown){
            app.processAjaxRequestError(jqXHR);
        },
        mimeType: 'text/html; charset=utf-8', // ! Need set mimeType only when run from local file
        success: function(data, textStatus, request){
            if (request.status == 278) {
                console.log('>> ajaxForm: Got HTTP 278');
                var newLocation = request.getResponseHeader('Location');

                var uri = new URI(newLocation);
                var uriFragment = uri.fragment();

                console.log('>>ajaxForm.newLocation:' + newLocation);
                console.log('>>ajaxForm.newLocation.uriFragment:' + uriFragment);
                console.log('>>ajaxForm.window.location.hash:' + window.location.hash);

                var currentUri = new URI(window.location.hash);
                var currentUriFragment = currentUri.fragment();

                var url = uriFragment || currentUriFragment;

                app.setLocation(newLocation);

            } else {
                console.log('>>ajaxForm.success');
                $('#ajax-content').html(data);
            }
        }
    });
}

PartialNavigation.prototype.setupHashLocation = function () {
    var app = this;

    // Load ajax content when the hash changes
    if (window.history && window.history.pushState) {
        $(window).on('popstate', function() {
            console.log('>> setupHashLocation.location: ' + location);
            var uri = new URI(location);
            var uriFragment = uri.fragment();
            app.loadAjaxContent(uriFragment);
        });
    }

    // Load any initial address in the URL of the browser
    if (window.location.hash) {
        var uri = new URI(window.location.hash);
        var uriFragment = uri.fragment();
        this.setLocation(uriFragment);
    } else {
        this.setLocation('/');
    }
}
