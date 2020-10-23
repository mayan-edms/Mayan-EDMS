'use strict';

jQuery(document).ready(function() {
    $('[data-autocopy="true"]').change(function(event) {
        var $this = $(this);
        var $idTemplate = $this.siblings('[data-template-fields="template"]');
        var templateCursorPosition = $idTemplate.prop('selectionStart');
        var templateValue = $idTemplate.val();
        var fieldText = eval('`' + $this.data('field-template') + '`');

        templateValue = templateValue.slice(
            0, templateCursorPosition
        ) + fieldText + templateValue.slice(
            templateCursorPosition
        );
        $idTemplate.val(templateValue);
        $idTemplate.focus();
        $idTemplate.prop(
            'selectionStart', templateCursorPosition + fieldText.length
        );
        $idTemplate.prop(
            'selectionEnd', templateCursorPosition + fieldText.length
        );

        $this.val('');
    });
});
