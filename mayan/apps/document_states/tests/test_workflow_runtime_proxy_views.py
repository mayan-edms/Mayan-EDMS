from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_workflow_view

from .mixins import (
    WorkflowRuntimeProxyStateViewTestMixin,
    WorkflowRuntimeProxyViewTestMixin, WorkflowTestMixin
)


class WorkflowRuntimeProxyViewTestCase(
    WorkflowRuntimeProxyViewTestMixin, WorkflowTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._create_test_document_stub()

    def test_workflow_runtime_proxy_document_list_view_no_permission(self):
        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow.label, status_code=404
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )

    def test_workflow_runtime_proxy_document_list_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_workflow_runtime_proxy_document_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow.label, status_code=404
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )

    def test_workflow_runtime_proxy_document_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow.label, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_trashed_document_workflow_runtime_proxy_document_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        self.test_document.delete()

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow.label, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_workflow_runtime_proxy_list_view_no_permission(self):
        response = self._request_test_workflow_runtime_proxy_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow.label, status_code=200
        )

    def test_workflow_runtime_proxy_list_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_list_view()
        self.assertContains(
            response=response, text=self.test_workflow.label, status_code=200
        )


class WorkflowRuntimeProxyStateViewTestCase(
    WorkflowRuntimeProxyStateViewTestMixin, WorkflowTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_states()
        self._create_test_workflow_transition()
        self._create_test_document_stub()

    def test_workflow_runtime_proxy_state_document_list_view_no_permission(self):
        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=404
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )

    def test_workflow_runtime_proxy_state_document_list_view_with_workflow_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_workflow_runtime_proxy_state_document_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=404
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )

    def test_workflow_runtime_proxy_state_document_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=200
        )
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_trashed_document_workflow_runtime_proxy_state_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        self.test_document.delete()

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

    def test_workflow_runtime_proxy_state_list_view_no_permission(self):
        response = self._request_test_workflow_runtime_proxy_state_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=404
        )

    def test_workflow_runtime_proxy_state_list_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_state_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=200
        )
