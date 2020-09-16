from django import forms
from django.utils.translation import ugettext_lazy as _

from ..fields import DocumentFileField

from .document_forms import DocumentDownloadForm

__all__ = ('DocumentFileDownloadForm', 'DocumentFilePreviewForm',)


class DocumentFileDownloadForm(DocumentDownloadForm):
    preserve_extension = forms.BooleanField(
        label=_('Preserve extension'), required=False,
        help_text=_(
            'Takes the file extension and moves it to the end of the '
            'filename allowing operating systems that rely on file '
            'extensions to open the downloaded document file correctly.'
        )
    )


class DocumentFilePreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document_file = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        self.fields['document_file'].initial = document_file

    document_file = DocumentFileField()
