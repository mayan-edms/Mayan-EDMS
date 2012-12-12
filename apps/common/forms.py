from __future__ import absolute_import

import os

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.conf import settings

from .utils import return_attrib
from .widgets import (DetailSelectMultiple, PlainWidget, TextAreaDiv,
    EmailInput)


class DetailForm(forms.ModelForm):
    def __init__(self, extra_fields=None, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        if extra_fields:
            for extra_field in extra_fields:
                result = return_attrib(self.instance, extra_field['field'])
                label = 'label' in extra_field and extra_field['label'] or None
                #TODO: Add others result types <=> Field types
                if isinstance(result, models.query.QuerySet):
                    self.fields[extra_field['field']] = \
                        forms.ModelMultipleChoiceField(
                            queryset=result, label=label)
                else:
                    self.fields[extra_field['field']] = forms.CharField(
                        label=extra_field['label'],
                        initial=return_attrib(self.instance,
                            extra_field['field'], None),
                            widget=PlainWidget)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.SelectMultiple):
                self.fields[field_name].widget = DetailSelectMultiple(
                    choices=field.widget.choices,
                    attrs=field.widget.attrs,
                    queryset=getattr(field, 'queryset', None),
                )
                self.fields[field_name].help_text = ''
            elif isinstance(field.widget, forms.widgets.Select):
                self.fields[field_name].widget = DetailSelectMultiple(
                    choices=field.widget.choices,
                    attrs=field.widget.attrs,
                    queryset=getattr(field, 'queryset', None),
                )
                self.fields[field_name].help_text = ''

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs.update({'readonly': 'readonly'})


class GenericConfirmForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pass


class GenericAssignRemoveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        left_list_qryset = kwargs.pop('left_list_qryset', None)
        right_list_qryset = kwargs.pop('right_list_qryset', None)
        left_filter = kwargs.pop('left_filter', None)
        super(GenericAssignRemoveForm, self).__init__(*args, **kwargs)
        if left_filter:
            self.fields['left_list'].queryset = left_list_qryset.filter(
                *left_filter)
        else:
            self.fields['left_list'].queryset = left_list_qryset

        self.fields['right_list'].queryset = right_list_qryset

    left_list = forms.ModelMultipleChoiceField(required=False, queryset=None)
    right_list = forms.ModelMultipleChoiceField(required=False, queryset=None)


class FilterForm(forms.Form):
    def __init__(self, list_filters, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        for list_filter in list_filters:
            label = list_filter.get('title', list_filter['name'])
            self.fields[list_filter['name']] = forms.ModelChoiceField(
                queryset=list_filter['queryset'],
                label=label[0].upper() + label[1:], required=False)


class ChoiceForm(forms.Form):
    """
    Form to be used in side by side templates used to add or remove
    items from a many to many field
    """
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        label = kwargs.pop('label', _(u'Selection'))
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.fields['selection'].choices = choices
        self.fields['selection'].label = label
        self.fields['selection'].widget.attrs.update({'size': 14, 'class': 'choice_form'})

    selection = forms.MultipleChoiceField()


class UserForm_view(DetailForm):
    """
    Form used to display an user's public details
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'groups')


class UserForm(forms.ModelForm):
    """
    Form used to edit an user's mininal fields by the user himself
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class EmailAuthenticationForm(AuthenticationForm):
    """
    Override the default authentication form to use email address
    authentication
    """
    email = forms.CharField(label=_(u'Email'), max_length=75,
        widget=EmailInput(attrs={'style': 'width: 100%;'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_('Please enter a correct email and password. Note that the password fields is case-sensitive.'))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account is inactive.'))
        self.check_for_test_cookie()
        return self.cleaned_data

# Remove the inherited username field
EmailAuthenticationForm.base_fields.keyOrder = ['email', 'password']


class FileDisplayForm(forms.Form):
    text = forms.CharField(
        label='',  # _(u'Text'),
        widget=forms.widgets.Textarea(
            attrs={'cols': 40, 'rows': 20, 'readonly': 'readonly'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(FileDisplayForm, self).__init__(*args, **kwargs)
        changelog_path = os.path.join(settings.PROJECT_ROOT, os.sep.join(self.DIRECTORY), self.FILENAME)
        fd = open(changelog_path)
        self.fields['text'].initial = fd.read()
        fd.close()


class LicenseForm(FileDisplayForm):
    FILENAME = u'LICENSE'
    DIRECTORY = [u'docs', u'credits']
