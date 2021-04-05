from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Workflow
from ..permissions import (
    permission_workflow_instance_transition,
    permission_workflow_template_view
)

from .literals import (
    TEST_WORKFLOW_TEMPLATE_LABEL, TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
)

from .mixins import (
    DocumentWorkflowTemplateAPIViewTestMixin, WorkflowTemplateTestMixin
)

#TODO: Add trashed document tests

class DocumentWorkflowsAPIViewTestCase(
    DocumentTestMixin, DocumentWorkflowTemplateAPIViewTestMixin,
    WorkflowTemplateTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_workflow_instance_detail_api_view_no_permission(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        response = self._request_test_workflow_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('workflow' in response.data)

    def test_workflow_instance_detail_api_view_with_workflow_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_view
        )

        response = self._request_test_workflow_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('workflow' in response.data)

    def test_workflow_instance_detail_api_view_with_document_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_document, permission=permission_workflow_template_view
        )

        response = self._request_test_workflow_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('workflow' in response.data)

    def test_workflow_instance_detail_api_view_with_full_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_workflow_template_view
        )

        response = self._request_test_workflow_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['workflow']['label'],
            TEST_WORKFLOW_TEMPLATE_LABEL
        )

    def test_workflow_instance_list_api_view_no_permission(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        response = self._request_test_workflow_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('result' in response.data)

    def test_workflow_instance_list_api_view_with_document_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_document, permission=permission_workflow_template_view
        )

        response = self._request_test_workflow_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_workflow_instance_list_api_view_with_workflow_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_view
        )

        response = self._request_test_workflow_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('result' in response.data)

    def test_workflow_instance_list_api_view_with_full_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_workflow_template_view
        )

        response = self._request_test_workflow_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['workflow']['label'],
            TEST_WORKFLOW_TEMPLATE_LABEL
        )

    def test_workflow_instance_log_entries_create_api_view_no_permission(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        workflow_instance = self.test_document.workflows.first()
        response = self._request_test_workflow_instance_log_entry_create_api_view(
            workflow_instance=workflow_instance
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # We get bad request because we try to create a transition for which
        # we don't have permission and therefore is not valid for this
        # workflow instance current state
        self.assertEqual(workflow_instance.log_entries.count(), 0)

    def test_workflow_instance_log_entries_create_api_view_with_workflow_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()

        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_instance_transition
        )
        workflow_instance = self.test_document.workflows.first()

        response = self._request_test_workflow_instance_log_entry_create_api_view(
            workflow_instance=workflow_instance
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        workflow_instance.refresh_from_db()
        self.assertEqual(
            workflow_instance.log_entries.first().transition.label,
            TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
        )

    def test_workflow_instance_log_entries_list_api_view_no_permission(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()
        self._create_test_workflow_template_instance_log_entry()

        response = self._request_test_workflow_instance_log_entry_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_workflow_instance_log_entries_list_api_view_with_document_access(self):
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_states()
        self._create_test_workflow_template_transition()
        self._create_test_document_stub()
        self._create_test_workflow_template_instance_log_entry()

        self.grant_access(
            obj=self.test_document, permission=permission_workflow_template_view
        )

        response = self._request_test_workflow_instance_log_entry_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['transition']['label'],
            TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
        )
