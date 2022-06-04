from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_error_log_deleted
from ..permissions import (
    permission_error_log_entry_delete, permission_error_log_entry_view
)

from .mixins import (
    ErrorLogPartitionEntryTestMixin, ErrorLogViewTestMixin,
    GlobalErrorLogViewTestMixin
)


class GlobalErrorLogViewTestCase(
    ErrorLogPartitionEntryTestMixin, GlobalErrorLogViewTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_error_log_object()
        self._create_test_error_log_entry()

    def test_global_error_log_partition_entry_list_view_no_permission(self):
        self._clear_events()

        response = self._request_global_error_log_partition_entry_list_view()
        self.assertNotContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_global_error_log_partition_entry_list_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_error_log_entry_view
        )

        self._clear_events()

        response = self._request_global_error_log_partition_entry_list_view()
        self.assertContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class ErrorLoggingViewTestCase(
    ErrorLogPartitionEntryTestMixin, ErrorLogViewTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_error_log_object()
        self._create_test_error_log_entry()

    def test_object_error_log_view_no_permission(self):
        self._clear_events()

        response = self._request_object_error_log_list_view()
        self.assertNotContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_object_error_log_entry_list_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_error_log_entry_view
        )

        self._clear_events()

        response = self._request_object_error_log_list_view()
        self.assertContains(
            response=response, text=self._test_error_log_entry.text,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_object_error_log_clear_view_no_permission(self):
        self._clear_events()

        response = self._request_object_error_log_clear_view()
        self.assertEqual(response.status_code, 404)

        self.assertNotEqual(self._test_object.error_log.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_object_error_log_clear_view_with_access(self):
        self.grant_access(
            obj=self._test_object,
            permission=permission_error_log_entry_delete
        )

        self._clear_events()

        response = self._request_object_error_log_clear_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self._test_object.error_log.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_object)
        self.assertEqual(events[0].verb, event_error_log_deleted.id)

    def test_object_error_log_entry_delete_view_no_permission(self):
        test_object_error_log_entry_count = self._test_object.error_log.count()

        self._clear_events()

        response = self._request_object_error_log_entry_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self._test_object.error_log.count(),
            test_object_error_log_entry_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_object_error_log_entry_delete_view_with_access(self):
        self.grant_access(
            obj=self._test_object,
            permission=permission_error_log_entry_delete
        )

        test_object_error_log_entry_count = self._test_object.error_log.count()

        self._clear_events()

        response = self._request_object_error_log_entry_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self._test_object.error_log.count(),
            test_object_error_log_entry_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_object)
        self.assertEqual(events[0].verb, event_error_log_deleted.id)
