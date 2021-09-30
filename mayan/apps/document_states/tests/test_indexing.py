from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import TEST_INDEX_TEMPLATE_METADATA_EXPRESSION
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin


class DocumentStateIndexingTestCase(
    IndexTemplateTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_INDEX_TEMPLATE_METADATA_EXPRESSION
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflow_indexing_initial_state(self):
        self._create_test_document_stub()

        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', str(self.test_workflow_template_states[0])]
        )

    def test_workflow_indexing_transition(self):
        self._create_test_document_stub()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_template_transition
        )

        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', str(self.test_workflow_template_states[1])]
        )

    def test_workflow_indexing_document_delete(self):
        self._create_test_document_stub()

        self.test_document.workflows.first().do_transition(
            transition=self.test_workflow_template_transition
        )

        self.test_document.delete(to_trash=False)

        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['']
        )
