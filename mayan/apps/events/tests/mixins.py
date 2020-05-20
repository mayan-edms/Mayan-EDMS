from actstream.models import Action

from ..classes import EventTypeNamespace
from ..models import Notification

from .literals import (
    TEST_EVENT_TYPE_LABEL, TEST_EVENT_TYPE_NAME,
    TEST_EVENT_TYPE_NAMESPACE_LABEL, TEST_EVENT_TYPE_NAMESPACE_NAME
)


class EventListAPIViewTestMixin(object):
    def _request_test_event_list_api_view(self):
        return self.get(viewname='rest_api:event-list')


class EventTypeNamespaceAPITestMixin(object):
    def _request_test_event_type_list_api_view(self):
        return self.get(viewname='rest_api:event-type-list')

    def _request_test_event_namespace_list_api_view(self):
        return self.get(viewname='rest_api:event-type-namespace-list')

    def _request_test_event_type_namespace_event_type_list_api_view(self):
        return self.get(
            viewname='rest_api:event-type-namespace-event-type-list',
            kwargs={
                'name': self.test_event_type_namespace.name
            }
        )


class EventTypeTestMixin(object):
    def _create_test_event_type(self):
        self.test_event_type_namespace = EventTypeNamespace(
            label=TEST_EVENT_TYPE_NAMESPACE_LABEL,
            name=TEST_EVENT_TYPE_NAMESPACE_NAME
        )
        self.test_event_type = self.test_event_type_namespace.add_event_type(
            label=TEST_EVENT_TYPE_LABEL,
            name=TEST_EVENT_TYPE_NAME
        )


class NotificationTestMixin(object):
    def _create_test_notification(self):
        self.test_notification = Notification.objects.create(
            user=self._test_case_user, action=Action.objects.first(),
            read=False
        )


class NotificationViewTestMixin(object):
    def _request_test_notification_list_view(self):
        return self.get(viewname='events:user_notifications_list')

    def _request_test_notification_mark_read_all_view(self):
        return self.post(viewname='events:notification_mark_read_all')

    def _request_test_notification_mark_read(self):
        return self.post(
            viewname='events:notification_mark_read', kwargs={
                'notification_id': self.test_notification.pk
            }
        )


class ObjectEventAPITestMixin(object):
    def _request_object_event_list_api_view(self):
        return self.get(
            viewname='rest_api:object-event-list',
            kwargs=self.view_arguments
        )


class UserEventViewsTestMixin(object):
    def _request_test_user_event_type_subscription_list_view(self):
        return self.get(viewname='events:event_types_user_subcriptions_list')
