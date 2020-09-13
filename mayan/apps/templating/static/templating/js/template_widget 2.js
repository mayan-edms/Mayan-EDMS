'use strict';

jQuery(document).ready(function() {
    var fieldNameID = '[data-template-fields="model_attribute"]';
    $(fieldNameID).change(function(event) {
        var $idModelProperty = $(this);
        var $idTemplate = $('[data-template-fields="template"]');
        var templateCursorPosition = $idTemplate.prop('selectionStart');
        var templateValue = $idTemplate.val();
        var modelVariable = $idTemplate.data('model-variable');
        var propertyText = '{{ ' + modelVariable + '.' + $idModelProperty.val() + ' }}';

        templateValue = templateValue.slice(
            0, templateCursorPosition
        ) + propertyText + templateValue.slice(
            templateCursorPosition
        );
        $idTemplate.val(templateValue);
        $idTemplate.focus();
        $idTemplate.prop(
            'selectionStart', templateCursorPosition + propertyText.length
        );
        $idTemplate.prop(
            'selectionEnd', templateCursorPosition + propertyText.length
        );
        $(fieldNameID + ' option')[0].selected = true;
    });
});
