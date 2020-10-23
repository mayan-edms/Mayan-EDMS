from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_edited
from ..models import WorkflowState
from ..permissions import permission_workflow_edit, permission_workflow_view

from .literals import (
    TEST_WORKFLOW_STATE_LABEL, TEST_WORKFLOW_STATE_COMPLETION,
)
from .mixins import WorkflowStateViewTestMixin, WorkflowTestMixin


class WorkflowStateViewTestCase(
    EventTestCaseMixin, WorkflowTestMixin, WorkflowStateViewTestMixin,
    GenericViewTestCase
):
    _test_event_object_name = 'test_workflow'

    def test_workflow_state_create_view_no_permission(self):
        self._create_test_workflow()
        self._clear_events()

        response = self._request_test_workflow_state_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowState.objects.count(), 0)
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_create_view_with_access(self):
        self._create_test_workflow()
        self._clear_events()

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
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_state_create_invalid_completion_view_with_access(self):
        self._create_test_workflow()
        self._clear_events()

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
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_state_delete_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

        response = self._request_test_workflow_state_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(WorkflowState.objects.count(), 2)
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_delete_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )

        response = self._request_test_workflow_state_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WorkflowState.objects.count(), 1)
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_state_edit_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

        workflow_state_label = self.test_workflow_state_1.label

        response = self._request_test_workflow_state_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_state_1.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state_1.label, workflow_state_label
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_edit_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

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
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_state_list_view_no_permission(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

        response = self._request_test_workflow_state_list_view()
        self.assertEqual(response.status_code, 404)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_list_view_with_access(self):
        self._create_test_workflow()
        self._create_test_workflow_states()
        self._clear_events()

        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_view
        )

        response = self._request_test_workflow_state_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=self.test_workflow_state_1.label)

        event = self._get_test_object_event()
        self.assertEqual(event, None)
