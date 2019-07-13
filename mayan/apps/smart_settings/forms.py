from __future__ import unicode_literals

import yaml

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load


class SettingForm(forms.Form):
    value = forms.CharField(
        help_text=_('Enter the new setting value.'), required=False,
        widget=forms.widgets.Textarea()
    )

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        self.setting = self.initial['setting']
        self.fields['value'].help_text = self.setting.help_text
        self.fields['value'].initial = self.setting.serialized_value

    def clean(self):
        try:
            yaml_load(stream=self.cleaned_data['value'])
        except yaml.YAMLError:
            raise ValidationError(
                _(
                    '"%s" not a valid entry.'
                ) % self.cleaned_data['value']
            )
