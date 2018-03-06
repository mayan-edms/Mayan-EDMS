'use strict';

var app = new App();

jQuery(document).ready(function() {
    app.setupFullHeightResizing();

    var partialNavigation = new PartialNavigation({
        initialURL: initialURL,
        excludeAnchorClasses: ['fancybox', 'new_window'],
    });
});

var afterBaseLoad = function () {
    MayanImage.intialize();

    app.doToastrMessages();
    app.setupAutoSubmit();
    app.setupItemsSelector();
    app.setupNewWindowAnchor();
    app.setupTableSelector();
    app.setupSelect2();
    app.setupScrollView();
}
