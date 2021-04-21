from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_workflow_template_edited
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .literals import TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_transition_mixins import (
    WorkflowTemplateTransitionAPIViewTestMixin,
    WorkflowTransitionFieldAPIViewTestMixin, WorkflowTransitionFieldTestMixin
)


class WorkflowTemplateTransitionAPIViewTestCase(
    DocumentTestMixin, WorkflowTemplateTestMixin,
    WorkflowTemplateTransitionAPIViewTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()

    def test_workflow_template_transition_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_transition_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template.transitions.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template.transitions.first().label,
            TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_transition
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_create_api_view_invalid_states_with_access(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()

        self.grant_access(
            obj=self.test_workflow_template,
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

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template.transitions.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_delete_api_view_with_access(self):
        self._create_test_workflow_template_transition()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template.transitions.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_workflow_template)
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
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_workflow_template_transition.pk
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
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_workflow_template_transition.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_api_view_via_patch_no_permission(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self.test_workflow_template_transition.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self.test_workflow_template_transition.origin_state,
            self.test_workflow_template_states[0]
        )
        self.assertEqual(
            self.test_workflow_template_transition.destination_state,
            self.test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_api_view_via_patch_with_access(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self.test_workflow_template_transition.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template_transition.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self.test_workflow_template_transition.origin_state,
            self.test_workflow_template_states[1]
        )
        self.assertEqual(
            self.test_workflow_template_transition.destination_state,
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_transition
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_edit_api_view_via_put_no_permission(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self.test_workflow_template_transition.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_put_api_view_via()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self.test_workflow_template_transition.origin_state,
            self.test_workflow_template_states[0]
        )
        self.assertEqual(
            self.test_workflow_template_transition.destination_state,
            self.test_workflow_template_states[1]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_edit_api_view_via_put_with_access(self):
        self._create_test_workflow_template_transition()

        test_workflow_template_transition_label = self.test_workflow_template_transition.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_edit_put_api_view_via()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_workflow_template_transition.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_transition.label,
            test_workflow_template_transition_label
        )
        self.assertEqual(
            self.test_workflow_template_transition.origin_state,
            self.test_workflow_template_states[1]
        )
        self.assertEqual(
            self.test_workflow_template_transition.destination_state,
            self.test_workflow_template_states[0]
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_transition
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)


class WorkflowTemplateTransitionFieldAPIViewTestCase(
    WorkflowTransitionFieldAPIViewTestMixin, DocumentTestMixin,
    WorkflowTemplateTestMixin, WorkflowTransitionFieldTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()

    def test_workflow_template_transition_field_create_api_view_no_permission(self):
        transition_field_count = self.test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        transition_field_count = self.test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            transition_field_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object,
            self.test_workflow_template_transition_field
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_delete_api_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        transition_field_count = self.test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_delete_api_view_with_access(self):
        self._create_test_workflow_template_transition_field()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        transition_field_count = self.test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_workflow_template_transition.fields.count(),
            transition_field_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_detail_api_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('results' in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_detail_api_view_with_access(self):
        self._create_test_workflow_template_transition_field()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'],
            self.test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_edit_via_patch_api_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        transition_field_label = self.test_workflow_template_transition_field.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_transition_field.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_transition_field.label, transition_field_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_edit_via_patch_api_view_with_access(self):
        self._create_test_workflow_template_transition_field()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        transition_field_label = self.test_workflow_template_transition_field.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template_transition_field.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_transition_field.label, transition_field_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_transition_field
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_list_api_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('results' in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_list_api_view_with_access(self):
        self._create_test_workflow_template_transition_field()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
