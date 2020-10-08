from django import forms
from django.utils.translation import ugettext_lazy as _

from ..fields import DocumentVersionField
from ..models.document_version_models import DocumentVersion

__all__ = ('DocumentVersionForm', 'DocumentVersionPreviewForm',)


class DocumentVersionForm(forms.ModelForm):
    class Meta:
        fields = ('comment',)
        model = DocumentVersion


class DocumentVersionPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document_file = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        self.fields['document_file'].initial = document_file

    document_file = DocumentVersionField()
