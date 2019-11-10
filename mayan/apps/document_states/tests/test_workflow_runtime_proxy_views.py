from __future__ import unicode_literals

from mayan.apps.common.tests.base import GenericViewTestCase

from ..permissions import permission_workflow_view

from .mixins import (
    WorkflowRuntimeProxyStateViewTestMixin,
    WorkflowRuntimeProxyViewTestMixin, WorkflowTestMixin
)


class WorkflowRuntimeProxyViewTestCase(
    WorkflowRuntimeProxyViewTestMixin, WorkflowTestMixin, GenericViewTestCase
):
    def setUp(self):
        super(WorkflowRuntimeProxyViewTestCase, self).setUp()
        self._create_test_workflow()

    def test_workflow_runtime_proxy_document_list_view_no_permission(self):
        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow.label, status_code=404
        )

    def test_workflow_runtime_proxy_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow.label, status_code=200
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
    GenericViewTestCase
):
    def setUp(self):
        super(WorkflowRuntimeProxyStateViewTestCase, self).setUp()
        self._create_test_workflow()
        self._create_test_workflow_states()

    def test_workflow_runtime_proxy_state_document_list_view_no_permission(self):
        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertNotContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=404
        )

    def test_workflow_runtime_proxy_state_document_list_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_runtime_proxy_state_document_list_view()
        self.assertContains(
            response=response, text=self.test_workflow_state_1.label,
            status_code=200
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
