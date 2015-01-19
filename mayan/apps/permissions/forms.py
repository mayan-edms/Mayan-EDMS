from __future__ import unicode_literals

from django import forms

from common.forms import DetailForm

from .models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'label')
        model = Role


class RoleForm_view(DetailForm):
    class Meta:
        fields = ('name', 'label')
        model = Role
