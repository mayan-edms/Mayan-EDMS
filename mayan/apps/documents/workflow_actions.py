from django.utils.translation import ugettext_lazy as _

from mayan.apps.document_states.classes import WorkflowAction


class TrashDocumentAction(WorkflowAction):
    label = _('Send document to trash')

    def execute(self, context):
        context['document'].delete()
