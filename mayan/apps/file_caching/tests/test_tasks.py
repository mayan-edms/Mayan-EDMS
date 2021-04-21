from mayan.apps.testing.tests.base import BaseTestCase

from ..events import event_cache_partition_purged, event_cache_purged

from .mixins import CacheTestMixin, FileCachingTaskTestMixin


class FileCachingTaskTestCase(
    FileCachingTaskTestMixin, CacheTestMixin, BaseTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

    def test_task_cache_partition_purge(self):
        self._clear_events()

        self._execute_task_cache_partition_purge()

        self.assertEqual(self.test_cache_partition.files.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_cache_partition)
        self.assertEqual(events[0].target, self.test_cache_partition)
        self.assertEqual(events[0].verb, event_cache_partition_purged.id)

    def test_task_cache_purge(self):
        self._clear_events()

        self._execute_task_cache_purge()

        self.assertEqual(self.test_cache_partition.files.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_cache_partition)
        self.assertEqual(events[0].target, self.test_cache_partition)
        self.assertEqual(events[0].verb, event_cache_partition_purged.id)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self.test_cache)
        self.assertEqual(events[1].target, self.test_cache)
        self.assertEqual(events[1].verb, event_cache_purged.id)
