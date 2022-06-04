from mayan.apps.testing.tests.base import GenericViewTestCase

from ..models import Notification
from ..permissions import permission_events_view

from .mixins import (
    EventObjectTestMixin, EventTestMixin, EventTypeTestMixin,
    NotificationTestMixin, NotificationViewTestMixin
)


class NotificationViewTestCase(
    EventObjectTestMixin, EventTestMixin, EventTypeTestMixin,
    NotificationTestMixin, NotificationViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_event_type()
        self._create_test_object_with_event_type_and_permission()
        self._create_test_event(target=self._test_object)
        self._create_test_notification()

    def test_notification_list_view_no_permission(self):
        response = self._request_test_notification_list_view()
        self.assertNotContains(
            response=response,
            text=self._test_notification.get_event_type().label,
            status_code=200
        )

    def test_notification_list_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_events_view
        )
        response = self._request_test_notification_list_view()
        self.assertContains(
            response=response,
            text=self._test_notification.get_event_type().label,
            status_code=200
        )

    def test_notification_mark_read_all_view_no_permission(self):
        notification_count = Notification.objects.get_unread().count()

        response = self._request_test_notification_mark_read_all_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Notification.objects.get_unread().count(),
            notification_count
        )

    def test_notification_mark_read_all_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_events_view
        )

        notification_count = Notification.objects.get_unread().count()

        response = self._request_test_notification_mark_read_all_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Notification.objects.get_unread().count(),
            notification_count - 1
        )

    def test_notification_mark_read_view_no_permission(self):
        notification_count = Notification.objects.get_unread().count()

        response = self._request_test_notification_mark_read()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            Notification.objects.get_unread().count(),
            notification_count
        )

    def test_notification_mark_read_view_with_access(self):
        self.grant_access(
            obj=self._test_object, permission=permission_events_view
        )
        notification_count = Notification.objects.get_unread().count()

        response = self._request_test_notification_mark_read()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Notification.objects.get_unread().count(),
            notification_count - 1
        )
