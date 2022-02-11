from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_workflow_template_edited
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_state_mixins import (
    WorkflowTemplateStateActionAPIViewTestMixin,
    WorkflowTemplateStateActionTestMixin
)


class WorkflowTemplateStateActionsAPIViewTestCase(
    WorkflowTemplateStateActionAPIViewTestMixin,
    WorkflowTemplateStateActionTestMixin, WorkflowTemplateTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()

    def test_workflow_template_state_action_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template_state.actions.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_workflow_template.refresh_from_db()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_state_action
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_state_action_delete_api_view_no_permission(self):
        self._create_test_workflow_template_state_action()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template_state.actions.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_delete_api_view_with_access(self):
        self._create_test_workflow_template_state_action()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template_state.actions.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_state_action_detail_api_view_no_permission(self):
        self._create_test_workflow_template_state_action()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_detail_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_detail_api_view_with_access(self):
        self._create_test_workflow_template_state_action()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_workflow_template_state_action.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_list_api_view_no_permission(self):
        self._create_test_workflow_template_state_action()

        self._clear_events()

        response = self._request_test_workflow_template_state_action_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_list_api_view_with_access(self):
        self._create_test_workflow_template_state_action()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_workflow_template_state_action.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_edit_api_view_via_patch_no_permission(self):
        self._create_test_workflow_template_state_action()

        test_workflow_template_state_action_label = self.test_workflow_template_state_action.label

        self._clear_events()

        response = self._request_test_workflow_template_state_action_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_state_action.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_state_action.label,
            test_workflow_template_state_action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_edit_api_view_via_patch_with_access(self):
        self._create_test_workflow_template_state_action()

        test_workflow_template_state_action_label = self.test_workflow_template_state_action.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template_state_action.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_state_action.label,
            test_workflow_template_state_action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_state_action
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_state_action_edit_api_view_via_put_no_permission(self):
        self._create_test_workflow_template_state_action()

        test_workflow_template_state_action_label = self.test_workflow_template_state_action.label

        self._clear_events()

        response = self._request_test_workflow_template_state_action_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_state_action.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_state_action.label,
            test_workflow_template_state_action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_action_edit_api_view_via_put_with_access(self):
        self._create_test_workflow_template_state_action()

        test_workflow_template_state_action_label = self.test_workflow_template_state_action.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_action_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template_state_action.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_state_action.label,
            test_workflow_template_state_action_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_state_action
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)
