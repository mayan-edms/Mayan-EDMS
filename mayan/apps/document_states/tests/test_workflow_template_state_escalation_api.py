from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_workflow_template_edited
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_state_escalation_mixins import (
    WorkflowTemplateStateEscalationAPIViewTestMixin,
    WorkflowTemplateStateEscalationTestMixin
)


class WorkflowTemplateStateEscalationsAPIViewTestCase(
    WorkflowTemplateStateEscalationAPIViewTestMixin,
    WorkflowTemplateStateEscalationTestMixin, WorkflowTemplateTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_transition()

    def test_workflow_template_state_escalation_create_api_view_no_permission(self):
        test_workflow_template_state_count = self._test_workflow_template_states[0].escalations.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_states[0].escalations.count(),
            test_workflow_template_state_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_create_api_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_state_count = self._test_workflow_template_states[0].escalations.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_states[0].escalations.count(),
            test_workflow_template_state_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_estate_escalation
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_state_escalation_create_api_view_validation_with_access(self):
        self._create_test_workflow_template_state_escalation()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_state_count = self._test_workflow_template_states[0].escalations.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_states[0].escalations.count(),
            test_workflow_template_state_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_delete_api_view_no_permission(self):
        self._create_test_workflow_template_state_escalation()

        test_workflow_template_state_count = self._test_workflow_template_states[0].escalations.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_states[0].escalations.count(),
            test_workflow_template_state_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_delete_api_view_with_access(self):
        self._create_test_workflow_template_state_escalation()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_state_count = self._test_workflow_template_states[0].escalations.count()

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_states[0].escalations.count(),
            test_workflow_template_state_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_state_escalation_detail_api_view_no_permission(self):
        self._create_test_workflow_template_state_escalation()

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_detail_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_detail_api_view_with_access(self):
        self._create_test_workflow_template_state_escalation()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self._test_workflow_template_state_escalation.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_list_api_view_no_permission(self):
        self._create_test_workflow_template_state_escalation()

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_list_api_view_with_access(self):
        self._create_test_workflow_template_state_escalation()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self._test_workflow_template_state_escalation.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_edit_api_view_via_patch_no_permission(self):
        self._create_test_workflow_template_state_escalation()

        test_workflow_template_state_escalation_amount = self._test_workflow_template_state_escalation.amount

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_state_escalation.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state_escalation.amount,
            test_workflow_template_state_escalation_amount
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_edit_api_view_via_patch_with_access(self):
        self._create_test_workflow_template_state_escalation()

        test_workflow_template_state_escalation_amount = self._test_workflow_template_state_escalation.amount

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_workflow_template_state_escalation.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_state_escalation.amount,
            test_workflow_template_state_escalation_amount
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_state_escalation
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_state_escalation_edit_api_view_via_put_no_permission(self):
        self._create_test_workflow_template_state_escalation()

        test_workflow_template_state_escalation_amount = self._test_workflow_template_state_escalation.amount
        test_workflow_template_state_escalation_transition = self._test_workflow_template_state_escalation.transition

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_state_escalation.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_state_escalation.amount,
            test_workflow_template_state_escalation_amount
        )
        self.assertEqual(
            self._test_workflow_template_state_escalation.transition,
            test_workflow_template_state_escalation_transition
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_state_escalation_edit_api_view_via_put_with_access(self):
        self._create_test_workflow_template_state_escalation()

        test_workflow_template_state_escalation_amount = self._test_workflow_template_state_escalation.amount
        test_workflow_template_state_escalation_transition = self._test_workflow_template_state_escalation.transition

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_state_escalation_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_workflow_template_state_escalation.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_state_escalation.amount,
            test_workflow_template_state_escalation_amount
        )
        self.assertNotEqual(
            self._test_workflow_template_state_escalation.transition,
            test_workflow_template_state_escalation_transition
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_state_escalation
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)
