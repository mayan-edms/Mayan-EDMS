from mayan.apps.documents.tests.base import GenericDocumentTestCase


from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_state_escalation.mixins import WorkflowTemplateStateEscalationModelTestMixin


class WorkflowTemplateStateEscalationModelTestCase(
    WorkflowTemplateStateEscalationModelTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

        self._create_test_document_stub()

    def test_workflow_template_state_escalation(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._create_test_workflow_template_state_escalation()

        self._clear_events()

        test_workflow_instance.check_escalation()
        self.assertNotEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )
        self.assertEqual(
            test_workflow_instance.get_last_log_entry().comment,
            self._create_test_workflow_template_state_escalation.comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_condition_true(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._create_test_workflow_template_state_escalation(
            extra_data={'condition': 'TRUE'}
        )

        self._clear_events()

        test_workflow_instance.check_escalation()
        self.assertNotEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )
        self.assertEqual(
            test_workflow_instance.get_last_log_entry().comment,
            self._create_test_workflow_template_state_escalation.comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_condition_false(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._create_test_workflow_template_state_escalation(
            extra_data={'condition': '{{ none }}'}
        )

        self._clear_events()

        test_workflow_instance.check_escalation()
        self.assertEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_no_escalation(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._clear_events()

        test_workflow_instance.check_escalation()
        self.assertEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
