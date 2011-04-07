from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import capfirst


class MultiItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        actions = kwargs.pop('actions', [])
        super(MultiItemForm, self).__init__(*args, **kwargs)
        choices = [('', '------')]
        choices.extend([(action[0], capfirst(action[1])) for action in actions])
        self.fields['action'].choices = choices

    action = forms.ChoiceField(label=_(u'Multi item action'))
