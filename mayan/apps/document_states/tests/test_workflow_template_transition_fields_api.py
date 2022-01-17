from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_workflow_template_edited
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_transition_mixins import (
    WorkflowTransitionFieldAPIViewTestMixin, WorkflowTransitionFieldTestMixin
)


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
        transition_field_count = self._test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_create_api_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        transition_field_count = self._test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self._test_workflow_template_transition.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            transition_field_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_transition_field
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_field_delete_api_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        transition_field_count = self._test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            transition_field_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_delete_api_view_with_access(self):
        self._create_test_workflow_template_transition_field()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        transition_field_count = self._test_workflow_template_transition.fields.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self._test_workflow_template_transition.fields.count(),
            transition_field_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self._test_workflow_template)
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
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'],
            self._test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_edit_via_patch_api_view_no_permission(self):
        self._create_test_workflow_template_transition_field()

        transition_field_label = self._test_workflow_template_transition_field.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_transition_field.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition_field.label, transition_field_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_field_edit_via_patch_api_view_with_access(self):
        self._create_test_workflow_template_transition_field()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        transition_field_label = self._test_workflow_template_transition_field.label

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_workflow_template_transition_field.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_transition_field.label, transition_field_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition_field
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
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
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_field_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self._test_workflow_template_transition_field.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
