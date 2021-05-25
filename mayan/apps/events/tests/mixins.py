from actstream.models import Action

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.permissions.tests.mixins import RoleTestMixin
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from ..classes import (
    EventModelRegistry, EventTypeNamespace, EventType, ModelEventType
)
from ..models import Notification
from ..permissions import permission_events_view

from .literals import (
    TEST_EVENT_TYPE_LABEL, TEST_EVENT_TYPE_NAME,
    TEST_EVENT_TYPE_NAMESPACE_LABEL, TEST_EVENT_TYPE_NAMESPACE_NAME
)


class EventListAPIViewTestMixin:
    def _request_test_event_list_api_view(self):
        return self.get(viewname='rest_api:event-list')


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
                'name': self.test_event_type_namespace.name
            }
        )


class EventTypeTestMixin:
    def setUp(self):
        super().setUp()
        self.test_actions = []

    def _create_test_event_type(self):
        self.test_event_type_namespace = EventTypeNamespace(
            label=TEST_EVENT_TYPE_NAMESPACE_LABEL,
            name=TEST_EVENT_TYPE_NAMESPACE_NAME
        )
        self.test_event_type = self.test_event_type_namespace.add_event_type(
            label=TEST_EVENT_TYPE_LABEL,
            name=TEST_EVENT_TYPE_NAME
        )


class EventViewTestMixin:
    def _request_test_current_user_events_view(self):
        return self.get(
            viewname='events:current_user_events'
        )

    def _request_test_events_by_verb_view(self):
        return self.get(
            viewname='events:events_by_verb', kwargs={
                'verb': self.test_event_type.id
            }
        )

    def _request_test_events_list_view(self):
        return self.get(viewname='events:events_list')

    def _request_events_for_object_view(self):
        return self.get(
            viewname='events:events_for_object', kwargs=self.view_arguments
        )


class EventsExportViewTestMixin:
    def _request_test_current_user_events_export_view(self):
        return self.post(
            viewname='events:current_user_events_export'
        )

    def _request_test_events_by_verb_export_view(self):
        return self.post(
            viewname='events:events_by_verb_export', kwargs={
                'verb': self.test_event_type.id
            }
        )

    def _request_test_events_list_export_view(self):
        return self.post(viewname='events:events_list_export')

    def _request_events_for_object_export_view(self):
        return self.post(
            viewname='events:events_for_object_export',
            kwargs=self.view_arguments
        )


class NotificationTestMixin(
    EventTypeTestMixin, GroupTestMixin, RoleTestMixin
):
    def _create_local_test_object(self):
        super()._create_test_object()

        EventModelRegistry.register(model=self.TestModel)

        ModelEventType.register(
            event_types=(self.test_event_type,), model=self.TestModel
        )

        EventType.refresh()

        ModelPermission.register(
            model=self.TestModel, permissions=(
                permission_events_view,
            )
        )

    def _create_local_test_user(self):
        self._create_test_user()
        self._create_test_group(add_users=(self.test_user,))
        self._create_test_role(add_groups=(self.test_group,))

    def _create_test_notification(self):
        self.test_notification = Notification.objects.create(
            user=self._test_case_user, action=Action.objects.first(),
            read=False
        )


class NotificationViewTestMixin:
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


class ObjectEventAPITestMixin:
    def _request_object_event_list_api_view(self):
        return self.get(
            viewname='rest_api:object-event-list',
            kwargs=self.view_arguments
        )


class UserEventViewsTestMixin:
    def _request_test_user_event_type_subscription_list_view(self):
        return self.get(viewname='events:event_types_user_subcriptions_list')
