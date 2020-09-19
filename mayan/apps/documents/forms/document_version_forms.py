from django import forms
from django.utils.translation import ugettext_lazy as _

from ..fields import DocumentVersionField

from .document_forms import DocumentDownloadForm

__all__ = ('DocumentVersionDownloadForm', 'DocumentVersionPreviewForm',)


class DocumentVersionDownloadForm(DocumentDownloadForm):
    preserve_extension = forms.BooleanField(
        label=_('Preserve extension'), required=False,
        help_text=_(
            'Takes the file extension and moves it to the end of the '
            'filename allowing operating systems that rely on file '
            'extensions to open the downloaded document file correctly.'
        )
    )


class DocumentVersionPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document_file = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        self.fields['document_file'].initial = document_file

    document_file = DocumentVersionField()
