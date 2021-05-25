from mayan.apps.testing.tests.base import BaseTestCase

from ..classes import (
    EventManagerMethodAfter, EventModelRegistry, EventType, ModelEventType
)
from ..decorators import method_event

from .mixins import EventTypeTestMixin


class EventManagerTestCase(EventTypeTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_event_type()
        self._create_test_user()
        self._create_test_object()

        EventModelRegistry.register(model=self.TestModel)

        ModelEventType.register(
            event_types=(self.test_event_type,), model=self.TestModel
        )

        EventType.refresh()

    def test_event_ignore(self):
        def method_1(self):
            self._event_ignore = True
            self.method_2()

        @method_event(
            event_manager_class=EventManagerMethodAfter,
            event=self.test_event_type,
            target='self'
        )
        def method_2(self):
            """Nothing"""

        self.TestModel.method_1 = method_1
        self.TestModel.method_2 = method_2

        self._clear_events()

        self.test_object.method_1()

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
