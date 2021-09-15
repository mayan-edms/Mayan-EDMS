from rest_framework import status

from mayan.apps.documents.tests.base import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_smart_link_edited
from ..models import SmartLinkCondition
from ..permissions import (
    permission_smart_link_edit, permission_smart_link_view
)

from .literals import (
    TEST_SMART_LINK_CONDITION_EXPRESSION,
    TEST_SMART_LINK_CONDITION_EXPRESSION_EDITED,
    TEST_SMART_LINK_CONDITION_OPERATOR
)
from .mixins import SmartLinkConditionAPIViewTestMixin, SmartLinkTestMixin


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
