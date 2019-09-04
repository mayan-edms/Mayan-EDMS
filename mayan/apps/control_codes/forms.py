from __future__ import unicode_literals

import yaml

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load

from .classes import ControlCode
from .models import ControlSheetCode


class ControlSheetCodeClassSelectionForm(forms.Form):
    control_code_class_name = forms.ChoiceField(
        choices=(), help_text=_('Available control codes.'),
        label=_('Control code'),
    )

    def __init__(self, *args, **kwargs):
        super(ControlSheetCodeClassSelectionForm, self).__init__(*args, **kwargs)

        self.fields[
            'control_code_class_name'
        ].choices = ControlCode.get_choices()


class ControlSheetCodeForm(forms.ModelForm):
    class Meta:
        fields = ('arguments', 'order', 'enabled')
        model = ControlSheetCode

    def clean(self):
        try:
            yaml_load(stream=self.cleaned_data['arguments'])
        except yaml.YAMLError:
            raise ValidationError(
                _(
                    '"%s" not a valid entry.'
                ) % self.cleaned_data['arguments']
            )
