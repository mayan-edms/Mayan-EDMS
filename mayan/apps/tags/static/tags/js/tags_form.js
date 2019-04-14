'use strict';

var tagSelectionTemplate = function (tag, container) {
    var $tag = $(
        '<span class="label label-tag" style="background: ' + tag.element.dataset.color + ';"> ' + tag.text + '</span>'
    );
    container[0].style.background = tag.element.dataset.color;
    return $tag;
}

var tagResultTemplate = function (tag) {
    if (!tag.element) { return ''; }
    var $tag = $(
        '<span class="label label-tag" style="background: ' + tag.element.dataset.color + ';"> ' + tag.text + '</span>'
    );
    return $tag;
}

jQuery(document).ready(function() {
    $('.select2-tags').select2({
        templateSelection: tagSelectionTemplate,
        templateResult: tagResultTemplate,
        width: '100%'
    });
});
