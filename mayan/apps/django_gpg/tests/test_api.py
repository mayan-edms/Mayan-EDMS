from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Key
from ..permissions import (
    permission_key_delete, permission_key_upload, permission_key_view
)

from .literals import TEST_KEY_PRIVATE_FINGERPRINT
from .mixins import KeyAPIViewTestMixin, KeyTestMixin


class KeyAPITestCase(KeyTestMixin, KeyAPIViewTestMixin, BaseAPITestCase):
    def test_key_create_api_view_no_permission(self):
        response = self._request_test_key_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Key.objects.all().count(), 0)

    def test_key_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        response = self._request_test_key_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['fingerprint'], TEST_KEY_PRIVATE_FINGERPRINT
        )

        key = Key.objects.first()
        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(key.fingerprint, TEST_KEY_PRIVATE_FINGERPRINT)

    def test_key_create_validation_api_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        response = self._request_test_key_create_api_view(
            extra_data={'key_data': 'invalid data'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('key_data' in response.data)

        self.assertEqual(Key.objects.count(), 0)

    def test_key_destroy_api_view_no_permission(self):
        self._create_test_key_private()

        response = self._request_test_key_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Key.objects.count(), 1)

    def test_key_destroy_api_view_with_access(self):
        self._create_test_key_private()
        self.grant_access(
            obj=self.test_key_private, permission=permission_key_delete
        )

        response = self._request_test_key_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Key.objects.count(), 0)

    def test_key_list_api_view_no_permission(self):
        self._create_test_key_private()

        response = self._request_test_key_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_key_list_api_view_with_access(self):
        self._create_test_key_private()
        self.grant_access(
            obj=self.test_key_private, permission=permission_key_view
        )

        response = self._request_test_key_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'], 1
        )
        self.assertEqual(
            response.data['results'][0]['fingerprint'],
            self.test_key_private.fingerprint
        )

    def test_key_retrieve_api_view_no_permission(self):
        self._create_test_key_private()

        response = self._request_test_key_retreive_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_key_retrieve_api_view_with_access(self):
        self._create_test_key_private()
        self.grant_access(
            obj=self.test_key_private, permission=permission_key_view
        )

        response = self._request_test_key_retreive_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['fingerprint'], self.test_key_private.fingerprint
        )
