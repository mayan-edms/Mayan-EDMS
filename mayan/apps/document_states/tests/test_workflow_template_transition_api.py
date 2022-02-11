from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_workflow_template_edited
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .literals import TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_transition_mixins import (
    WorkflowTemplateTransitionAPIViewTestMixin
)


class WorkflowTemplateTransitionAPIViewTestCase(
    WorkflowTemplateTestMixin, WorkflowTemplateTransitionAPIViewTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()

    def test_workflow_template_transition_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_transition_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(self._test_workflow_template.transitions.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_create_api_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template.transitions.first().label,
            TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_create_api_view_invalid_states_with_access(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_delete_api_view_no_permission(self):
        self._create_test_workflow_template_transition()

        self._clear_events()

        response = self._request_test_workflow_template_transition_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(self._test_workflow_template.transitions.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_delete_api_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(self._test_workflow_template.transitions.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_detail_api_view_no_permission(self):
        self._create_test_workflow_template_transition()

        self._clear_events()

        response = self._request_test_workflow_template_transition_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_detail_api_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self._test_workflow_template_transition.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_list_api_view_no_permission(self):
        self._create_test_workflow_template_transition()

        self._clear_events()

        response = self._request_test_workflow_template_transition_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_list_api_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self._test_workflow_template_transition.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_api_view_via_patch_no_permission(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self._test_workflow_template_transition.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self._test_workflow_template_transition.origin_state,
            self._test_workflow_template_states[0]
        )
        self.assertEqual(
            self._test_workflow_template_transition.destination_state,
            self._test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_api_view_via_patch_with_access(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self._test_workflow_template_transition.label

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_workflow_template_transition.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self._test_workflow_template_transition.origin_state,
            self._test_workflow_template_states[1]
        )
        self.assertEqual(
            self._test_workflow_template_transition.destination_state,
            self._test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_edit_api_view_via_put_no_permission(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self._test_workflow_template_transition.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_put_api_view_via()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self._test_workflow_template_transition.origin_state,
            self._test_workflow_template_states[0]
        )
        self.assertEqual(
            self._test_workflow_template_transition.destination_state,
            self._test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_api_view_via_put_with_access(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self._test_workflow_template_transition.label

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_put_api_view_via()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_workflow_template_transition.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self._test_workflow_template_transition.origin_state,
            self._test_workflow_template_states[1]
        )
        self.assertEqual(
            self._test_workflow_template_transition.destination_state,
            self._test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)
