'use strict';

jQuery(document).ready(function() {
    $('[data-autocopy="true"]').change(function(event) {
        const $this = $(this);
        const $idTemplate = $this.siblings('[data-template-fields="template"]');
        const templateCursorPosition = $idTemplate.prop('selectionStart');
        let templateValue = $idTemplate.val();
        const fieldText = eval('`' + $this.data('field-template') + '`');

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
