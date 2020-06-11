from django import forms

from mayan.apps.views.forms import FileDisplayForm, DetailForm

from .models import UserLocaleProfile


class LicenseForm(FileDisplayForm):
    DIRECTORY = ()
    FILENAME = 'LICENSE'


class LocaleProfileForm(forms.ModelForm):
    class Meta:
        fields = ('language', 'timezone')
        model = UserLocaleProfile
        widgets = {
            'language': forms.Select(
                attrs={
                    'class': 'select2'
                }
            ),
            'timezone': forms.Select(
                attrs={
                    'class': 'select2'
                }
            )
        }


class LocaleProfileForm_view(DetailForm):
    class Meta:
        fields = ('language', 'timezone')
        model = UserLocaleProfile
