from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model


class UserForm(forms.ModelForm):
    class Meta:
        fields = (
            'username', 'first_name', 'last_name', 'email', 'is_active',
        )
        model = get_user_model()
