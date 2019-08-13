from __future__ import unicode_literals

from mayan.apps.common.tests import GenericViewTestCase

from ..permissions import (
    permission_cache_purge, permission_cache_view
)

from .mixins import CacheTestMixin, CacheViewTestMixin


class CacheViewTestCase(
    CacheTestMixin, CacheViewTestMixin, GenericViewTestCase
):
    def test_cache_list_view_with_no_permission(self):
        self._create_test_cache()

        response = self._request_test_cache_list_view()
        self.assertNotContains(
            response=response, text=self.test_cache.label, status_code=200
        )

    def test_cache_list_view_with_access(self):
        self._create_test_cache()

        self.grant_access(
            obj=self.test_cache, permission=permission_cache_view
        )

        response = self._request_test_cache_list_view()
        self.assertContains(
            response=response, text=self.test_cache.label, status_code=200
        )

    def test_cache_purge_view_no_permissions(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        cache_total_size = self.test_cache.get_total_size()

        response = self._request_test_cache_purge_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(cache_total_size, self.test_cache.get_total_size())

    def test_cache_purge_view_with_access(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        self.grant_access(
            obj=self.test_cache, permission=permission_cache_purge
        )

        cache_total_size = self.test_cache.get_total_size()

        response = self._request_test_cache_purge_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(cache_total_size, self.test_cache.get_total_size())

    def test_cache_multiple_purge_view_no_permissions(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        cache_total_size = self.test_cache.get_total_size()

        response = self._request_test_cache_multiple_purge_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(cache_total_size, self.test_cache.get_total_size())

    def test_cache_multiple_purge_view_with_access(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        self.grant_access(
            obj=self.test_cache, permission=permission_cache_purge
        )

        cache_total_size = self.test_cache.get_total_size()

        response = self._request_test_cache_multiple_purge_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(cache_total_size, self.test_cache.get_total_size())
