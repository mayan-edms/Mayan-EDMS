from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.events.tests.mixins import EventTypeTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_workflow_template_edited
from ..permissions import (
    permission_workflow_template_edit, permission_workflow_template_view
)

from .mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from .mixins.workflow_template_transition_mixins import (
    WorkflowTemplateTransitionTriggerAPIViewTestMixin,
    WorkflowTemplateTransitionTriggerTestMixin
)


class WorkflowTemplateTransitionTriggersAPIViewTestCase(
    DocumentTestMixin, EventTypeTestMixin,
    WorkflowTemplateTransitionTriggerAPIViewTestMixin,
    WorkflowTemplateTransitionTriggerTestMixin, WorkflowTemplateTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()
        self._create_test_workflow_template(add_test_document_type=True)
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_state()
        self._create_test_workflow_template_transition()
        self._create_test_workflow_template_transition()
        self._create_test_event_type()

    def test_workflow_template_transition_trigger_create_api_view_no_permission(self):
        test_workflow_template_transition_trigger_count = self._test_workflow_template_transition.trigger_events.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.trigger_events.count(),
            test_workflow_template_transition_trigger_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_create_api_view_with_access(self):
        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_transition_trigger_count = self._test_workflow_template_transition.trigger_events.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self._test_workflow_template_transition.trigger_events.count(),
            test_workflow_template_transition_trigger_count + 1
        )

        self._test_workflow_template.refresh_from_db()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object,
            self._test_workflow_template_transition_trigger
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_trigger_delete_api_view_no_permission(self):
        self._create_test_workflow_template_transition_trigger()

        test_workflow_template_transition_trigger_count = self._test_workflow_template_transition.trigger_events.count()

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.trigger_events.count(),
            test_workflow_template_transition_trigger_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_delete_api_view_with_access(self):
        self._create_test_workflow_template_transition_trigger()

        test_workflow_template_transition_trigger_count = self._test_workflow_template_transition.trigger_events.count()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self._test_workflow_template.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition.trigger_events.count(),
            test_workflow_template_transition_trigger_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_trigger_detail_api_view_no_permission(self):
        self._create_test_workflow_template_transition_trigger()

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_detail_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_detail_api_view_with_access(self):
        self._create_test_workflow_template_transition_trigger()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self._test_workflow_template_transition_trigger.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_list_api_view_no_permission(self):
        self._create_test_workflow_template_transition_trigger()

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_list_api_view_with_access(self):
        self._create_test_workflow_template_transition_trigger()

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self._test_workflow_template_transition_trigger.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_edit_api_view_via_patch_no_permission(self):
        self._create_test_workflow_template_transition_trigger()
        self._create_test_event_type()

        test_workflow_template_transition_trigger_event_type = self._test_workflow_template_transition_trigger.event_type

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_transition_trigger.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition_trigger.event_type,
            test_workflow_template_transition_trigger_event_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_edit_api_view_via_patch_with_access(self):
        self._create_test_workflow_template_transition_trigger()
        self._create_test_event_type()

        test_workflow_template_transition_trigger_event_type = self._test_workflow_template_transition_trigger.event_type

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_workflow_template_transition_trigger.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_transition_trigger.event_type,
            test_workflow_template_transition_trigger_event_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition_trigger
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_transition_trigger_edit_api_view_via_put_no_permission(self):
        self._create_test_workflow_template_transition_trigger()
        self._create_test_event_type()

        test_workflow_template_transition_trigger_event_type = self._test_workflow_template_transition_trigger.event_type

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self._test_workflow_template_transition_trigger.refresh_from_db()
        self.assertEqual(
            self._test_workflow_template_transition_trigger.event_type,
            test_workflow_template_transition_trigger_event_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_transition_trigger_edit_api_view_via_put_with_access(self):
        self._create_test_workflow_template_transition_trigger()
        self._create_test_event_type()

        test_workflow_template_transition_trigger_event_type = self._test_workflow_template_transition_trigger.event_type

        self.grant_access(
            obj=self._test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_transition_trigger_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self._test_workflow_template_transition_trigger.refresh_from_db()
        self.assertNotEqual(
            self._test_workflow_template_transition_trigger.event_type,
            test_workflow_template_transition_trigger_event_type
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self._test_workflow_template_transition_trigger
        )
        self.assertEqual(events[0].target, self._test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)
