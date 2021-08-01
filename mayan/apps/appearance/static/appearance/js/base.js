'use strict';

// Make it globally available. Used by event.links

const MayanAppClass = MayanApp;

const partialNavigation = new PartialNavigation({
    initialURL: initialURL,
    disabledAnchorClasses: [
        'btn-multi-item-action', 'disabled', 'pagination-disabled'
    ],
    excludeAnchorClasses: ['fancybox', 'new_window', 'non-ajax'],
});
