'use strict';

var app = new App();
var partialNavigation = new PartialNavigation({
    initialURL: initialURL,
    excludeAnchorClasses: ['fancybox', 'new_window', 'non-ajax'],
    formBeforeSerializeCallbacks: [App.MultiObjectFormProcess],
});

jQuery(document).ready(function() {
    app.setupAutoSubmit();
    app.setupFullHeightResizing();
    app.setupItemsSelector();
    app.setupNavbarCollapse();
    app.setupNewWindowAnchor();
    app.setupAJAXperiodicWorkers();
    partialNavigation.initialize();
});

var afterBaseLoad = function () {
    MayanImage.intialize();
    app.doToastrMessages();
    app.resizeFullHeight();
    app.setupSelect2();
    app.setupScrollView();
}
