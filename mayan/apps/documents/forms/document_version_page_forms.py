from django import forms
from django.utils.translation import ugettext_lazy as _

from ..fields import DocumentVersionPageField

__all__ = ('DocumentVersionPageForm', 'DocumentVersionPageNumberForm')


class DocumentVersionPageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        rotation = kwargs.pop('rotation', None)
        zoom = kwargs.pop('zoom', None)
        super(DocumentVersionPageForm, self).__init__(*args, **kwargs)
        self.fields['document_version_page'].initial = instance
        self.fields['document_version_page'].widget.attrs.update({
            'zoom': zoom,
            'rotation': rotation,
        })

    document_version_page = DocumentVersionPageField()


class DocumentVersionPageNumberForm(forms.Form):
    page = forms.ModelChoiceField(
        help_text=_(
            'Page number from which all the transformations will be cloned. '
            'Existing transformations will be lost.'
        ), queryset=None
    )

    def __init__(self, *args, **kwargs):
        self.document = kwargs.pop('document')
        super(DocumentVersionPageNumberForm, self).__init__(*args, **kwargs)
        self.fields['page'].queryset = self.document.pages.all()
