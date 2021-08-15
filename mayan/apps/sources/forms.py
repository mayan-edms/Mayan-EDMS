import json
import logging

from django import forms
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.forms.document_forms import DocumentForm
from mayan.apps.documents.literals import DOCUMENT_FILE_ACTION_PAGE_CHOICES
from mayan.apps.views.forms import DynamicModelForm

from .classes import SourceBackend
from .models import Source

logger = logging.getLogger(name=__name__)


class NewDocumentForm(DocumentForm):
    class Meta(DocumentForm.Meta):
        exclude = ('label', 'description')


class NewDocumentFileForm(forms.Form):
    comment = forms.CharField(
        help_text=_('An optional comment to explain the upload.'),
        label=_('Comment'), required=False,
        widget=forms.widgets.Textarea(attrs={'rows': 4}),
    )
    action = forms.ChoiceField(
        choices=DOCUMENT_FILE_ACTION_PAGE_CHOICES, label=_('Action'),
        help_text=_(
            'The action to take in regards to the pages of the new file '
            'being uploaded.'
        )
    )


class UploadBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop('source')

        super().__init__(*args, **kwargs)


class SourceBackendSelectionForm(forms.Form):
    backend = forms.ChoiceField(
        choices=(), help_text=_('The backend used to create the new source.'),
        label=_('Backend')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['backend'].choices = SourceBackend.get_choices()


class SourceBackendDynamicForm(DynamicModelForm):
    class Meta:
        fields = ('label', 'enabled', 'backend_data')
        model = Source
        widgets = {'backend_data': forms.widgets.HiddenInput}

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        if self.instance.backend_data:
            backend_data = json.loads(s=self.instance.backend_data)

            for key in self.instance.get_backend().get_fields():
                self.fields[key].initial = backend_data.get(key, None)

    def clean(self):
        data = super().clean()

        # Consolidate the dynamic fields into a single JSON field called
        # 'backend_data'.
        backend_data = {}

        for field_name, field_data in self.schema['fields'].items():
            backend_data[field_name] = data.pop(
                field_name, field_data.get('default', None)
            )
            if isinstance(backend_data[field_name], QuerySet):
                # Flatten the queryset to a list of ids
                backend_data[field_name] = list(
                    backend_data[field_name].values_list('id', flat=True)
                )
            elif isinstance(backend_data[field_name], Model):
                # Store only the ID of a model instance
                backend_data[field_name] = backend_data[field_name].pk

        data['backend_data'] = json.dumps(obj=backend_data)

        return data


class WebFormUploadFormHTML5(UploadBaseForm):
    file = forms.FileField(
        label=_('File'), widget=forms.widgets.FileInput(
            attrs={'class': 'hidden', 'hidden': True}
        )
    )
