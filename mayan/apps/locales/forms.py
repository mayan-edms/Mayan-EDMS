from django import forms

from mayan.apps.views.forms import DetailForm

from .models import UserLocaleProfile


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
