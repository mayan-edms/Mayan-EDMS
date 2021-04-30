from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase


from .mixins.workflow_template_mixins import (
    WorkflowTaskTestCaseMixin, WorkflowTemplateTestMixin
)


class WorkflowTaskTestCase(
    WorkflowTaskTestCaseMixin, WorkflowTemplateTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()

    def test_task_launch_all_workflows(self):
        workflow_instance_count = self.test_document.workflows.count()

        self._execute_task_launch_all_workflows()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_all_workflows(self):
        workflow_instance_count = self.test_document.workflows.count()

        self.test_document.delete()

        self._execute_task_launch_all_workflows()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

    def test_task_launch_workflow(self):
        workflow_instance_count = self.test_document.workflows.count()

        self._execute_task_launch_workflow()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_workflow(self):
        workflow_instance_count = self.test_document.workflows.count()

        self.test_document.delete()

        self._execute_task_launch_workflow()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

    def test_task_launch_workflow_for(self):
        workflow_instance_count = self.test_document.workflows.count()

        self._execute_task_launch_workflow_for()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_workflow_for(self):
        workflow_instance_count = self.test_document.workflows.count()

        self.test_document.delete()

        with self.assertRaises(expected_exception=Document.DoesNotExist):
            self._execute_task_launch_workflow_for()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )

    def test_task_launch_all_workflow_for(self):
        workflow_instance_count = self.test_document.workflows.count()

        self._execute_task_launch_all_workflow_for()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count + 1
        )

    def test_trashed_document_task_launch_all_workflow_for(self):
        workflow_instance_count = self.test_document.workflows.count()

        self.test_document.delete()

        with self.assertRaises(expected_exception=Document.DoesNotExist):
            self._execute_task_launch_all_workflow_for()

        self.assertEqual(
            self.test_document.workflows.count(), workflow_instance_count
        )
