from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import DetailForm

from ..fields import DocumentFileField
from ..models.document_file_models import DocumentFile

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


class DocumentFilePropertiesForm(DetailForm):
    """
    Detail class form to display a document file properties
    """
    def __init__(self, *args, **kwargs):
        document_file = kwargs['instance']

        extra_fields = [
            {
                'label': _('Date added'),
                'field': 'timestamp',
                'widget': forms.widgets.DateTimeInput
            },
            {
                'label': _('Mimetype'),
                'field': lambda x: document_file.mimetype or _('None')
            },
            {
                'label': _('Encoding'),
                'field': lambda x: document_file.encoding or _(
                    'None'
                )
            },
            {
                'label': _('Size'),
                'field': lambda document_file: filesizeformat(
                    document_file.size
                ) if document_file.size else '-'
            },
            {'label': _('Exists in storage'), 'field': 'exists'},
            {
                'label': _('Path in storage'),
                'field': 'file'
            },
            {'label': _('Checksum'), 'field': 'checksum'},
            {'label': _('Pages'), 'field': 'page_count'},
        ]

        kwargs['extra_fields'] = extra_fields
        super().__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = DocumentFile
