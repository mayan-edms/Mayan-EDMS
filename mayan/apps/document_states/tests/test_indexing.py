from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models import Index, IndexInstanceNode

from ..models import Workflow

from .literals import (
    TEST_INDEX_LABEL, TEST_INDEX_TEMPLATE_METADATA_EXPRESSION,
    TEST_WORKFLOW_INTERNAL_NAME, TEST_WORKFLOW_INITIAL_STATE_LABEL,
    TEST_WORKFLOW_INITIAL_STATE_COMPLETION, TEST_WORKFLOW_LABEL,
    TEST_WORKFLOW_STATE_LABEL, TEST_WORKFLOW_STATE_COMPLETION,
    TEST_WORKFLOW_TRANSITION_LABEL
)


class DocumentStateIndexingTestCase(GenericDocumentTestCase):
    auto_upload_test_document = False

    def _create_test_workflow(self):
        self.test_workflow = Workflow.objects.create(
            label=TEST_WORKFLOW_LABEL,
            internal_name=TEST_WORKFLOW_INTERNAL_NAME
        )
        self.test_workflow.document_types.add(self.test_document_type)

    def _create_test_workflow_states(self):
        self._create_test_workflow()
        self.test_workflow_state_1 = self.test_workflow.states.create(
            completion=TEST_WORKFLOW_INITIAL_STATE_COMPLETION,
            initial=True, label=TEST_WORKFLOW_INITIAL_STATE_LABEL
        )
        self.test_workflow_state_2 = self.test_workflow.states.create(
            completion=TEST_WORKFLOW_STATE_COMPLETION,
            label=TEST_WORKFLOW_STATE_LABEL
        )

    def _create_test_workflow_transition(self):
        self._create_test_workflow_states()
        self.test_workflow_transition = self.test_workflow.transitions.create(
            label=TEST_WORKFLOW_TRANSITION_LABEL,
            origin_state=self.test_workflow_state_1,
            destination_state=self.test_workflow_state_2,
        )

    def _create_test_index(self):
        # Create empty index
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        # Add our document type to the new index
        index.document_types.add(self.test_document_type)

        # Create simple index template
        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_INDEX_TEMPLATE_METADATA_EXPRESSION,
            link_documents=True
        )

    def test_workflow_indexing_initial_state(self):
        self._create_test_workflow_transition()
        self._create_test_index()
        self._upload_test_document()

        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', TEST_WORKFLOW_INITIAL_STATE_LABEL]
        )

    def test_workflow_indexing_transition(self):
        self._create_test_workflow_transition()
        self._create_test_index()
        self._upload_test_document()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_transition,
            user=self._test_case_user
        )

        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', TEST_WORKFLOW_STATE_LABEL]
        )

    def test_workflow_indexing_document_delete(self):
        self._create_test_workflow_transition()
        self._create_test_index()
        self._upload_test_document()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_transition,
            user=self._test_case_user
        )

        self.test_document.delete(to_trash=False)

        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['']
        )
