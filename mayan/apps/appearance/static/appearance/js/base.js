'use strict';

var app = new App();
var partialNavigation = new PartialNavigation({
    initialURL: initialURL,
    excludeAnchorClasses: ['fancybox', 'new_window', 'non-ajax'],
    formBeforeSerializeCallbacks: [App.MultiObjectFormProcess],
});

jQuery(document).ready(function() {
    app.setupFullHeightResizing();
    partialNavigation.initialize();
});

var afterBaseLoad = function () {
    MayanImage.intialize();
    app.doToastrMessages();
    app.setupAJAXperiodicWorkers();
    app.setupAutoSubmit();
    app.setupItemsSelector();
    app.setupNewWindowAnchor();
    app.setupTableSelector();
    app.setupSelect2();
    app.setupScrollView();
}
