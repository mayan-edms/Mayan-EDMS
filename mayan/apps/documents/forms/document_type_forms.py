from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList

from ..models import DocumentType, DocumentTypeFilename

__all__ = ('DocumentTypeFilteredSelectForm', 'DocumentTypeFilenameForm_create')


class DocumentTypeFilteredSelectForm(forms.Form):
    """
    Form to select the document type of a document to be created. This form
    is meant to be reused and reconfigured by other apps. Example: Used
    as form #1 in the document creation wizard.
    """
    def __init__(self, *args, **kwargs):
        help_text = kwargs.pop('help_text', None)
        if kwargs.pop('allow_multiple', False):
            extra_kwargs = {}
            field_class = forms.ModelMultipleChoiceField
            widget_class = forms.widgets.SelectMultiple
        else:
            extra_kwargs = {'empty_label': None}
            field_class = forms.ModelChoiceField
            widget_class = forms.widgets.Select

        permission = kwargs.pop('permission', None)
        user = kwargs.pop('user', None)

        super(DocumentTypeFilteredSelectForm, self).__init__(*args, **kwargs)

        queryset = DocumentType.objects.all()
        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset, user=user
            )

        self.fields['document_type'] = field_class(
            help_text=help_text, label=_('Document type'),
            queryset=queryset, required=True,
            widget=widget_class(attrs={'class': 'select2', 'size': 10}),
            **extra_kwargs
        )


class DocumentTypeFilenameForm_create(forms.ModelForm):
    """
    Model class form to create a new document type filename
    """
    class Meta:
        fields = ('filename',)
        model = DocumentTypeFilename
