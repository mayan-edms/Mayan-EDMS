from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests.base import GenericViewTestCase

from ..models import Key
from ..permissions import (
    permission_key_delete, permission_key_download, permission_key_upload,
    permission_key_view
)

from .literals import TEST_KEY_PRIVATE_FINGERPRINT
from .mixins import KeyTestMixin, KeyViewTestMixin


class KeyViewTestCase(KeyTestMixin, KeyViewTestMixin, GenericViewTestCase):
    def test_key_delete_view_no_permission(self):
        self._create_test_key_private()
        key_count = Key.objects.count()

        response = self._request_test_key_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Key.objects.count(), key_count)

    def test_key_delete_view_with_access(self):
        self._create_test_key_private()
        self.grant_access(
            obj=self.test_key_private, permission=permission_key_delete
        )
        key_count = Key.objects.count()

        response = self._request_test_key_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Key.objects.count(), key_count - 1)

    def test_key_download_view_no_permission(self):
        self._create_test_key_private()

        response = self._request_test_key_download_view()
        self.assertEqual(response.status_code, 404)

    def test_key_download_view_with_access(self):
        self.expected_content_types = ('text/html; charset=utf-8',)

        self._create_test_key_private()

        self.grant_access(
            obj=self.test_key_private, permission=permission_key_download
        )

        response = self._request_test_key_download_view()
        self.assert_download_response(
            response=response, content=self.test_key_private.key_data,
            filename=self.test_key_private.key_id,
        )

    def test_key_detail_view_no_permission(self):
        self._create_test_key_private()

        response = self._request_test_key_detail_view()
        self.assertNotContains(
            response=response, text=self.test_key_private.key_id,
            status_code=404
        )

    def test_key_detail_view_with_access(self):
        self._create_test_key_private()

        self.grant_access(
            obj=self.test_key_private, permission=permission_key_view
        )

        response = self._request_test_key_detail_view()
        self.assertContains(
            response=response, text=self.test_key_private.key_id,
            status_code=200
        )

    def test_key_private_list_view_no_permission(self):
        self._create_test_key_private()

        response = self._request_test_key_private_list_view()
        self.assertNotContains(
            response=response, text=self.test_key_private.key_id,
            status_code=200
        )

    def test_key_private_list_view_with_access(self):
        self._create_test_key_private()

        self.grant_access(
            obj=self.test_key_private, permission=permission_key_view
        )

        response = self._request_test_key_private_list_view()
        self.assertContains(
            response=response, text=self.test_key_private.key_id,
            status_code=200
        )

    def test_key_public_list_view_no_permission(self):
        self._create_test_key_public()

        response = self._request_test_key_public_list_view()
        self.assertNotContains(
            response=response, text=self.test_key_public.key_id,
            status_code=200
        )

    def test_key_public_list_view_with_access(self):
        self._create_test_key_public()

        self.grant_access(
            obj=self.test_key_public, permission=permission_key_view
        )

        response = self._request_test_key_public_list_view()
        self.assertContains(
            response=response, text=self.test_key_public.key_id,
            status_code=200
        )

    def test_key_upload_view_no_permission(self):
        response = self._request_test_key_upload_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Key.objects.count(), 0)

    def test_key_upload_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        response = self._request_test_key_upload_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(
            Key.objects.first().fingerprint, TEST_KEY_PRIVATE_FINGERPRINT
        )
