from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class MultiItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        actions = kwargs.pop('actions', [])
        super(MultiItemForm, self).__init__(*args, **kwargs)

        self.fields['action'].choices = actions

    action = forms.ChoiceField(label=_('Actions'), required=False)
