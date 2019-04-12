from __future__ import unicode_literals

import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


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
        quotes = ['"', "'"]

        if self.setting.quoted:
            stripped = self.cleaned_data['value'].strip()

            if stripped[0] not in quotes or stripped[-1] not in quotes:
                raise ValidationError(
                    _(
                        'Value must be properly quoted.'
                    )
                )

        try:
            yaml.load(stream=self.cleaned_data['value'], Loader=SafeLoader)
        except yaml.YAMLError:
            raise ValidationError(
                _(
                    '"%s" not a valid entry.'
                ) % self.cleaned_data['value']
            )
