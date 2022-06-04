from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_error_log_deleted
from ..permissions import (
    permission_error_log_entry_delete, permission_error_log_entry_view
)

from .mixins import (
    ErrorLogPartitionEntryAPIViewTestMixin, ErrorLogPartitionEntryTestMixin
)


class ErrorLogPartitionEntryAPIViewTestCase(
    ErrorLogPartitionEntryTestMixin, ErrorLogPartitionEntryAPIViewTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_error_log_object()
        self._create_test_error_log_entry()

    def test_error_log_delete_api_view_no_permission(self):
        error_log_entry_count = self._test_object.error_log.count()

        self._clear_events()

        response = self._request_test_error_log_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self._test_object.error_log.count(), error_log_entry_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_error_log_delete_api_view_with_access(self):
        self.grant_access(
            self._test_object, permission=permission_error_log_entry_delete
        )

        error_log_entry_count = self._test_object.error_log.count()

        self._clear_events()

        response = self._request_test_error_log_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self._test_object.error_log.count(), error_log_entry_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_object)
        self.assertEqual(events[0].verb, event_error_log_deleted.id)

    def test_error_log_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_error_log_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_error_log_detail_api_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_error_log_entry_view
        )

        self._clear_events()

        response = self._request_test_error_log_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_error_log_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_error_log_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_error_log_list_api_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_error_log_entry_view
        )

        self._clear_events()

        response = self._request_test_error_log_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
