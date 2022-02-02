from mayan.apps.documents.tests.base import GenericDocumentTestCase

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_transition_mixins import WorkflowTransitionFieldTestMixin


class WorkflowTemplateTransitionFieldModelTestCase(
    WorkflowTemplateTestMixin, WorkflowTransitionFieldTestMixin,
    GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_transition_field()
        self._create_test_document_stub()

    def test_deleted_field_context_references(self):
        """
        Transition a workflow with a transition field, and the delete the
        transition field. The retrieving the context should work even with an
        obsolete field reference.
        """
        self._transition_test_workflow_instance(
            extra_data={
                self.test_workflow_template_transition_field.name: 'test'
            }
        )
        self.test_document.workflows.first().log_entries.first().get_extra_data()
        self.test_workflow_template_transition_field.delete()
        self.test_document.workflows.first().log_entries.first().get_extra_data()
