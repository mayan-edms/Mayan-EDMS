'use strict';

jQuery(document).ready(function() {
    const tagSelectionTemplate = function (tag, container) {
        const $tag = $(
            '<span class="label label-tag" style="background: ' + tag.element.dataset.color + ';"> ' + tag.text + '</span>'
        );
        container[0].style.background = tag.element.dataset.color;
        return $tag;
    }

    const tagResultTemplate = function (tag) {
        if (!tag.element) { return ''; }
        const $tag = $(
            '<span class="label label-tag" style="background: ' + tag.element.dataset.color + ';"> ' + tag.text + '</span>'
        );
        return $tag;
    }

    $('.select2-tags').select2({
        templateSelection: tagSelectionTemplate,
        templateResult: tagResultTemplate,
        width: '100%'
    });
});
