from __future__ import absolute_import, unicode_literals

from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.classes import ModelProperty
from mayan.apps.common.widgets import NamedMultiWidget


class TemplateWidget(NamedMultiWidget):
    class Media:
        js = ('templating/js/template_widget.js',)

    def __init__(self, attrs=None, **kwargs):
        widgets = OrderedDict()

        widgets['model_property'] = forms.widgets.Select(
            attrs={'data-template-fields': 'model_property'}
        )
        widgets['template'] = forms.widgets.Textarea(
            attrs={'rows': 5, 'data-template-fields': 'template'}
        )
        super(TemplateWidget, self).__init__(
            widgets=widgets, attrs=attrs, **kwargs
        )

    def decompress(self, value):
        choices = ModelProperty.get_choices_for(
            model=self.attrs['model']
        )
        self.widgets['model_property'].choices = (
            [('', _('<Model property choices>'))] + choices
        )
        return {
            'model_property': None, 'template': value
        }

    def value_from_datadict(self, querydict, files, name):
        template = querydict.get('{}_template'.format(name))

        return template
