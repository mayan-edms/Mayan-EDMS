from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase

from ..tasks import (
    task_launch_all_workflows, task_launch_all_workflow_for,
    task_launch_workflow, task_launch_workflow_for
)

from .mixins import WorkflowTestMixin


class WorkflowTaskTestCaseMixin:
    def _execute_task_launch_all_workflows(self):
        task_launch_all_workflows.apply_async().get()

    def _execute_task_launch_all_workflow_for(self):
        task_launch_all_workflow_for.apply_async(
            kwargs={
                'document_id': self.test_document.pk,
            }
        ).get()

    def _execute_task_launch_workflow(self):
        task_launch_workflow.apply_async(
            kwargs={
                'workflow_id': self.test_workflow.pk
            }
        ).get()

    def _execute_task_launch_workflow_for(self):
        task_launch_workflow_for.apply_async(
            kwargs={
                'document_id': self.test_document.pk,
                'workflow_id': self.test_workflow.pk
            }
        ).get()


class WorkflowTaskTestCase(
    WorkflowTaskTestCaseMixin, WorkflowTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_state()

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
