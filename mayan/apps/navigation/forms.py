from __future__ import unicode_literals

from django import forms


class MultiItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        actions = kwargs.pop('actions', [])
        if actions:
            actions.insert(0, ['', '---'])

        super(MultiItemForm, self).__init__(*args, **kwargs)

        self.fields['action'].choices = actions

    action = forms.ChoiceField(
        label='', required=False, widget=forms.widgets.Select(
            attrs={'class': 'select-auto-submit'}
        )
    )
