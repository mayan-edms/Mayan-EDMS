from __future__ import unicode_literals

from mayan.apps.common.tests import GenericViewTestCase

from ..models import WorkflowState
from ..permissions import permission_workflow_edit, permission_workflow_view

from .literals import (
    TEST_WORKFLOW_STATE_LABEL, TEST_WORKFLOW_STATE_COMPLETION,
)
from .mixins import WorkflowStateViewTestMixin, WorkflowTestMixin


class WorkflowStateViewTestCase(
    WorkflowTestMixin, WorkflowStateViewTestMixin, GenericViewTestCase
):
    def test_create_workflow_state_no_access(self):
        self._create_test_workflow()

        response = self._request_test_workflow_state_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowState.objects.count(), 0)

    def test_create_workflow_state_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_state_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WorkflowState.objects.count(), 1)
        self.assertEqual(
            WorkflowState.objects.all()[0].label, TEST_WORKFLOW_STATE_LABEL
        )
        self.assertEqual(
            WorkflowState.objects.all()[0].completion,
            TEST_WORKFLOW_STATE_COMPLETION
        )

    def test_create_workflow_state_invalid_completion_with_access(self):
        self._create_test_workflow()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_state_create_view(
            extra_data={'completion': ''}
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WorkflowState.objects.count(), 1)
        self.assertEqual(
            WorkflowState.objects.all()[0].label, TEST_WORKFLOW_STATE_LABEL
        )
        self.assertEqual(
            WorkflowState.objects.all()[0].completion, 0
        )

    def test_delete_workflow_state_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        response = self._request_test_workflow_state_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowState.objects.count(), 2)

    def test_delete_workflow_state_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_state_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WorkflowState.objects.count(), 1)

    def test_edit_workflow_state_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        workflow_state_label = self.test_workflow_state_1.label

        response = self._request_test_workflow_state_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_state_1.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state_1.label, workflow_state_label
        )

    def test_edit_workflow_state_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        workflow_state_label = self.test_workflow_state_1.label

        response = self._request_test_workflow_state_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_state_1.refresh_from_db()
        self.assertNotEquals(
            self.test_workflow_state_1.label, workflow_state_label
        )

    def test_workflow_state_list_no_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        response = self._request_test_workflow_state_list_view()
        self.assertEqual(response.status_code, 404)

    def test_workflow_state_list_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_state_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=self.test_workflow_state_1.label)
