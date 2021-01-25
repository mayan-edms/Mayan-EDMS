from django.utils.translation import ugettext_lazy as _

from mayan.apps.document_states.classes import WorkflowAction

from .models.document_type_models import DocumentType


class DocumentTypeChangeAction(WorkflowAction):
    fields = {
        'document_type': {
            'label': _('Document type'),
            'class': 'django.forms.ModelChoiceField', 'kwargs': {
                'help_text': _('New document type for the workflow document.'),
                'queryset': DocumentType.objects.all(), 'required': True
            }
        }
    }
    label = _('Change document type')
    widgets = {
        'workflows': {
            'class': 'django.forms.widgets.Select', 'kwargs': {
                'attrs': {'class': 'select2'},
            }
        }
    }

    def execute(self, context):
        context['document'].document_type_change(
            document_type=self.get_document_type()
        )

    def get_document_type(self):
        return DocumentType.objects.get(pk=self.form_data.get('document_type'))


class TrashDocumentAction(WorkflowAction):
    label = _('Send document to trash')

    def execute(self, context):
        context['document'].delete()
