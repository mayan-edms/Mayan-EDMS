from django import forms
from django.utils.translation import ugettext_lazy as _

from ..classes import DocumentVersionModification
from ..fields import DocumentVersionField
from ..models.document_version_models import DocumentVersion

__all__ = ('DocumentVersionForm', 'DocumentVersionPreviewForm',)


class DocumentVersionForm(forms.ModelForm):
    class Meta:
        fields = ('comment',)
        model = DocumentVersion


class DocumentVersionModificationBackendForm(forms.Form):
    backend = forms.ChoiceField(
        choices=(), help_text=_(
            'The backend that will be executed against the selected '
            'document version.'
        ), label=_('Backend')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['backend'].choices = DocumentVersionModification.get_choices()


class DocumentVersionPreviewForm(forms.Form):
    document_version = DocumentVersionField()

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
