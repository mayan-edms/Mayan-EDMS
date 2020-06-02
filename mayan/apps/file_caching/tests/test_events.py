from actstream.models import Action

from mayan.apps.tests.tests.base import BaseTestCase

from ..events import event_cache_created, event_cache_purged
from ..models import Cache

from .mixins import CacheTestMixin


class CacheEventsTestCase(CacheTestMixin, BaseTestCase):
    def test_cache_create_event(self):
        action_count = Action.objects.count()

        self._create_test_cache()

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        cache = Cache.objects.last()

        self.assertEqual(event.verb, event_cache_created.id)
        self.assertEqual(event.target, cache)

    def test_cache_purge_event(self):
        self._create_test_cache()

        action_count = Action.objects.count()

        self.test_cache.purge()

        self.assertEqual(Action.objects.count(), action_count + 1)

        event = Action.objects.first()

        cache = Cache.objects.last()

        self.assertEqual(event.verb, event_cache_purged.id)
        self.assertEqual(event.target, cache)
