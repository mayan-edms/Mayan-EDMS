from mayan.apps.testing.tests.base import BaseTestCase

from ..models import ErrorLogPartitionEntry

from .mixins import LoggingTextMixin


class LoggingModelTestCase(LoggingTextMixin, BaseTestCase):
    def setUp(self):
        super().setUp()
        self._create_error_log_test_object()
        self._create_error_log_entry()

    def test_entries_limit(self):
        self.error_log.limit = 3
        self.test_object.error_log.create(text='1')
        self.test_object.error_log.create(text='2')
        self.test_object.error_log.create(text='3')
        self.test_object.error_log.create(text='4')

        self.assertEqual(
            list(self.test_object.error_log.values_list('text', flat=True)),
            ['2', '3', '4']
        )

    def test_object_deletion(self):
        self.test_object.delete()
        self.assertEqual(ErrorLogPartitionEntry.objects.count(), 0)
