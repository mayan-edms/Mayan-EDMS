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

    // lastLocation - used as the AJAX referer
    this.lastLocation = null;

    // initialURL - the URL to send users when trying to access the / URL
    this.initialURL = parameters.initialURL || null;

    // excludeAnchorClasses - Anchors with any of these classes will not be processes as AJAX anchors
    this.excludeAnchorClasses = parameters.excludeAnchorClasses || [];

    // formBeforeSerializeCallbacks - Callbacks to execute before submitting an ajaxForm
    this.formBeforeSerializeCallbacks = parameters.formBeforeSerializeCallbacks || [];

    if (!this.initialURL) {
        alert('Need to setup initialURL');
    }
}

PartialNavigation.prototype.initialize = function () {
    this.setupAjaxAnchors();
    this.setupAjaxNavigation();
    this.setupAjaxForm();
}

PartialNavigation.prototype.filterLocation = function (newLocation) {
    var uri = new URI(newLocation);

    console.log('>> filterLocation.Newlocation: ' + newLocation);
    console.log('>> filterLocation.newLocation.uri.path(): ' + uri.path());

    var currentLocation = new URI(location);

    if (uri.path() === '') {
        // href with no path remain in the same location
        // We strip the same location query and use the new href's one
        uri.path(
            new URI(currentLocation.fragment()).path()
        )
        return uri.toString();
    }

    if (uri.path() === '/') {
        // Root URL is not allowed
        return this.initialURL;
    }

    return newLocation;
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
        success: function (data, textStatus, response){
            if (response.status == 278) {
                console.log('>> loadAjaxContent.ajax: got HTTP278');
                var newLocation = response.getResponseHeader('Location');

                console.log('>> loadAjaxContent.ajax.newLocation: ' + newLocation);
                app.setLocation(newLocation);
                app.lastLocation = newLocation;
            } else {
                app.lastLocation = url;
                if (response.getResponseHeader('Content-Disposition')) {
                    window.location = this.url;
                } else {
                    $('#ajax-content').html(data);
                }
            }
        },
        error: function (jqXHR, textStatus, errorThrown){
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
    if (jqXHR.status == 0) {
        $('#modal-server-error .modal-body').html($('#template-error').html());
        $('#modal-server-error').modal('show')
    } else {
        $('#ajax-content').html(jqXHR.responseText.replace(/\n/g, "<br />"));
    }
}

PartialNavigation.prototype.setLocation = function (newLocation, pushState) {
    console.log('>> setLocation.newLocation: ' + newLocation);
    console.log('>> setLocation.location: ' + location);
    newLocation = this.filterLocation(newLocation);

    if (typeof pushState === 'undefined') {
         pushState = true;
    }

    var currentLocation = new URI(location);
    currentLocation.fragment(newLocation);

    if (pushState) {
        history.pushState({}, '', currentLocation);
    }
    this.loadAjaxContent(newLocation);
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
        beforeSerialize: function($form, options) {
            $.each(app.formBeforeSerializeCallbacks, function (index, value) {
               value($form, options);
            });
        },
        beforeSubmit: function(arr, $form, options) {
            console.log('>> ajaxForm.beforeSubmit.$form.target: ' + $form.attr('action'));
            var uri = new URI(location);
            var uriFragment = uri.fragment();
            var url = $form.attr('action') || uriFragment;

            console.log('>>ajaxForm.$form.target.uriFragment:' + uriFragment);
            options.url = url;

            if ($form.attr('target') == '_blank') {
                window.open(
                    $form.attr('action') + '?' + decodeURIComponent($form.serialize())
                );

                return false;
            }

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

PartialNavigation.prototype.setupAjaxNavigation = function () {
    var app = this;

    // Load ajax content when the hash changes
    if (window.history && window.history.pushState) {
        $(window).on('popstate', function() {
            console.log('>> setupHashLocation.popstate.location: ' + location);
            var uri = new URI(location);
            var uriFragment = uri.fragment();
            app.setLocation(uriFragment, false);
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

    $.ajaxSetup({
        beforeSend: function (jqXHR, settings) {
            jqXHR.setRequestHeader('X-Alt-Referer', app.lastLocation);
        },
    });
}
