from mayan.apps.testing.tests.base import BaseTestCase

from ..models import EventSubscription, ObjectEventSubscription

from .mixins import (
    EventObjectTestMixin, EventTestMixin, EventTypeTestMixin,
    NotificationTestMixin
)


class EventTypeNotificationModelTestCase(
    EventObjectTestMixin, EventTestMixin, EventTypeTestMixin,
    NotificationTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()

        self._create_test_event_type()
        self._create_test_object_with_event_type_and_permission()

        EventSubscription.objects.create(
            stored_event_type=self._test_event_type.get_stored_event_type(),
            user=self._test_case_user
        )

    def test_event_type_notification_creation(self):
        test_notification_count = self._test_case_user.notifications.count()

        self._create_test_event(target=self._test_object)
        self.assertEqual(
            self._test_case_user.notifications.count(),
            test_notification_count + 1
        )


class ObjectEventNotificationModelTestCase(
    EventObjectTestMixin, EventTestMixin, EventTypeTestMixin,
    NotificationTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()

        self._create_test_event_type()
        self._create_test_object_with_event_type_and_permission()

        ObjectEventSubscription.objects.create(
            content_object=self._test_object,
            stored_event_type=self._test_event_type.get_stored_event_type(),
            user=self._test_case_user
        )

    def test_object_notification_creation(self):
        test_notification_count = self._test_case_user.notifications.count()

        self._create_test_event(target=self._test_object)
        self.assertEqual(
            self._test_case_user.notifications.count(),
            test_notification_count + 1
        )
