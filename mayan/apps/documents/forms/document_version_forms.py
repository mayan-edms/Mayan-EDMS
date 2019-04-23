from __future__ import absolute_import, unicode_literals

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
            'extensions to open the downloaded document version correctly.'
        )
    )


class DocumentVersionPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document_version = kwargs.pop('instance', None)
        super(DocumentVersionPreviewForm, self).__init__(*args, **kwargs)
        self.fields['document_version'].initial = document_version

    document_version = DocumentVersionField()
