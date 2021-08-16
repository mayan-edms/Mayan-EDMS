from django import forms

from ..fields import DocumentVersionField
from ..models.document_version_models import DocumentVersion

__all__ = ('DocumentVersionForm', 'DocumentVersionPreviewForm',)


class DocumentVersionForm(forms.ModelForm):
    class Meta:
        fields = ('comment',)
        model = DocumentVersion


class DocumentVersionPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document_version = kwargs.pop('instance', None)
        transformation_instance_list = kwargs.pop(
            'transformation_instance_list', ()
        )
        super().__init__(*args, **kwargs)
        self.fields['document_version'].initial = document_version
        self.fields['document_version'].widget.attrs.update(
            {
                'transformation_instance_list': transformation_instance_list
            }
        )

    document_version = DocumentVersionField()
