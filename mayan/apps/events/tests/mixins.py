from __future__ import unicode_literals

from ..classes import EventTypeNamespace

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


class ObjectEventAPITestMixin(object):
    def _request_object_event_list_api_view(self):
        return self.get(
            viewname='rest_api:object-event-list',
            kwargs=self.view_arguments
        )
