'use strict';

// Make it globally available. Used by event.links

var MayanAppClass = MayanApp;

var partialNavigation = new PartialNavigation({
    initialURL: initialURL,
    disabledAnchorClasses: ['disabled'],
    excludeAnchorClasses: ['fancybox', 'new_window', 'non-ajax'],
    formBeforeSerializeCallbacks: [MayanApp.MultiObjectFormProcess],
});
