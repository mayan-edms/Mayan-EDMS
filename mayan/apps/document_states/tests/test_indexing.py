from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models import (
    IndexInstanceNode, IndexTemplate
)

from .literals import (
    TEST_INDEX_TEMPLATE_LABEL, TEST_INDEX_TEMPLATE_METADATA_EXPRESSION
)
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin


class DocumentStateIndexingTestCase(
    WorkflowTemplateTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def _create_test_index_template(self):
        # Create empty index
        index_template = IndexTemplate.objects.create(
            label=TEST_INDEX_TEMPLATE_LABEL
        )

        # Add our document type to the new index
        index_template.document_types.add(self.test_document_type)

        # Create simple index template
        root = index_template.template_root
        index_template.node_templates.create(
            parent=root, expression=TEST_INDEX_TEMPLATE_METADATA_EXPRESSION,
            link_documents=True
        )

    def test_workflow_indexing_initial_state(self):
        self._create_test_index_template()
        self._upload_test_document()

        self.assertEqual(
            list(
                IndexInstanceNode.objects.values_list('value', flat=True)
            ), ['', str(self.test_workflow_template_states[0])]
        )

    def test_workflow_indexing_transition(self):
        self._create_test_index_template()
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
        self._create_test_index_template()
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
