import mock

from mayan.apps.testing.tests.base import BaseTestCase

from .literals import TEST_CACHE_PARTITION_FILE_FILENAME
from .mixins import CacheTestMixin


class CacheModelTestCase(CacheTestMixin, BaseTestCase):
    class FakeException(Exception):
        """
        Exception to force the cache file creation to fail but not the
        test itself.
        """

    def test_cache_get_absolute_url_method(self):
        self._create_test_cache()

        self.test_cache.get_absolute_url()

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

    def test_cleanup_on_storage_file_creation_error(self):
        self._silence_logger(name='mayan.apps.file_caching.models')

        self._create_test_cache()
        self._create_test_cache_partition()

        cache_parition_file_count = self.test_cache_partition.files.count()

        with self.assertRaises(expected_exception=CacheModelTestCase.FakeException):
            with self.test_cache_partition.create_file(filename=TEST_CACHE_PARTITION_FILE_FILENAME):
                raise CacheModelTestCase.FakeException

        self.assertEqual(
            self.test_cache_partition.files.count(),
            cache_parition_file_count
        )
        self.assertFalse(
            self.test_cache_partition.cache.storage.exists(
                name=self.test_cache_partition.get_full_filename(
                    filename=TEST_CACHE_PARTITION_FILE_FILENAME
                )
            )
        )

    @mock.patch('mayan.apps.file_caching.models.CachePartitionFile.save')
    def test_cleanup_on_model_file_creation_error(self, mock_save):
        self._silence_logger(name='mayan.apps.file_caching.models')

        mock_save.side_effect = CacheModelTestCase.FakeException

        self._create_test_cache()
        self._create_test_cache_partition()

        cache_parition_file_count = self.test_cache_partition.files.count()

        with self.assertRaises(expected_exception=CacheModelTestCase.FakeException):
            with self.test_cache_partition.create_file(filename=TEST_CACHE_PARTITION_FILE_FILENAME) as file_object:
                file_object.write(b'')

        self.assertEqual(
            self.test_cache_partition.files.count(),
            cache_parition_file_count
        )
        self.assertFalse(
            self.test_cache_partition.cache.storage.exists(
                name=self.test_cache_partition.get_full_filename(
                    filename=TEST_CACHE_PARTITION_FILE_FILENAME
                )
            )
        )
