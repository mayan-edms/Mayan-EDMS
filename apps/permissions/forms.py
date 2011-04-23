from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DetailForm

from permissions.models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role


class RoleForm_view(DetailForm):
    class Meta:
        model = Role


class ChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        label = kwargs.pop('label', _(u'Selection'))
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['selection'].choices = choices
        self.fields['selection'].label = label
        self.fields['selection'].widget.attrs.update({'size': 14})

    selection = forms.MultipleChoiceField()
