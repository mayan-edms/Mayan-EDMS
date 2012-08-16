from __future__ import absolute_import

from django import forms

from app_registry.models import App
from common.widgets import ScrollableCheckboxSelectMultiple

from .models import BackupJob
from .api import AppBackup


def valid_app_choices():
    # Return app that exist in the app registry and that have been registered for backup
    return App.live.filter(pk__in=[appbackup.app.pk for appbackup in AppBackup.get_all()])


class BackupJobForm(forms.ModelForm):
    apps = forms.ModelMultipleChoiceField(queryset=valid_app_choices(), widget=ScrollableCheckboxSelectMultiple())

    class Meta:
        model = BackupJob
