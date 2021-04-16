import json

from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models.trashed_document_models import TrashedDocument
from ..workflow_actions import DocumentTypeChangeAction, TrashDocumentAction

from .literals import (
    TEST_DOCUMENT_TYPE_CHANGE_ACTION_DOTTED_PATH,
    TEST_TRASH_DOCUMENT_WORKFLOW_ACTION_DOTTED_PATH
)


class WorkflowActionActionTestCase(
    WorkflowTemplateTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_change_action(self):
        self._upload_test_document()

        document_type = self.test_document.document_type

        self._create_test_document_type(label='document type 2')

        action = DocumentTypeChangeAction(
            form_data={'document_type': self.test_document_types[1].pk}
        )

        action.execute(context={'document': self.test_document})

        self.assertNotEqual(
            self.test_document.document_type, document_type
        )

    def test_document_type_change_action_execution(self):
        self._create_test_document_type(label='document type 2')

        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self.test_workflow_template_states[1].actions.create(
            action_data=json.dumps(obj={'document_type': self.test_document_types[1].pk}),
            action_path=TEST_DOCUMENT_TYPE_CHANGE_ACTION_DOTTED_PATH,
            label='', when=WORKFLOW_ACTION_ON_ENTRY,

        )
        self.test_workflow_template.document_types.add(self.test_document_types[0])

        self._upload_test_document(document_type=self.test_document_types[0])

        document_type = self.test_document.document_type

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_template_transition
        )

        self.assertNotEqual(
            self.test_document.document_type, document_type
        )

    def test_trash_document_action(self):
        trashed_document_count = TrashedDocument.objects.count()

        self._upload_test_document()

        action = TrashDocumentAction()

        action.execute(context={'document': self.test_document})

        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count + 1
        )

    def test_trash_document_action_workflow_execution(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self.test_workflow_template_states[1].actions.create(
            action_path=TEST_TRASH_DOCUMENT_WORKFLOW_ACTION_DOTTED_PATH,
            label='', when=WORKFLOW_ACTION_ON_ENTRY,
        )
        self.test_workflow_template.document_types.add(self.test_document_type)

        trashed_document_count = TrashedDocument.objects.count()

        self._upload_test_document()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_template_transition
        )

        self.assertEqual(
            TrashedDocument.objects.count(), trashed_document_count + 1
        )
