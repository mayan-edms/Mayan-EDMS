from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_cache_purged
from ..permissions import (
    permission_cache_purge, permission_cache_view
)

from .mixins import CacheTestMixin, CacheViewTestMixin


class CacheViewTestCase(
    CacheTestMixin, CacheViewTestMixin, GenericViewTestCase
):
    _test_event_object_name = 'test_cache'

    def test_cache_detail_view_no_permission(self):
        self._create_test_cache()

        self._clear_events()

        response = self._request_test_cache_detail_view()
        self.assertNotContains(
            response=response, text=self.test_cache.label, status_code=404
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_cache_detail_view_with_access(self):
        self._create_test_cache()

        self.grant_access(
            obj=self.test_cache, permission=permission_cache_view
        )

        self._clear_events()

        response = self._request_test_cache_detail_view()
        self.assertContains(
            response=response, text=self.test_cache.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_cache_list_view_with_no_permission(self):
        self._create_test_cache()

        self._clear_events()

        response = self._request_test_cache_list_view()
        self.assertNotContains(
            response=response, text=self.test_cache.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_cache_list_view_with_access(self):
        self._create_test_cache()

        self.grant_access(
            obj=self.test_cache, permission=permission_cache_view
        )

        self._clear_events()

        response = self._request_test_cache_list_view()
        self.assertContains(
            response=response, text=self.test_cache.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_cache_purge_view_no_permission(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        cache_total_size = self.test_cache.get_total_size()

        self._clear_events()

        response = self._request_test_cache_purge_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(cache_total_size, self.test_cache.get_total_size())

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_cache_purge_view_with_access(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        self.grant_access(
            obj=self.test_cache, permission=permission_cache_purge
        )

        cache_total_size = self.test_cache.get_total_size()

        self._clear_events()

        response = self._request_test_cache_purge_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(cache_total_size, self.test_cache.get_total_size())

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.action_object, None)
        self.assertEqual(event.target, self.test_cache)
        self.assertEqual(event.verb, event_cache_purged.id)

    def test_cache_multiple_purge_view_no_permission(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        cache_total_size = self.test_cache.get_total_size()

        self._clear_events()

        response = self._request_test_cache_multiple_purge_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(cache_total_size, self.test_cache.get_total_size())

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_cache_multiple_purge_view_with_access(self):
        self._create_test_cache()
        self._create_test_cache_partition()
        self._create_test_cache_partition_file()

        self.grant_access(
            obj=self.test_cache, permission=permission_cache_purge
        )

        cache_total_size = self.test_cache.get_total_size()

        self._clear_events()

        response = self._request_test_cache_multiple_purge_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(cache_total_size, self.test_cache.get_total_size())

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.action_object, None)
        self.assertEqual(event.target, self.test_cache)
        self.assertEqual(event.verb, event_cache_purged.id)
