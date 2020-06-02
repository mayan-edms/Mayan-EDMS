from mayan.apps.tests.tests.base import BaseTestCase

from .mixins import CacheTestMixin


class CacheModelTestCase(CacheTestMixin, BaseTestCase):
    def test_cache_purge(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        cache_total_size = self.test_cache.get_total_size()

        self.test_cache.purge()

        self.assertNotEqual(cache_total_size, self.test_cache.get_total_size())
