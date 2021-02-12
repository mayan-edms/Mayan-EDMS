from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.widgets import TextAreaDiv


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
