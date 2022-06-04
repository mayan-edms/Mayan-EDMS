from mayan.apps.testing.tests.base import BaseTestCase

from ..events import event_error_log_deleted
from ..models import ErrorLogPartitionEntry

from .mixins import ErrorLogPartitionEntryTestMixin


class ErrorLoggingModelTestCase(ErrorLogPartitionEntryTestMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_test_error_log_object()
        self._create_test_error_log_entry()

    def test_entries_limit(self):
        self.error_log.limit = 3
        self._test_object.error_log.create(text='1')
        self._test_object.error_log.create(text='2')
        self._test_object.error_log.create(text='3')
        self._test_object.error_log.create(text='4')

        self.assertEqual(
            list(self._test_object.error_log.values_list('text', flat=True)),
            ['2', '3', '4']
        )

    def test_orphan_error_logs_after_object_deletion(self):
        self._clear_events()

        self._test_object.delete()
        self.assertEqual(ErrorLogPartitionEntry.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_error_log_deletion(self):
        self._clear_events()

        self._test_error_log_entry.delete()
        self.assertEqual(ErrorLogPartitionEntry.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_object)
        self.assertEqual(events[0].target, self._test_object)
        self.assertEqual(events[0].verb, event_error_log_deleted.id)
