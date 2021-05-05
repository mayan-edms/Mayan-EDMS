from django.utils.encoding import force_bytes

from mayan.apps.storage.classes import DefinedStorage
from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..models import Cache
from ..tasks import task_cache_partition_purge, task_cache_purge

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
        self.test_cache_partition_files = []

    def tearDown(self):
        fs_cleanup(filename=self.temporary_directory)
        super().tearDown()

    def _create_test_cache(self, extra_data=None):
        data = {
            'defined_storage_name': TEST_STORAGE_NAME_FILE_CACHING_TEST_STORAGE,
            'maximum_size': TEST_CACHE_MAXIMUM_SIZE
        }

        if extra_data:
            data.update(extra_data)

        self.test_cache = Cache.objects.create(**data)

    def _create_test_cache_partition(self):
        self.test_cache_partition = self.test_cache.partitions.create(
            name=TEST_CACHE_PARTITION_NAME
        )

    def _create_test_cache_partition_file(self, filename=None, file_size=None):
        cache_partition_file_total = len(self.test_cache_partition_files)

        file_size = file_size or TEST_CACHE_PARTITION_FILE_SIZE
        filename = filename or '{}_{}'.format(
            TEST_CACHE_PARTITION_FILE_FILENAME, cache_partition_file_total
        )

        with self.test_cache_partition.create_file(filename=filename) as file_object:
            file_object.write(
                force_bytes(s=' ' * file_size)
            )

        self.test_cache_partition_file = self.test_cache_partition.files.get(
            filename=filename
        )

        self.test_cache_partition_files.append(self.test_cache_partition_file)


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


class FileCachingTaskTestMixin:
    def _execute_task_cache_partition_purge(self):
        task_cache_partition_purge.apply_async(
            kwargs={
                'cache_partition_id': self.test_cache_partition.pk
            }
        ).get()

    def _execute_task_cache_purge(self):
        task_cache_purge.apply_async(
            kwargs={
                'cache_id': self.test_cache.pk
            }
        ).get()
