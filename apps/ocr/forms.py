from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from ocr.models import QueueTransformation


class QueueTransformationForm(forms.ModelForm):
    class Meta:
        model = QueueTransformation

    def __init__(self, *args, **kwargs):
        super(QueueTransformationForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()


class QueueTransformationForm_create(forms.ModelForm):
    class Meta:
        model = QueueTransformation
        exclude = ('content_type', 'object_id')
