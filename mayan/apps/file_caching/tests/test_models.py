import mock

from mayan.apps.testing.tests.base import BaseTestCase

from ..exceptions import FileCachingException
from ..models import CachePartitionFile

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

    def test_cache_partition_file_hits(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        cache_partition_file_hits = self.test_cache_partition_file.hits

        with self.test_cache_partition_file.open():
            """Do nothing"""

        self.test_cache_partition_file.refresh_from_db()

        self.assertEqual(
            self.test_cache_partition_file.hits, cache_partition_file_hits + 1
        )

    def test_cache_partition_file_lru_eviction(self):
        self._create_test_cache(
            extra_data={
                'maximum_size': 2
            }
        )

        self._create_test_cache_partition()
        self._create_test_cache_partition_file(file_size=1)
        self._create_test_cache_partition_file(file_size=1)

        with self.test_cache_partition_files[0].open():
            """Do nothing"""

        self._create_test_cache_partition_file(file_size=1)

        # Older but more hits was kept.
        self.assertTrue(
            self.test_cache_partition_files[0] in CachePartitionFile.objects.all()
        )
        # Newer but less hits was purged.
        self.assertTrue(
            self.test_cache_partition_files[1] not in CachePartitionFile.objects.all()
        )

    def test_cache_partition_file_size_protection(self):
        self._create_test_cache(
            extra_data={
                'maximum_size': 1
            }
        )

        self._create_test_cache_partition()

        with self.assertRaises(expected_exception=FileCachingException):
            self._create_test_cache_partition_file(file_size=2)

    @mock.patch('mayan.apps.file_caching.models.Cache.prune')
    def test_prune_on_cache_size_reduction(self, mock_cache_prune_method):
        self._create_test_cache(
            extra_data={
                'maximum_size': 2
            }
        )

        self.test_cache.maximum_size = 2
        self.test_cache.save()
        self.assertFalse(mock_cache_prune_method.called)

        self.test_cache.maximum_size = 1
        self.test_cache.save()
        self.assertTrue(mock_cache_prune_method.called)

    def test_incremental_file_index_cache_prune(self):
        self._create_test_cache(
            extra_data={
                'maximum_size': 2
            }
        )

        self._create_test_cache_partition()
        self._create_test_cache_partition_file(file_size=1)
        self._create_test_cache_partition_file(file_size=1)

        with self.test_cache_partition_files[1].open():
            """Increase hits of file #1"""

        with self.test_cache_partition_files[0].open():
            """Lock and increase hits of file #0"""
            self._create_test_cache_partition_file(file_size=1)

        self.assertTrue(
            self.test_cache_partition_files[0] in CachePartitionFile.objects.all()
        )
        self.assertTrue(
            self.test_cache_partition_files[1] not in CachePartitionFile.objects.all()
        )
        self.assertTrue(
            self.test_cache_partition_files[2] in CachePartitionFile.objects.all()
        )
