from __future__ import absolute_import

from django import forms

from app_registry.models import App

from .models import BackupJob
from .api import AppBackup


def valid_app_choices():
    return App.live.filter(name__in=[appbackup.name for appbackup in AppBackup.get_all()])


class BackupJobForm(forms.ModelForm):
    #expiration_datetime = SplitTimeDeltaField()

    apps = forms.ModelChoiceField(queryset=valid_app_choices())

    class Meta:
        model = BackupJob
        #exclude = ('checkout_datetime', 'user_content_type', 'user_object_id')

        #widgets = {
        #    'document': forms.widgets.HiddenInput(),
        #}

    #def clean_document(self):
    #    document = self.cleaned_data['document']
    #    if document.is_checked_out():
    #        raise DocumentAlreadyCheckedOut
    #    return document
