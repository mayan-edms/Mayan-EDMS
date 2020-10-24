from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import DetailForm

from ..fields import DocumentFileField
from ..literals import DEFAULT_DOCUMENT_FILE_ZIP_FILENAME
from ..models.document_file_models import DocumentFile

__all__ = (
    'DocumentFileForm', 'DocumentFilePreviewForm',
    'DocumentFilePropertiesForm'
)


class DocumentFileForm(forms.ModelForm):
    class Meta:
        fields = ('filename', 'comment',)
        model = DocumentFile


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
                'field': 'mimetype',
            },
            {
                'label': _('Encoding'),
                'field': 'encoding',
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
        declared_fields = ('mimetype',)
        fields = ('filename', 'comment',)
        model = DocumentFile
