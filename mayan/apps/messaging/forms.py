from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.user_management.querysets import get_user_queryset
from mayan.apps.views.widgets import TextAreaDiv

from .models import Message


class MessageCreateForm(forms.ModelForm):
    class Meta:
        fields = ('user', 'subject', 'body')
        model = Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {
            'class': 'full-height', 'data-height-difference': 560
        }
        self.fields['user'].queryset = get_user_queryset()
        self.fields['user'].widget.attrs = {'class': 'select2'}


class MessageDetailForm(forms.Form):
    body = forms.CharField(
        label=_('Body'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div full-height',
                'data-height-difference': 360,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        self.fields['body'].initial = self.instance.body
