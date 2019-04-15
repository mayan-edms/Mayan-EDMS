from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import FilteredSelectionForm

from .models import AccessControlList


class ACLCreateForm(FilteredSelectionForm, forms.ModelForm):
    class Meta:
        field_name = 'role'
        fields = ('role',)
        label = _('Role')
        model = AccessControlList
        widget_attributes = {'class': 'select2'}
