from django.utils.encoding import force_bytes

from mayan.apps.storage.classes import DefinedStorage
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..models import Cache

from .literals import (
    TEST_CACHE_MAXIMUM_SIZE, TEST_CACHE_PARTITION_FILE_FILENAME,
    TEST_CACHE_PARTITION_FILE_SIZE, TEST_CACHE_PARTITION_NAME,
    TEST_STORAGE_NAME_FILE_CACHING_TEST_STORAGE
)


class CachePartitionViewTestMixin:
    def _request_test_object_file_cache_partition_purge_view(self):
        return self.post(
            viewname='file_caching:cache_partitions_purge',
            kwargs=self.test_object_view_kwargs
        )


class CacheTestMixin:
    def setUp(self):
        super().setUp()
        self.temporary_directory = mkdtemp()
        DefinedStorage(
            dotted_path='django.core.files.storage.FileSystemStorage',
            label='File caching test storage',
            name=TEST_STORAGE_NAME_FILE_CACHING_TEST_STORAGE,
            kwargs={'location': self.temporary_directory}
        )

    def tearDown(self):
        fs_cleanup(filename=self.temporary_directory)
        super().tearDown()

    def _create_test_cache(self):
        self.test_cache = Cache.objects.create(
            maximum_size=TEST_CACHE_MAXIMUM_SIZE,
            defined_storage_name=TEST_STORAGE_NAME_FILE_CACHING_TEST_STORAGE,
        )

    def _create_test_cache_partition(self):
        self.test_cache_partition = self.test_cache.partitions.create(
            name=TEST_CACHE_PARTITION_NAME
        )

    def _create_test_cache_partition_file(self):
        with self.test_cache_partition.create_file(filename=TEST_CACHE_PARTITION_FILE_FILENAME) as file_object:
            file_object.write(
                force_bytes(s=' ' * TEST_CACHE_PARTITION_FILE_SIZE)
            )

        self.test_cache_partition_file = self.test_cache_partition.files.get(
            filename=TEST_CACHE_PARTITION_FILE_FILENAME
        )


class CacheViewTestMixin:
    def _request_test_cache_detail_view(self):
        return self.get(
            viewname='file_caching:cache_detail', kwargs={
                'cache_id': self.test_cache.pk
            }
        )

    def _request_test_cache_list_view(self):
        return self.get(viewname='file_caching:cache_list')

    def _request_test_cache_purge_view(self):
        return self.post(
            viewname='file_caching:cache_purge', kwargs={
                'cache_id': self.test_cache.pk
            }
        )

    def _request_test_cache_multiple_purge_view(self):
        return self.post(
            viewname='file_caching:cache_multiple_purge', data={
                'id_list': self.test_cache.pk
            }
        )
