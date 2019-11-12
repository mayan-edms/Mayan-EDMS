from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

import mayan

from .widgets import TemplateWidget


class TemplateField(forms.CharField):
    widget = TemplateWidget

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.model_variable = kwargs.pop('model_variable')
        super(TemplateField, self).__init__(*args, **kwargs)
        self.help_text = _(
            'The template string to be evaluated. '
            'Use Django\'s default templating language '
            '(https://docs.djangoproject.com/en/%(django_version)s/ref/templates/builtins/)'
        ) % {'django_version': mayan.__django_version__}
        self.widget.attrs['model'] = self.model
        self.widget.attrs['data-model-variable'] = self.model_variable
