from django import forms
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

import mayan

from .widgets import TemplateWidget


class TemplateField(forms.CharField):
    widget = TemplateWidget

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.model_variable = kwargs.pop('model_variable')
        self.initial_help_text = kwargs.pop('initial_help_text', '')
        super(TemplateField, self).__init__(*args, **kwargs)
        self.help_text = format_lazy(
            '{} {}', self.initial_help_text,
            _(
                'Use Django\'s default templating language '
                '(https://docs.djangoproject.com/en/%(django_version)s/ref/templates/builtins/). '
                'The {{ %(variable)s }} variable is available to the template.'
            ) % {
                'django_version': mayan.__django_version__,
                'variable': self.model_variable
            }
        )
        self.widget.attrs['model'] = self.model
        self.widget.attrs['data-model-variable'] = self.model_variable
