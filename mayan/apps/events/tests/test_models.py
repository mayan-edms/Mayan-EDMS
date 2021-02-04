from mayan.apps.acls.models import AccessControlList
from mayan.apps.testing.tests.base import BaseTestCase

from ..models import EventSubscription, Notification, ObjectEventSubscription
from ..permissions import permission_events_view

from .mixins import NotificationTestMixin


class EventNotificationModelTestCase(NotificationTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_event_type()
        self._create_local_test_user()
        self._create_local_test_object()

    def test_event_notification_single_user_no_permission(self):
        notification_count = Notification.objects.count()

        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )

        self.test_event_type.commit(target=self.test_object)

        self.assertEqual(Notification.objects.count(), notification_count)

    def test_event_notification_single_user_with_access(self):
        notification_count = Notification.objects.count()

        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )

        AccessControlList.objects.grant(
            obj=self.test_object, permission=permission_events_view,
            role=self.test_role
        )

        result = self.test_event_type.commit(target=self.test_object)

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_user)
        self.assertEqual(notification.action, result)

    def test_event_notification_multiple_users_with_user_0_access(self):
        self._create_local_test_user()

        notification_count = Notification.objects.count()

        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_object, permission=permission_events_view,
            role=self.test_roles[0]
        )

        result = self.test_event_type.commit(target=self.test_object)

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_users[0])
        self.assertEqual(notification.action, result)

    def test_event_notification_multiple_users_with_user_1_access(self):
        self._create_local_test_user()

        notification_count = Notification.objects.count()

        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_object, permission=permission_events_view,
            role=self.test_roles[1]
        )

        result = self.test_event_type.commit(target=self.test_object)

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_users[1])
        self.assertEqual(notification.action, result)

    def test_event_notification_multiple_users_with_all_user_access(self):
        self._create_local_test_user()

        notification_count = Notification.objects.count()

        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        EventSubscription.objects.create(
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_object, permission=permission_events_view,
            role=self.test_roles[0]
        )
        AccessControlList.objects.grant(
            obj=self.test_object, permission=permission_events_view,
            role=self.test_roles[1]
        )

        result = self.test_event_type.commit(target=self.test_object)

        self.assertEqual(Notification.objects.count(), notification_count + 2)
        notifications = Notification.objects.all()
        user_pk_list = notifications.values_list('user__id', flat=True)
        self.assertTrue(self.test_users[0].pk in user_pk_list)
        self.assertEqual(notifications[0].action, result)
        self.assertTrue(self.test_users[1].pk in user_pk_list)
        self.assertEqual(notifications[1].action, result)


class ObjectEventNotificationModelTestCase(NotificationTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_event_type()
        self._create_local_test_user()
        self._create_local_test_object()

    def test_object_notification_single_user_no_permission(self):
        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_object,
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )

        self.test_event_type.commit(target=self.test_object)

        self.assertEqual(Notification.objects.count(), notification_count)

    def test_object_notification_single_user_with_access(self):
        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_object,
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )

        AccessControlList.objects.grant(
            obj=self.test_object, permission=permission_events_view,
            role=self.test_role
        )

        result = self.test_event_type.commit(target=self.test_object)

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_user)
        self.assertEqual(notification.action, result)

    def test_object_notification_single_user_and_multiple_objects_with_object_0_access(self):
        self._create_local_test_object()
        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[1],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_role
        )

        result_0 = self.test_event_type.commit(target=self.test_objects[0])
        self.test_event_type.commit(target=self.test_objects[1])

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_user)
        self.assertEqual(notification.action, result_0)

    def test_object_notification_single_user_and_multiple_objects_with_object_0_target_access(self):
        self._create_local_test_object()
        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[1],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_role
        )

        result_0 = self.test_event_type.commit(
            target=self.test_objects[0], action_object=self.test_objects[1]
        )

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_user)
        self.assertEqual(notification.action, result_0)

    def test_object_notification_single_user_and_multiple_objects_with_object_1_action_object_access(self):
        self._create_local_test_object()
        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[1],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_user
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[1], permission=permission_events_view,
            role=self.test_role
        )

        result_0 = self.test_event_type.commit(
            target=self.test_objects[0], action_object=self.test_objects[1]
        )

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_user)
        self.assertEqual(notification.action, result_0)

    def test_object_notification_multiple_users_and_single_object_with_user_0_access(self):
        self._create_local_test_user()

        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_roles[0]
        )

        result_0 = self.test_event_type.commit(target=self.test_objects[0])

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_users[0])
        self.assertEqual(notification.action, result_0)

    def test_object_notification_multiple_users_and_single_object_with_user_1_access(self):
        self._create_local_test_user()

        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_roles[1]
        )

        result_0 = self.test_event_type.commit(target=self.test_objects[0])

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.test_users[1])
        self.assertEqual(notification.action, result_0)

    def test_object_notification_multiple_users_and_single_object_with_both_user_access(self):
        self._create_local_test_user()

        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_roles[0]
        )
        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_roles[1]
        )

        result_0 = self.test_event_type.commit(target=self.test_objects[0])

        self.assertEqual(Notification.objects.count(), notification_count + 2)
        notifications = Notification.objects.all()
        user_pk_list = notifications.values_list('user__id', flat=True)
        self.assertTrue(self.test_users[0].pk in user_pk_list)
        self.assertEqual(notifications[0].action, result_0)
        self.assertTrue(self.test_users[1].pk in user_pk_list)
        self.assertEqual(notifications[1].action, result_0)

    def test_object_notification_multiple_users_and_multiple_object_with_user_0_and_object_0_access(self):
        self._create_local_test_user()
        self._create_local_test_object()

        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[1],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[1],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_roles[0]
        )

        result_0 = self.test_event_type.commit(target=self.test_objects[0])
        self.test_event_type.commit(target=self.test_objects[1])

        self.assertEqual(Notification.objects.count(), notification_count + 1)
        notifications = Notification.objects.all()
        self.assertEqual(notifications[0].user, self.test_users[0])
        self.assertEqual(notifications[0].action, result_0)

    def test_object_notification_multiple_users_and_multiple_object_with_user_0_and_object_0_action_object_access(self):
        self._create_local_test_user()
        self._create_local_test_object()

        notification_count = Notification.objects.count()

        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[1],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[0]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[0],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )
        ObjectEventSubscription.objects.create(
            content_object=self.test_objects[1],
            stored_event_type=self.test_event_type.stored_event_type,
            user=self.test_users[1]
        )

        AccessControlList.objects.grant(
            obj=self.test_objects[0], permission=permission_events_view,
            role=self.test_roles[0]
        )

        result_0 = self.test_event_type.commit(
            action_object=self.test_objects[1], target=self.test_objects[0]
        )
        result_1 = self.test_event_type.commit(
            action_object=self.test_objects[0], target=self.test_objects[1]
        )

        self.assertEqual(Notification.objects.count(), notification_count + 2)
        notifications = Notification.objects.all()
        self.assertEqual(notifications[0].user, self.test_users[0])
        self.assertEqual(notifications[0].action, result_1)
        self.assertEqual(notifications[1].user, self.test_users[0])
        self.assertEqual(notifications[1].action, result_0)
