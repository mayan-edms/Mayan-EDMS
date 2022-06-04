from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.document_indexing.models.index_instance_models import IndexInstanceNode
from mayan.apps.document_indexing.tests.mixins import IndexTemplateTestMixin

from .literals import (
    TEST_WORKFLOW_INDEX_TEMPLATE_EXPRESSION,
    TEST_WORKFLOW_TEMPLATE_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_INDEX_TEMPLATE_EXPRESSION,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED
)
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin


class WorkflowInstanceIndexingTestCase(
    IndexTemplateTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_WORKFLOW_INDEX_TEMPLATE_EXPRESSION
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)

    def _create_test_workflow_states_and_transitions(self):
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflow_indexing_workflow_instance_no_initial_state(self):
        self._create_test_document_stub()

        test_workflow_instance = self._test_document.workflows.first()

        value = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )

    def test_workflow_indexing_workflow_instance_initial_state(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        test_workflow_instance = self._test_document.workflows.first()

        value = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )

    def test_workflow_indexing_workflow_instance_transition(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        test_workflow_instance = self._test_document.workflows.first()

        value = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self._test_document.workflows.first().do_transition(
            transition=self._test_workflow_template_transition
        )

        value_transitioned = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value_transitioned
            ).exists()
        )


class WorkflowTemplateIndexingTestCase(
    IndexTemplateTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_WORKFLOW_INDEX_TEMPLATE_EXPRESSION
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)

    def _create_test_workflow_states_and_transitions(self):
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflow_indexing_workflow_template_delete(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        self._test_workflow_template.delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
            ).exists()
        )

    def test_workflow_indexing_workflow_template_edit(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        test_workflow_instance = self._test_document.workflows.first()

        value = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self._test_workflow_template.label = TEST_WORKFLOW_TEMPLATE_LABEL_EDITED
        self._test_workflow_template.save()

        value_edited = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value_edited
            ).exists()
        )

    def test_workflow_indexing_workflow_template_state_delete(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        self._test_workflow_template_states[0].delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
            ).exists()
        )

    def test_workflow_indexing_workflow_template_state_edit(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        test_workflow_instance = self._test_document.workflows.first()

        value = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self._test_workflow_template_states[0].label = TEST_WORKFLOW_TEMPLATE_STATE_LABEL_EDITED
        self._test_workflow_template_states[0].save()

        value_edited = '{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state()
        )

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value_edited
            ).exists()
        )


class WorkflowTemplateTranstitionIndexingTestCase(
    IndexTemplateTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    _test_index_template_node_expression = TEST_WORKFLOW_TEMPLATE_TRANSITION_INDEX_TEMPLATE_EXPRESSION
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)

    def _create_test_workflow_states_and_transitions(self):
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflow_indexing_workflow_template_transition_delete(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        self._test_workflow_template_transition.delete()

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
            ).exists()
        )

    def test_workflow_indexing_workflow_template_transition_edit(self):
        self._create_test_workflow_states_and_transitions()
        self._create_test_document_stub()

        test_workflow_instance = self._test_document.workflows.first()

        value = '{}-{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state(),
            self._test_workflow_template.transitions.first()
        )

        self._test_workflow_template_transition.label = TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL_EDITED
        self._test_workflow_template_transition.save()

        value_edited = '{}-{}-{}'.format(
            self._test_workflow_template.label,
            test_workflow_instance.get_current_state(),
            self._test_workflow_template.transitions.first()
        )

        self.assertFalse(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value
            ).exists()
        )
        self.assertTrue(
            IndexInstanceNode.objects.filter(
                documents=self._test_document,
                value=value_edited
            ).exists()
        )
