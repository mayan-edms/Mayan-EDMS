from django import forms
from django.utils.translation import ugettext as _

from .links import link_spacer


class MultiItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        actions = kwargs.pop('actions', [])
        super(MultiItemForm, self).__init__(*args, **kwargs)
        choices = []
        group = []

        for action in actions:
            if not action[0]:
                if group:
                    choices.append((link_spacer['text'], group))
                group = []
            else:
                group.append(action)

        self.fields['action'].choices = choices

    action = forms.ChoiceField(label=_(u'Actions'), required=False)
