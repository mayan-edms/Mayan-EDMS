from rest_framework import status

from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view,
    permission_document_view
)
from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_smart_link_created, event_smart_link_edited
from ..models import SmartLink, SmartLinkCondition
from ..permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

from .literals import (
    TEST_SMART_LINK_CONDITION_EXPRESSION,
    TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED,
    TEST_SMART_LINK_CONDITION_OPERATOR, TEST_SMART_LINK_LABEL_EDITED,
    TEST_SMART_LINK_LABEL
)
from .mixins import (
    ResolvedSmartLinkAPIViewTestMixin, SmartLinkAPIViewTestMixin,
    SmartLinkConditionAPIViewTestMixin, SmartLinkDocumentTypeAPIViewTestMixin,
    SmartLinkTestMixin
)


class ResolvedSmartLinkAPIViewTestCase(
    DocumentTestMixin, SmartLinkTestMixin,
    ResolvedSmartLinkAPIViewTestMixin, BaseAPITestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_smart_link(add_test_document_type=True)
        self._create_test_smart_link_condition()

    def test_resolved_smart_link_detail_api_view_no_permission(self):
        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resolved_smart_link_detail_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resolved_smart_link_detail_api_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resolved_smart_link_detail_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_resolved_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['label'], TEST_SMART_LINK_LABEL
        )

    def test_resolved_smart_link_list_api_view_no_permission(self):
        response = self._request_resolved_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse('results' in response.data)

    def test_resolved_smart_link_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_resolved_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

    def test_resolved_smart_link_list_api_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )
        response = self._request_resolved_smart_link_list_api_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse('results' in response.data)

    def test_resolved_smart_link_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_resolved_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], TEST_SMART_LINK_LABEL
        )

    def test_resolved_smart_link_document_list_api_view_no_permission(self):
        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resolved_smart_link_document_list_api_view_with_smart_link_access(self):
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resolved_smart_link_document_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        response = self._request_resolved_smart_link_document_list_api_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resolved_smart_link_document_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        response = self._request_resolved_smart_link_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'], self.test_document.label
        )


