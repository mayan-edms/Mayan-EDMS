from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active',)


class PasswordForm(forms.Form):
    new_password_1 = forms.CharField(
        label=_('New password'), widget=forms.PasswordInput()
    )
    new_password_2 = forms.CharField(
        label=_('Confirm password'), widget=forms.PasswordInput()
    )
