from django import forms

from ..fields import DocumentFilePageField

__all__ = ('DocumentFilePageForm',)


class DocumentFilePageForm(forms.Form):
    document_file_page = DocumentFilePageField()

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        rotation = kwargs.pop('rotation', None)
        zoom = kwargs.pop('zoom', None)
        super().__init__(*args, **kwargs)
        self.fields['document_file_page'].initial = instance
        self.fields['document_file_page'].widget.attrs.update({
            'zoom': zoom,
            'rotation': rotation,
        })
