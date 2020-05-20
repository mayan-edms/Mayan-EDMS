from mayan.apps.document_states.tests.mixins import WorkflowTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY

from ..models.document_models import TrashedDocument
from ..workflow_actions import TrashDocumentAction

from .literals import TEST_TRASH_DOCUMENT_WORKFLOW_ACTION_DOTTED_PATH


class TrashDocumentActionActionTestCase(
    WorkflowTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_trash_document_action(self):
        trashed_document_count = TrashedDocument.objects.count()

        self._upload_test_document()

        action = TrashDocumentAction()

        action.execute(context={'document': self.test_document})

        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count + 1
        )

    def test_trash_document_action_workflow_execution(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self.test_workflow_states[1].actions.create(
            action_path=TEST_TRASH_DOCUMENT_WORKFLOW_ACTION_DOTTED_PATH,
            label='', when=WORKFLOW_ACTION_ON_ENTRY,
        )
        self.test_workflow.document_types.add(self.test_document_type)

        trashed_document_count = TrashedDocument.objects.count()

        self._upload_test_document()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_transition
        )

        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count + 1
        )
