from actstream.models import Action, any_stream

from mayan.apps.acls.classes import ModelPermission

from ..classes import (
    EventModelRegistry, EventTypeNamespace, EventType, ModelEventType
)
from ..models import Notification, ObjectEventSubscription
from ..permissions import permission_events_view

from .literals import (
    TEST_EVENT_TYPE_LABEL, TEST_EVENT_TYPE_NAME,
    TEST_EVENT_TYPE_NAMESPACE_LABEL, TEST_EVENT_TYPE_NAMESPACE_NAME
)


class EventsClearViewTestMixin:
    def _request_test_verb_event_list_clear_view(self):
        return self.post(
            viewname='events:verb_event_list_clear', kwargs={
                'verb': self._test_event_type.id
            }
        )

    def _request_test_event_list_clear_view(self):
        return self.post(viewname='events:event_list_clear')

    def _request_object_event_list_clear_view(self):
        return self.post(
            viewname='events:object_event_list_clear',
            kwargs=self.view_arguments
        )


class EventsExportViewTestMixin:
    def _request_test_verb_event_list_export_view(self):
        return self.post(
            viewname='events:verb_event_list_export', kwargs={
                'verb': self._test_event_type.id
            }
        )

    def _request_test_event_list_export_view(self):
        return self.post(viewname='events:event_list_export')

    def _request_object_event_list_export_view(self):
        return self.post(
            viewname='events:object_event_list_export',
            kwargs=self.view_arguments
        )


class EventListAPIViewTestMixin:
    def _request_test_event_list_api_view(self):
        return self.get(viewname='rest_api:event-list')


class EventObjectTestMixin:
    def _create_test_object_with_event_type_and_permission(self):
        self._create_test_object()

        EventModelRegistry.register(model=self.TestModel)

        ModelEventType.register(
            event_types=(self._test_event_type,), model=self.TestModel
        )

        EventType.refresh()

        ModelPermission.register(
            model=self.TestModel, permissions=(
                permission_events_view,
            )
        )


class EventTestMixin:
    def setUp(self):
        super().setUp()
        self._test_events = []

    def _create_test_event(self, action_object=None, actor=None, target=None):
        self._test_event = self._test_event_type.commit(
            action_object=action_object, actor=actor or self._test_case_user,
            target=target
        )
        self._test_events.append(self._test_event)


class EventTestCaseMixin:
    def setUp(self):
        super().setUp()
        Action.objects.all().delete()

    def _clear_events(self):
        Action.objects.all().delete()

    def _get_test_events(self):
        return Action.objects.all().order_by('timestamp')


class EventTypeNamespaceAPITestMixin:
    def _request_test_event_type_list_api_view(self):
        return self.get(viewname='rest_api:event-type-list')

    def _request_test_event_namespace_list_api_view(self):
        return self.get(viewname='rest_api:event-type-namespace-list')

    def _request_test_event_type_namespace_event_type_list_api_view(self):
        return self.get(
            viewname='rest_api:event-type-namespace-event-type-list',
            kwargs={
                'name': self._test_event_type_namespace.name
            }
        )


class EventTypeTestMixin:
    def setUp(self):
        super().setUp()
        self._test_event_types = []

    def _create_test_event_type(self):
        total_test_event_types = len(self._test_event_types)
        test_namespace_label = '{}_{}'.format(
            TEST_EVENT_TYPE_NAMESPACE_LABEL, total_test_event_types
        )
        test_namespace_name = '{}_{}'.format(
            TEST_EVENT_TYPE_NAMESPACE_NAME, total_test_event_types
        )
        test_event_label = '{}_{}'.format(
            TEST_EVENT_TYPE_LABEL, total_test_event_types
        )
        test_event_name = '{}_{}'.format(
            TEST_EVENT_TYPE_NAME, total_test_event_types
        )

        self._test_event_type_namespace = EventTypeNamespace(
            label=test_namespace_label, name=test_namespace_name
        )
        self._test_event_type = self._test_event_type_namespace.add_event_type(
            label=test_event_label, name=test_event_name
        )
        self._test_event_types.append(self._test_event_type)


class EventViewTestMixin:
    def _request_test_verb_event_list_view(self):
        return self.get(
            viewname='events:verb_event_list', kwargs={
                'verb': self._test_event_type.id
            }
        )

    def _request_test_event_list_view(self):
        return self.get(viewname='events:event_list')

    def _request_test_object_event_list_view(self):
        return self.get(
            viewname='events:object_event_list', kwargs=self.view_arguments
        )


class NotificationTestMixin:
    def _create_test_notification(self):
        action = any_stream(obj=self._test_object).first()

        self._test_notification = Notification.objects.create(
            action=action, read=False, user=self._test_case_user
        )


class NotificationViewTestMixin:
    def _request_test_notification_list_view(self):
        return self.get(viewname='events:user_notifications_list')

    def _request_test_notification_mark_read_all_view(self):
        return self.post(viewname='events:notification_mark_read_all')

    def _request_test_notification_mark_read(self):
        return self.post(
            viewname='events:notification_mark_read', kwargs={
                'notification_id': self._test_notification.pk
            }
        )


class ObjectEventAPITestMixin:
    def _request_object_event_list_api_view(self):
        return self.get(
            viewname='rest_api:object-event-list',
            kwargs=self.view_arguments
        )


class ObjectEventSubscriptionTestMixin:
    def _create_test_object_event_subscription(self):
        ObjectEventSubscription.objects.create(
            content_object=self._test_object,
            user=self._test_case_user,
            stored_event_type=self._test_event_type.get_stored_event_type()
        )


class UserEventViewTestMixin:
    def _request_test_user_event_type_subscription_list_view(self):
        return self.get(viewname='events:event_type_user_subscription_list')


class UserObjectSubscriptionViewTestMixin:
    def _request_user_object_subscription_list_view(self):
        return self.get(
            viewname='events:user_object_subscription_list'
        )
