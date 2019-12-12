from __future__ import absolute_import, unicode_literals

import logging
import os

from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import DetailForm

from ..fields import DocumentField
from ..models import Document
from ..literals import DEFAULT_ZIP_FILENAME, PAGE_RANGE_ALL, PAGE_RANGE_CHOICES
from ..utils import get_language, get_language_choices

__all__ = (
    'DocumentDownloadForm', 'DocumentForm', 'DocumentPreviewForm',
    'DocumentPropertiesForm', 'DocumentPrintForm'
)
logger = logging.getLogger(__name__)


class DocumentDownloadForm(forms.Form):
    compressed = forms.BooleanField(
        label=_('Compress'), required=False,
        help_text=_(
            'Download the document in the original format or in a compressed '
            'manner. This option is selectable only when downloading one '
            'document, for multiple documents, the bundle will always be '
            'downloads as a compressed file.'
        )
    )
    zip_filename = forms.CharField(
        initial=DEFAULT_ZIP_FILENAME, label=_('Compressed filename'),
        required=False,
        help_text=_(
            'The filename of the compressed file that will contain the '
            'documents to be downloaded, if the previous option is selected.'
        )
    )

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop('queryset', None)
        super(DocumentDownloadForm, self).__init__(*args, **kwargs)
        if self.queryset.count() > 1:
            self.fields['compressed'].initial = True
            self.fields['compressed'].widget.attrs.update(
                {'disabled': 'disabled'}
            )


class DocumentForm(forms.ModelForm):
    """
    Form sub classes from DocumentForm used only when editing a document
    """
    class Meta:
        fields = ('label', 'description', 'language')
        model = Document
        widgets = {
            'language': forms.Select(
                choices=get_language_choices(), attrs={
                    'class': 'select2'
                }
            )

        }

    def __init__(self, *args, **kwargs):
        document_type = kwargs.pop('document_type', None)

        super(DocumentForm, self).__init__(*args, **kwargs)

        # Is a document (documents app edit) and has been saved (sources
        # app upload)?
        if self.instance and self.instance.pk:
            document_type = self.instance.document_type

        filenames_queryset = document_type.filenames.filter(enabled=True)

        if filenames_queryset:
            self.fields[
                'document_type_available_filenames'
            ] = forms.ModelChoiceField(
                queryset=filenames_queryset,
                required=False,
                label=_('Quick document rename'),
                widget=forms.Select(
                    attrs={
                        'class': 'select2'
                    }
                )
            )
            self.fields['preserve_extension'] = forms.BooleanField(
                label=_('Preserve extension'), required=False,
                help_text=_(
                    'Takes the file extension and moves it to the end of the '
                    'filename allowing operating systems that rely on file '
                    'extensions to open document correctly.'
                )
            )

    def clean(self):
        self.cleaned_data['label'] = self.get_final_label(
            # Fallback to the instance label if there is no label key or
            # there is a label key and is an empty string
            filename=self.cleaned_data.get('label') or self.instance.label
        )

        return self.cleaned_data

    def get_final_label(self, filename):
        if 'document_type_available_filenames' in self.cleaned_data:
            if self.cleaned_data['document_type_available_filenames']:
                if self.cleaned_data['preserve_extension']:
                    filename, extension = os.path.splitext(filename)

                    filename = '{}{}'.format(
                        self.cleaned_data[
                            'document_type_available_filenames'
                        ].filename, extension
                    )
                else:
                    filename = self.cleaned_data[
                        'document_type_available_filenames'
                    ].filename

        return filename


class DocumentPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document = kwargs.pop('instance', None)
        super(DocumentPreviewForm, self).__init__(*args, **kwargs)
        self.fields['document'].initial = document

    document = DocumentField()


class DocumentPropertiesForm(DetailForm):
    """
    Detail class form to display a document file based properties
    """
    def __init__(self, *args, **kwargs):
        document = kwargs['instance']

        extra_fields = [
            {
                'label': _('Date added'),
                'field': 'date_added',
                'widget': forms.widgets.DateTimeInput
            },
            {'label': _('UUID'), 'field': 'uuid'},
            {
                'label': _('Language'),
                'field': lambda x: get_language(language_code=document.language)
            },
        ]

        if document.latest_version:
            extra_fields += (
                {
                    'label': _('File mimetype'),
                    'field': lambda x: document.file_mimetype or _('None')
                },
                {
                    'label': _('File encoding'),
                    'field': lambda x: document.file_mime_encoding or _(
                        'None'
                    )
                },
                {
                    'label': _('File size'),
                    'field': lambda document: filesizeformat(
                        document.size
                    ) if document.size else '-'
                },
                {'label': _('Exists in storage'), 'field': 'exists'},
                {
                    'label': _('File path in storage'),
                    'field': 'latest_version.file'
                },
                {'label': _('Checksum'), 'field': 'checksum'},
                {'label': _('Pages'), 'field': 'page_count'},
            )

        kwargs['extra_fields'] = extra_fields
        super(DocumentPropertiesForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ('document_type', 'description')
        model = Document


class DocumentPrintForm(forms.Form):
    page_group = forms.ChoiceField(
        choices=PAGE_RANGE_CHOICES, initial=PAGE_RANGE_ALL,
        widget=forms.RadioSelect
    )
    page_range = forms.CharField(label=_('Page range'), required=False)
