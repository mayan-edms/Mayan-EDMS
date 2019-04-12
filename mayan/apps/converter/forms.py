from __future__ import unicode_literals

import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Transformation


class TransformationForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'arguments', 'order')
        model = Transformation

    def clean(self):
        try:
            yaml.load(stream=self.cleaned_data['arguments'], Loader=SafeLoader)
        except yaml.YAMLError:
            raise ValidationError(
                _(
                    '"%s" not a valid entry.'
                ) % self.cleaned_data['arguments']
            )
