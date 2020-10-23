import mock

from mayan.apps.testing.tests.base import BaseTestCase

from .mixins import CacheTestMixin


class CacheModelTestCase(CacheTestMixin, BaseTestCase):
    def test_cache_purge(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        cache_total_size = self.test_cache.get_total_size()

        self.test_cache.purge()

        self.assertNotEqual(cache_total_size, self.test_cache.get_total_size())

    @mock.patch('django.core.files.File.close')
    def test_storage_file_close(self, mock_storage_file_close_method):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        self.assertTrue(mock_storage_file_close_method.called)
