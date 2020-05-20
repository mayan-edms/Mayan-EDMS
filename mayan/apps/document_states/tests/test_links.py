from django.urls import reverse

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..links import (
    link_workflow_runtime_proxy_document_list,
    link_workflow_runtime_proxy_list,
    link_workflow_runtime_proxy_state_document_list,
    link_workflow_runtime_proxy_state_list,
)
from ..permissions import permission_workflow_view

from .mixins import WorkflowTestMixin


class WorkflowRuntimeProxyLinkTestCase(
    WorkflowTestMixin, GenericDocumentViewTestCase
):
    def _resolve_test_link(self, test_object=None):
        self.add_test_view(test_object=test_object)
        context = self.get_test_view()
        self.resolved_test_link = self.test_link.resolve(context=context)

    def test_workflow_runtime_proxy_document_list_link_no_permission(self):
        self.test_link = link_workflow_runtime_proxy_document_list

        self._create_test_workflow(add_document_type=True)

        self._resolve_test_link(test_object=self.test_workflow_runtime_proxy)

        self.assertEqual(self.resolved_test_link, None)

    def test_workflow_runtime_proxy_document_list_link_with_access(self):
        self.test_link = link_workflow_runtime_proxy_document_list

        self._create_test_workflow(add_document_type=True)

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        self._resolve_test_link(test_object=self.test_workflow_runtime_proxy)

        self.assertNotEqual(self.resolved_test_link, None)
        self.assertEqual(
            self.resolved_test_link.url,
            reverse(
                viewname=self.test_link.view, kwargs={
                    'workflow_runtime_proxy_id': self.test_workflow_runtime_proxy.pk
                }
            )
        )

    def test_workflow_runtime_proxy_link_no_permission(self):
        self.test_link = link_workflow_runtime_proxy_list

        self._create_test_workflow(add_document_type=True)

        self._resolve_test_link()
        self.assertEqual(self.resolved_test_link, None)

    def test_workflow_runtime_proxy_link_with_access(self):
        self.test_link = link_workflow_runtime_proxy_list

        self._create_test_workflow(add_document_type=True)

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        self._resolve_test_link()

        self.assertNotEqual(self.resolved_test_link, None)
        self.assertEqual(
            self.resolved_test_link.url,
            reverse(
                viewname=self.test_link.view,
            )
        )

    def test_workflow_runtime_proxy_state_document_list_link_no_permission(self):
        self.test_link = link_workflow_runtime_proxy_state_document_list

        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_state()

        self._resolve_test_link(test_object=self.test_workflow_state_runtime_proxy)

        self.assertEqual(self.resolved_test_link, None)

    def test_workflow_runtime_proxy_state_document_list_link_with_access(self):
        self.test_link = link_workflow_runtime_proxy_state_document_list

        self._create_test_workflow(add_document_type=True)
        self._create_test_workflow_state()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        self._resolve_test_link(test_object=self.test_workflow_state_runtime_proxy)

        self.assertNotEqual(self.resolved_test_link, None)
        self.assertEqual(
            self.resolved_test_link.url,
            reverse(
                viewname=self.test_link.view, kwargs={
                    'workflow_runtime_proxy_state_id': self.test_workflow_state_runtime_proxy.pk
                }
            )
        )

    def test_workflow_runtime_proxy_state_list_link_no_permission(self):
        self.test_link = link_workflow_runtime_proxy_state_list

        self._create_test_workflow(add_document_type=True)

        self._resolve_test_link(test_object=self.test_workflow_runtime_proxy)
        self.assertEqual(self.resolved_test_link, None)

    def test_workflow_runtime_proxy_state_list_link_with_access(self):
        self.test_link = link_workflow_runtime_proxy_state_list

        self._create_test_workflow(add_document_type=True)

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        self._resolve_test_link(test_object=self.test_workflow_runtime_proxy)

        self.assertNotEqual(self.resolved_test_link, None)
        self.assertEqual(
            self.resolved_test_link.url,
            reverse(
                viewname=self.test_link.view, kwargs={
                    'workflow_runtime_proxy_id': self.test_workflow_runtime_proxy.pk
                }
            )
        )
