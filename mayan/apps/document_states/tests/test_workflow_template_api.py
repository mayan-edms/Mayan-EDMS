from rest_framework import status

from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_workflow_template_created, event_workflow_template_edited
from ..models import Workflow
from ..permissions import (
    permission_workflow_template_create, permission_workflow_template_delete,
    permission_workflow_template_edit, permission_workflow_template_view
)

from .literals import (
    TEST_WORKFLOW_TEMPLATE_LABEL, TEST_WORKFLOW_TEMPLATE_STATE_LABEL,
    TEST_WORKFLOW_TEMPLATE_TRANSITION_LABEL
)

from .mixins import (
    WorkflowTemplateStateAPIViewTestMixin,
    WorkflowTemplateDocumentTypeAPIViewMixin,
    WorkflowTemplateAPIViewTestMixin, WorkflowTemplateTestMixin,
    WorkflowTemplateTransitionAPIViewTestMixin,
    WorkflowTransitionFieldAPIViewTestMixin,
    WorkflowTransitionFieldTestMixin
)


class WorkflowTemplateAPIViewTestCase(
    DocumentTestMixin, WorkflowTemplateAPIViewTestMixin,
    WorkflowTemplateTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_workflow_template_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_template_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Workflow.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_workflow_template_create)

        self._clear_events()

        response = self._request_test_workflow_template_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['label'], TEST_WORKFLOW_TEMPLATE_LABEL
        )

        self.assertEqual(Workflow.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_created.id)

    def test_workflow_template_delete_api_view_no_permission(self):
        self._create_test_workflow_template()

        self._clear_events()

        response = self._request_test_workflow_template_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Workflow.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_delete_api_view_with_permission(self):
        self._create_test_workflow_template()
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_delete
        )

        self._clear_events()

        response = self._request_test_workflow_template_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Workflow.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_detail_api_view_no_permission(self):
        self._create_test_workflow_template()

        self._clear_events()

        response = self._request_test_workflow_template_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse('label' in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_detail_api_view_with_access(self):
        self._create_test_workflow_template()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['label'], self.test_workflow_template.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_image_api_view_no_permission(self):
        self._create_test_workflow_template(add_test_document_type=True)

        self._clear_events()

        response = self._request_test_workflow_template_image_view_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_image_api_view_with_access(self):
        self._create_test_workflow_template(add_test_document_type=True)

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_image_view_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_list_api_view_no_permission(self):
        self._create_test_workflow_template()

        self._clear_events()

        response = self._request_test_workflow_template_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_list_api_view_with_access(self):
        self._create_test_workflow_template()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_workflow_template.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_edit_via_patch_api_view_no_permission(self):
        self._create_test_workflow_template()

        test_workflow_template_label = self.test_workflow_template.label

        self._clear_events()

        response = self._request_test_workflow_template_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template.label, test_workflow_template_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_edit_via_patch_api_view_with_access(self):
        self._create_test_workflow_template()

        test_workflow_template_label = self.test_workflow_template.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template.label,
            test_workflow_template_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_edit_via_put_api_view_no_permission(self):
        self._create_test_workflow_template()

        test_workflow_template_label = self.test_workflow_template.label

        self._clear_events()

        response = self._request_test_workflow_template_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template.label, test_workflow_template_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_edit_via_put_api_view_with_access(self):
        self._create_test_workflow_template()

        test_workflow_template_label = self.test_workflow_template.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_template_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template.label,
            test_workflow_template_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)


class WorkflowTemplateDocumentTypeAPIViewTestCase(
    DocumentTestMixin, WorkflowTemplateDocumentTypeAPIViewMixin,
    WorkflowTemplateTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()

    def test_workflow_template_document_type_add_api_view_no_permission(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_api_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_api_view_with_workflow_template_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_add_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_template_permission_list_api_view_no_permission(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_permission_list_api_view_with_document_type_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_permission_list_api_view_with_workflow_template_access(self):
        self.test_workflow_template.document_types.add(self.test_document_type)

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_permission_list_api_view_with_full_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_template_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_type.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_remove_api_view_no_permission(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_remove_api_view_with_document_type_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_remove_api_view_with_workflow_template_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_template_document_type_remove_api_view_with_full_access(self):
        self.test_workflow_template.document_types.add(
            self.test_document_type
        )

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        test_workflow_template_document_types_count = self.test_workflow_template.document_types.count()

        self._clear_events()

        response = self._request_test_workflow_template_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template.refresh_from_db()

        self.assertEqual(
            self.test_workflow_template.document_types.count(),
            test_workflow_template_document_types_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)


class WorkflowTemplateStatesAPIViewTestCase(
    DocumentTestMixin, WorkflowTemplateStateAPIViewTestMixin,
    WorkflowTemplateTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_workflow_template()

    def test_workflow_state_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_workflow_state_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template.states.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_state_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template.states.first().label,
            TEST_WORKFLOW_TEMPLATE_STATE_LABEL
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_state
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_state_delete_api_view_no_permission(self):
        self._create_test_workflow_template_state()

        self._clear_events()

        response = self._request_test_workflow_state_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template.states.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_delete_api_view_with_access(self):
        self._create_test_workflow_template_state()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_state_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.test_workflow_template.refresh_from_db()
        self.assertEqual(self.test_workflow_template.states.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_state_detail_api_view_no_permission(self):
        self._create_test_workflow_template_state()

        self._clear_events()

        response = self._request_test_workflow_state_detail_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_detail_api_view_with_access(self):
        self._create_test_workflow_template_state()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_state_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_workflow_template_state.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_list_api_view_no_permission(self):
        self._create_test_workflow_template_state()

        self._clear_events()

        response = self._request_test_workflow_state_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_list_api_view_with_access(self):
        self._create_test_workflow_template_state()

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_view
        )

        self._clear_events()

        response = self._request_test_workflow_state_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_workflow_template_state.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_edit_api_view_via_patch_no_permission(self):
        self._create_test_workflow_template_state()

        test_workflow_template_state_label = self.test_workflow_template_state.label

        self._clear_events()

        response = self._request_test_workflow_state_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_state.label,
            test_workflow_template_state_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_edit_api_view_via_patch_with_access(self):
        self._create_test_workflow_template_state()

        test_workflow_template_state_label = self.test_workflow_template_state.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_state_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template_state.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_state.label,
            test_workflow_template_state_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_state
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)

    def test_workflow_state_edit_api_view_via_put_no_permission(self):
        self._create_test_workflow_template_state()

        test_workflow_template_state_label = self.test_workflow_template_state.label

        self._clear_events()

        response = self._request_test_workflow_state_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_workflow_template_state.refresh_from_db()
        self.assertEqual(
            self.test_workflow_template_state.label,
            test_workflow_template_state_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_workflow_state_edit_api_view_via_put_with_access(self):
        self._create_test_workflow_template_state()

        test_workflow_template_state_label = self.test_workflow_template_state.label

        self.grant_access(
            obj=self.test_workflow_template,
            permission=permission_workflow_template_edit
        )

        self._clear_events()

        response = self._request_test_workflow_state_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_workflow_template_state.refresh_from_db()
        self.assertNotEqual(
            self.test_workflow_template_state.label,
            test_workflow_template_state_label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(
            events[0].action_object, self.test_workflow_template_state
        )
        self.assertEqual(events[0].target, self.test_workflow_template)
        self.assertEqual(events[0].verb, event_workflow_template_edited.id)


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
