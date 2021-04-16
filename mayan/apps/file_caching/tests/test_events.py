from mayan.apps.testing.tests.base import BaseTestCase

from ..events import event_cache_created, event_cache_purged
from ..models import Cache

from .mixins import CacheTestMixin


class CacheEventsTestCase(CacheTestMixin, BaseTestCase):
    def test_cache_create_event(self):
        self._clear_events()

        self._create_test_cache()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        cache = Cache.objects.last()

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, cache)
        self.assertEqual(events[0].target, cache)
        self.assertEqual(events[0].verb, event_cache_created.id)

    def test_cache_purge_event(self):
        self._create_test_cache()

        self._clear_events()

        self.test_cache.purge()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        cache = Cache.objects.last()

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, cache)
        self.assertEqual(events[0].target, cache)
        self.assertEqual(events[0].verb, event_cache_purged.id)
