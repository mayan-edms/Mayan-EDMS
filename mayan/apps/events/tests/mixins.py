from __future__ import unicode_literals

from ..classes import EventTypeNamespace

from .literals import (
    TEST_EVENT_TYPE_LABEL, TEST_EVENT_TYPE_NAME,
    TEST_EVENT_TYPE_NAMESPACE_LABEL, TEST_EVENT_TYPE_NAMESPACE_NAME
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
