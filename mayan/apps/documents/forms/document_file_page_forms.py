from django import forms

from ..fields import DocumentFilePageField

__all__ = ('DocumentFilePageForm',)


class DocumentFilePageForm(forms.Form):
    document_file_page = DocumentFilePageField()

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        transformation_instance_list = kwargs.pop(
            'transformation_instance_list', ()
        )
        super().__init__(*args, **kwargs)
        self.fields['document_file_page'].initial = instance
        self.fields['document_file_page'].widget.attrs.update(
            {
                'transformation_instance_list': transformation_instance_list
            }
        )
