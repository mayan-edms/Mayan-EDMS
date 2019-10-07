from __future__ import unicode_literals

from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import Workflow
from ..permissions import (
    permission_workflow_create, permission_workflow_delete,
    permission_workflow_edit, permission_workflow_view,
    permission_workflow_tools
)

from .literals import TEST_WORKFLOW_LABEL, TEST_WORKFLOW_LABEL_EDITED
from .mixins import WorkflowTestMixin, WorkflowViewTestMixin


class WorkflowViewTestCase(
    WorkflowTestMixin, WorkflowViewTestMixin, GenericViewTestCase
):
    def test_workflow_create_view_no_permission(self):
        response = self._request_test_workflow_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Workflow.objects.count(), 0)

    def test_workflow_create_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_create)

        response = self._request_test_workflow_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Workflow.objects.count(), 1)
        self.assertEqual(Workflow.objects.all()[0].label, TEST_WORKFLOW_LABEL)

    def test_workflow_delete_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_workflow in Workflow.objects.all())

    def test_workflow_delete_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_delete
        )

        response = self._request_test_workflow_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertFalse(self.test_workflow in Workflow.objects.all())

    def test_workflow_edit_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow.refresh_from_db()
        self.assertEqual(self.test_workflow.label, TEST_WORKFLOW_LABEL)

    def test_workflow_edit_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow.refresh_from_db()
        self.assertEqual(self.test_workflow.label, TEST_WORKFLOW_LABEL_EDITED)

    def test_workflow_list_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_list_view()

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, text=self.test_workflow.label)

    def test_workflow_list_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=self.test_workflow.label)

    def test_workflow_template_preview_view_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_template_preview_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(self.test_workflow in Workflow.objects.all())

    def test_workflow_template_preview_view_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )
        response = self._request_test_workflow_template_preview_view()
        self.assertEqual(response.status_code, 200)


class WorkflowToolViewTestCase(WorkflowTestMixin, GenericDocumentViewTestCase):
    def _request_workflow_launch_view(self):
        return self.post(
            viewname='document_states:tool_launch_workflows',
        )

    def test_tool_launch_workflows_view_no_permission(self):
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.assertEqual(self.test_document.workflows.count(), 0)

        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.test_document.workflows.count(), 0)

    def test_tool_launch_workflows_view_with_permission(self):
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()

        self.grant_permission(permission=permission_workflow_tools)
        self.assertEqual(self.test_document.workflows.count(), 0)

        response = self._request_workflow_launch_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.workflows.first().workflow, self.test_workflow
        )
