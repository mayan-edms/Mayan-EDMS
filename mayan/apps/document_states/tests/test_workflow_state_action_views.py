from __future__ import unicode_literals

from mayan.apps.common.tests import GenericViewTestCase

from ..permissions import permission_workflow_edit

from .mixins import WorkflowStateActionTestMixin, WorkflowTestMixin


class WorkflowStateActionViewTestCase(WorkflowStateActionTestMixin, WorkflowTestMixin, GenericViewTestCase):
    def setUp(self):
        super(WorkflowStateActionViewTestCase, self).setUp()
        self._create_test_workflow()
        self._create_test_workflow_state()

    def _request_test_document_state_action_view(self):
        return self.get(
            viewname='document_states:setup_workflow_state_action_list',
            kwargs={'pk': self.test_workflow_state.pk}
        )

    def test_workflow_state_action_list_view_no_permission(self):
        self._create_test_workflow_state_action()

        response = self._request_test_document_state_action_view()
        self.assertNotContains(
            response=response, text=self.TestWorkflowAction.label,
            status_code=200
        )

    def test_workflow_state_action_list_view_with_access(self):
        self._create_test_workflow_state_action()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_document_state_action_view()
        self.assertContains(
            response=response, text=self.TestWorkflowAction.label,
            status_code=200
        )
