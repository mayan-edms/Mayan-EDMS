from collections import OrderedDict

from django import forms

from mayan.apps.common.classes import ModelAttribute
from mayan.apps.views.widgets import NamedMultiWidget

from .literals import EMPTY_LABEL


class TemplateWidget(NamedMultiWidget):
    class Media:
        js = ('templating/js/template_widget.js',)

    def __init__(self, attrs=None, **kwargs):
        widgets = OrderedDict()

        widgets['model_attribute'] = forms.widgets.Select(
            attrs={'data-template-fields': 'model_attribute'}
        )
        widgets['template'] = forms.widgets.Textarea(
            attrs={'rows': 5, 'data-template-fields': 'template'}
        )
        super(TemplateWidget, self).__init__(
            widgets=widgets, attrs=attrs, **kwargs
        )

    def get_context(self, name, value, attrs):
        result = super(TemplateWidget, self).get_context(name, value, attrs)
        result['widget']['subwidgets'][0]['attrs']['required'] = False
        return result

    def decompress(self, value):
        attribute_choices = ModelAttribute.get_all_choices_for(
            model=self.attrs['model']
        )
        choices = []

        choices = attribute_choices
        choices.insert(
            0, ('', EMPTY_LABEL)
        )

        self.widgets['model_attribute'].choices = choices
        return {
            'model_attribute': None, 'template': value
        }

    def value_from_datadict(self, querydict, files, name):
        template = querydict.get('{}_template'.format(name))

        return template
