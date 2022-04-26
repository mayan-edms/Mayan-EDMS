from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase


from .mixins.workflow_template_mixins import (
    WorkflowTaskTestCaseMixin, WorkflowTemplateTestMixin
)
from .mixins.workflow_template_state_escalation_mixins import (
    WorkflowTemplateStateEscalationTaskTestMixin,
    WorkflowTemplateStateEscalationTestMixin
)


class WorkflowTaskTestCase(
    WorkflowTaskTestCaseMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()

    def test_task_launch_all_workflows(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._execute_task_launch_all_workflows()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_all_workflows(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._test_document.delete()

        self._execute_task_launch_all_workflows()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count
        )

    def test_task_launch_workflow(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._execute_task_launch_workflow()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_workflow(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._test_document.delete()

        self._execute_task_launch_workflow()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count
        )

    def test_task_launch_workflow_for(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._execute_task_launch_workflow_for()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_workflow_for(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._test_document.delete()

        with self.assertRaises(expected_exception=Document.DoesNotExist):
            self._execute_task_launch_workflow_for()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count
        )

    def test_task_launch_all_workflow_for(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._execute_task_launch_all_workflow_for()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_all_workflow_for(self):
        workflow_instance_count = self._test_document.workflows.count()

        self._test_document.delete()

        with self.assertRaises(expected_exception=Document.DoesNotExist):
            self._execute_task_launch_all_workflow_for()

        self.assertEqual(
            self._test_document.workflows.count(), workflow_instance_count
        )


class WorkflowTemplateStateEscalationTaskTestCase(
    WorkflowTemplateStateEscalationTaskTestMixin,
    WorkflowTemplateStateEscalationTestMixin, WorkflowTemplateTestMixin,
    GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_state_escalation()
        self._create_test_document_stub()

    def test_task_workflow_instance_check_escalation(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._clear_events()

        self._execute_task_workflow_instance_check_escalation(
            test_workflow_instance_id=test_workflow_instance.pk
        )

        self.assertNotEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )
        self.assertEqual(
            test_workflow_instance.get_last_log_entry().comment,
            self._test_workflow_template_state_escalation.comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_task_workflow_instance_check_escalation_all(self):
        test_workflow_instance = self._test_document.workflows.first()
        test_workflow_instance_state = test_workflow_instance.get_current_state()

        self._clear_events()

        self._execute_task_workflow_instance_check_escalation_all()

        self.assertNotEqual(
            test_workflow_instance.get_current_state(),
            test_workflow_instance_state
        )
        self.assertEqual(
            test_workflow_instance.get_last_log_entry().comment,
            self._test_workflow_template_state_escalation.comment
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
