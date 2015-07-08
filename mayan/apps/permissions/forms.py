from __future__ import unicode_literals

from django import forms

from .models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        fields = ('label',)
        model = Role
