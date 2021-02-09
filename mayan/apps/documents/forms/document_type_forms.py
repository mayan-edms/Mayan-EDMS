from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import FilteredSelectionForm

from ..classes import BaseDocumentFilenameGenerator
from ..models import DocumentType, DocumentTypeFilename

__all__ = (
    'DocumentTypeFilenameGeneratorForm', 'DocumentTypeFilteredSelectForm',
    'DocumentTypeFilenameForm_create'
)


class DocumentTypeFilenameGeneratorForm(forms.ModelForm):
    class Meta:
        fields = (
            'filename_generator_backend',
            'filename_generator_backend_arguments'
        )
        model = DocumentType
        widgets = {
            'filename_generator_backend': forms.widgets.Select(
                choices=BaseDocumentFilenameGenerator.get_choices()
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            'filename_generator_backend'
        ].choices = BaseDocumentFilenameGenerator.get_choices()


class DocumentTypeFilenameForm_create(forms.ModelForm):
    """
    Model class form to create a new document type filename
    """
    class Meta:
        fields = ('filename',)
        model = DocumentTypeFilename


class DocumentTypeFilteredSelectForm(FilteredSelectionForm):
    class Meta:
        field_name = 'document_type'
        label = _('Document type')
        queryset = DocumentType.objects.all()
        required = True
        widget_attributes = {'class': 'select2', 'size': 10}