class SmartLinkAPIViewTestCase(
    SmartLinkTestMixin, SmartLinkAPIViewTestMixin, BaseAPITestCase
):
    def test_smart_link_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_smart_link_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(SmartLink.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_smart_link_create)

        self._clear_events()

        response = self._request_test_smart_link_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        smart_link = SmartLink.objects.first()
        self.assertEqual(response.data['id'], smart_link.pk)
        self.assertEqual(response.data['label'], TEST_SMART_LINK_LABEL)

        self.assertEqual(SmartLink.objects.count(), 1)
        self.assertEqual(smart_link.label, TEST_SMART_LINK_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_created.id)

    def test_smart_link_delete_api_view_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(SmartLink.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_delete_api_view_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_delete
        )

        self._clear_events()

        response = self._request_test_smart_link_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(SmartLink.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_detail_api_view_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertFalse('label' in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_detail_api_view_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        self._clear_events()

        response = self._request_test_smart_link_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['label'], TEST_SMART_LINK_LABEL
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_edit_api_view_via_patch_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(self.test_smart_link.label, TEST_SMART_LINK_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_edit_api_view_via_patch_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_edit_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(
            self.test_smart_link.label, TEST_SMART_LINK_LABEL_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_edit_api_view_via_put_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(self.test_smart_link.label, TEST_SMART_LINK_LABEL)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_edit_api_view_via_put_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_test_smart_link_edit_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_smart_link.refresh_from_db()
        self.assertEqual(
            self.test_smart_link.label, TEST_SMART_LINK_LABEL_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_list_api_view_no_permission(self):
        self._create_test_smart_link()

        self._clear_events()

        response = self._request_test_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_list_api_view_with_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        self._clear_events()

        response = self._request_test_smart_link_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_smart_link.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class SmartLinkConditionAPIViewTestCase(
    DocumentTestMixin, SmartLinkTestMixin,
    SmartLinkConditionAPIViewTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_smart_link(add_test_document_type=True)

    def test_smart_link_condition_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_smart_link_condition_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_smart_link_condition_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        smart_link_condition = SmartLinkCondition.objects.first()
        self.assertEqual(response.data['id'], smart_link_condition.pk)
        self.assertEqual(
            response.data['operator'], TEST_SMART_LINK_CONDITION_OPERATOR
        )

        self.assertEqual(SmartLinkCondition.objects.count(), 1)
        self.assertEqual(
            smart_link_condition.operator, TEST_SMART_LINK_CONDITION_OPERATOR
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_smart_link_condition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_condition_delete_api_view_no_permission(self):
        self._create_test_smart_link_condition()

        self._clear_events()

        response = self._request_smart_link_condition_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(SmartLinkCondition.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_delete_api_view_with_access(self):
        self._create_test_smart_link_condition()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_smart_link_condition_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(SmartLinkCondition.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_condition_detail_api_view_no_permission(self):
        self._create_test_smart_link_condition()

        self._clear_events()

        response = self._request_smart_link_condition_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_detail_api_view_with_access(self):
        self._create_test_smart_link_condition()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        self._clear_events()

        response = self._request_smart_link_condition_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['operator'], TEST_SMART_LINK_CONDITION_OPERATOR
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_edit_via_patch_api_view_no_permission(self):
        self._create_test_smart_link_condition()

        self._clear_events()

        response = self._request_smart_link_condition_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.test_smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_edit_via_patch_api_view_with_access(self):
        self._create_test_smart_link_condition()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_smart_link_condition_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.test_smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_smart_link_condition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_condition_edit_via_put_api_view_no_permission(self):
        self._create_test_smart_link_condition()

        self._clear_events()

        response = self._request_smart_link_condition_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.test_smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_edit_via_put_api_view_with_access(self):
        self._create_test_smart_link_condition()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        self._clear_events()

        response = self._request_smart_link_condition_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_smart_link_condition.refresh_from_db()
        self.assertEqual(
            self.test_smart_link_condition.expression,
            TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self.test_smart_link_condition
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_condition_list_api_view_no_permission(self):
        self._create_test_smart_link_condition()

        self._clear_events()

        response = self._request_smart_link_condition_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_condition_list_api_view_with_access(self):
        self._create_test_smart_link_condition()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        self._clear_events()

        response = self._request_smart_link_condition_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_smart_link_condition.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class SmartLinkDocumentTypeAPIViewTestCase(
    DocumentTestMixin, SmartLinkTestMixin, SmartLinkDocumentTypeAPIViewTestMixin,
    BaseAPITestCase
):
    auto_upload_test_document = False

    def test_smart_link_document_type_add_api_view_no_permission(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_api_view_with_document_type_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_api_view_with_smart_link_access(self):
        self._create_test_smart_link()

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_add_api_view_with_full_access(self):
        self._create_test_smart_link()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_add_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)

    def test_smart_link_permission_list_api_view_no_permission(self):
        self._create_test_smart_link()
        self.test_smart_link.document_types.add(self.test_document_type)

        self._clear_events()

        response = self._request_test_smart_link_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_permission_list_api_view_with_document_type_access(self):
        self._create_test_smart_link()
        self.test_smart_link.document_types.add(self.test_document_type)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_permission_list_api_view_with_smart_link_access(self):
        self._create_test_smart_link()
        self.test_smart_link.document_types.add(self.test_document_type)

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_permission_list_api_view_with_full_access(self):
        self._create_test_smart_link()
        self.test_smart_link.document_types.add(self.test_document_type)

        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_view
        )

        self._clear_events()

        response = self._request_test_smart_link_document_type_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_type.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_remove_api_view_no_permission(self):
        self._create_test_smart_link(add_test_document_type=True)
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_remove_api_view_with_document_type_access(self):
        self._create_test_smart_link(add_test_document_type=True)
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_remove_api_view_with_smart_link_access(self):
        self._create_test_smart_link(add_test_document_type=True)

        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_smart_link_document_type_remove_api_view_with_full_access(self):
        self._create_test_smart_link(add_test_document_type=True)
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_smart_link, permission=permission_smart_link_edit
        )

        test_smart_link_document_types_count = self.test_smart_link.document_types.count()

        self._clear_events()

        response = self._request_test_smart_link_document_type_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_smart_link.refresh_from_db()

        self.assertEqual(
            self.test_smart_link.document_types.count(),
            test_smart_link_document_types_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_smart_link)
        self.assertEqual(events[0].verb, event_smart_link_edited.id)
