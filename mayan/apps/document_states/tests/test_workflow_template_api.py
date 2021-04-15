from rest_framework import status

from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_workflow_template_created, event_workflow_template_edited
)
from ..models import Workflow
from ..permissions import (
    permission_workflow_template_create, permission_workflow_template_delete,
    permission_workflow_template_edit, permission_workflow_template_view
)

from .literals import TEST_WORKFLOW_TEMPLATE_LABEL
from .mixins.workflow_template_mixins import (
    WorkflowTemplateAPIViewTestMixin,
    WorkflowTemplateDocumentTypeAPIViewMixin,
    WorkflowTemplateTestMixin
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
