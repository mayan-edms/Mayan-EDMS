from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_workflow_edited
from ..permissions import permission_workflow_edit

from .literals import TEST_WORKFLOW_STATE_ACTION_DOTTED_PATH
from .mixins import (
    WorkflowStateActionTestMixin, WorkflowStateActionViewTestMixin,
    WorkflowTestMixin
)


class WorkflowStateActionViewTestCase(
    EventTestCaseMixin, WorkflowStateActionTestMixin,
    WorkflowStateActionViewTestMixin, WorkflowTestMixin, GenericViewTestCase
):
    _test_event_object_name = 'test_workflow'

    def setUp(self):
        super().setUp()
        self._create_test_workflow()
        self._create_test_workflow_state()

    def test_workflow_state_action_create_get_view_no_permission(self):
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_get_view(
            class_path=TEST_WORKFLOW_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 404)

        self.test_workflow_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_action_create_get_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_get_view(
            class_path=TEST_WORKFLOW_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 200)

        self.test_workflow_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_action_create_post_view_no_permission(self):
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path=TEST_WORKFLOW_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 404)

        self.test_workflow_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_action_create_post_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path=TEST_WORKFLOW_STATE_ACTION_DOTTED_PATH
        )
        self.assertEqual(response.status_code, 302)

        self.test_workflow_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count + 1
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_state_action_delete_view_no_permission(self):
        self._create_test_workflow_state_action()
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_worflow_template_state_action_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_action_delete_view_with_access(self):
        self._create_test_workflow_state_action()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_worflow_template_state_action_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count - 1
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_state_action_edit_view_no_permission(self):
        self._create_test_workflow_state_action()
        action_label = self.test_workflow_state_action.label
        self._clear_events()

        response = self._request_test_worflow_template_state_action_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_state_action.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state_action.label, action_label
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_action_edit_view_with_access(self):
        self._create_test_workflow_state_action()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        action_label = self.test_workflow_state_action.label
        self._clear_events()

        response = self._request_test_worflow_template_state_action_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_state_action.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_state_action.label, action_label
        )
        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_workflow_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_workflow_state_action_list_view_no_permission(self):
        self._create_test_workflow_state_action()
        self._clear_events()

        response = self._request_test_worflow_template_state_action_list_view()
        self.assertNotContains(
            response=response, text=self.TestWorkflowAction.label,
            status_code=404
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_action_list_view_with_access(self):
        self._create_test_workflow_state_action()
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        self._clear_events()

        response = self._request_test_worflow_template_state_action_list_view()
        self.assertContains(
            response=response, text=self.TestWorkflowAction.label,
            status_code=200
        )

    def test_workflow_state_action_selection_view_no_permission(self):
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_workflow_state_action_selection_view()
        self.assertEqual(response.status_code, 404)

        self.test_workflow_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_workflow_state_action_selection_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow, permission=permission_workflow_edit
        )
        action_count = self.test_workflow_state.actions.count()
        self._clear_events()

        response = self._request_test_workflow_state_action_selection_view()
        self.assertEqual(response.status_code, 302)

        self.test_workflow_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_state.actions.count(), action_count
        )
        event = self._get_test_object_event()
        self.assertEqual(event, None)
