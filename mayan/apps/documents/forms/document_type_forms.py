from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList

from ..models import DocumentType, DocumentTypeFilename
from ..permissions import permission_document_create

__all__ = ('DocumentTypeSelectForm', 'DocumentTypeFilenameForm_create')


class DocumentTypeSelectForm(forms.Form):
    """
    Form to select the document type of a document to be created, used
    as form #1 in the document creation wizard
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DocumentTypeSelectForm, self).__init__(*args, **kwargs)

        queryset = AccessControlList.objects.filter_by_access(
            permission_document_create, user,
            queryset=DocumentType.objects.all()
        )

        self.fields['document_type'] = forms.ModelChoiceField(
            empty_label=None, label=_('Document type'), queryset=queryset,
            required=True, widget=forms.widgets.Select(attrs={'size': 10})
        )


class DocumentTypeFilenameForm_create(forms.ModelForm):
    """
    Model class form to create a new document type filename
    """
    class Meta:
        fields = ('filename',)
        model = DocumentTypeFilename
