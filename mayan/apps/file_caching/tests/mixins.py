from __future__ import unicode_literals

from django.core.files.storage import FileSystemStorage
from django.utils.encoding import force_bytes

from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..models import Cache

from .literals import (
    TEST_CACHE_LABEL, TEST_CACHE_MAXIMUM_SIZE, TEST_CACHE_NAME,
    TEST_CACHE_PARTITION_FILE_FILENAME, TEST_CACHE_PARTITION_FILE_SIZE,
    TEST_CACHE_PARTITION_NAME, TEST_CACHE_STORAGE_INSTANCE_PATH
)

test_storage = None


class CacheTestMixin(object):
    def setUp(self):
        super(CacheTestMixin, self).setUp()
        global test_storage
        self.temporary_directory = mkdtemp()
        test_storage = FileSystemStorage(location=self.temporary_directory)

    def tearDown(self):
        fs_cleanup(filename=self.temporary_directory)
        super(CacheTestMixin, self).tearDown()

    def _create_test_cache(self):
        self.test_cache = Cache.objects.create(
            label=TEST_CACHE_LABEL,
            storage_instance_path=TEST_CACHE_STORAGE_INSTANCE_PATH,
            maximum_size=TEST_CACHE_MAXIMUM_SIZE,
            name=TEST_CACHE_NAME,
        )

    def _create_test_cache_partition(self):
        self.test_cache_partition = self.test_cache.partitions.create(
            name=TEST_CACHE_PARTITION_NAME
        )

    def _create_test_cache_partition_file(self):
        with self.test_cache_partition.create_file(filename=TEST_CACHE_PARTITION_FILE_FILENAME) as file_object:
            file_object.write(
                force_bytes(' ' * TEST_CACHE_PARTITION_FILE_SIZE)
            )

        self.test_cache_partition_file = self.test_cache_partition.files.get(
            filename=TEST_CACHE_PARTITION_FILE_FILENAME
        )


class CacheViewTestMixin(object):
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
