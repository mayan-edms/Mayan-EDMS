from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active',)


class PasswordForm(forms.Form):
    new_password_1 = forms.CharField(label=_(u'New password'), widget=forms.PasswordInput())
    new_password_2 = forms.CharField(label=_(u'Confirm password'), widget=forms.PasswordInput())


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
