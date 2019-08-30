from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Key
from ..permissions import (
    permission_key_delete, permission_key_upload, permission_key_view
)

from .literals import TEST_KEY_DATA, TEST_KEY_FINGERPRINT
from .mixins import KeyTestMixin


class KeyAPITestCase(KeyTestMixin, BaseAPITestCase):

    # Key creation by upload

    def _request_key_create_view(self):
        return self.post(
            viewname='rest_api:key-list', data={
                'key_data': TEST_KEY_DATA
            }
        )

    def test_key_create_view_no_permission(self):
        response = self._request_key_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Key.objects.all().count(), 0)

    def test_key_create_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        response = self._request_key_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['fingerprint'], TEST_KEY_FINGERPRINT)

        key = Key.objects.first()
        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(key.fingerprint, TEST_KEY_FINGERPRINT)

    # Key deletion

    def _request_key_delete_view(self):
        return self.delete(
            viewname='rest_api:key-detail', kwargs={'pk': self.test_key.pk}
        )

    def test_key_delete_view_no_access(self):
        self._create_test_key()

        response = self._request_key_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Key.objects.count(), 1)

    def test_key_delete_view_with_access(self):
        self._create_test_key()
        self.grant_access(
            obj=self.test_key, permission=permission_key_delete
        )

        response = self._request_key_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Key.objects.count(), 0)

    # Key detail

    def _request_key_detail_view(self):
        return self.get(
            viewname='rest_api:key-detail', kwargs={'pk': self.test_key.pk}
        )

    def test_key_detail_view_no_access(self):
        self._create_test_key()

        response = self._request_key_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_key_detail_view_with_access(self):
        self._create_test_key()
        self.grant_access(
            obj=self.test_key, permission=permission_key_view
        )

        response = self._request_key_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['fingerprint'], self.test_key.fingerprint
        )
