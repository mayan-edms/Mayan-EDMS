'use strict';

var app = new App();
var partialNavigation = new PartialNavigation({
    initialURL: initialURL,
    excludeAnchorClasses: ['fancybox', 'new_window', 'non-ajax'],
    formBeforeSerializeCallbacks: [App.MultiObjectFormProcess],
});

jQuery(document).ready(function() {
    app.setupFullHeightResizing();
    app.setupNavbarCollapse();
    app.setupAJAXperiodicWorkers();
    partialNavigation.initialize();
});

var afterBaseLoad = function () {
    MayanImage.intialize();
    app.doToastrMessages();
    app.setupAutoSubmit();
    app.setupItemsSelector();
    app.setupNewWindowAnchor();
    app.setupTableSelector();
    app.resizeFullHeight();
    app.setupSelect2();
    app.setupScrollView();
}
