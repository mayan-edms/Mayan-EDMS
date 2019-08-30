from __future__ import absolute_import, unicode_literals

from django_downloadview.test import assert_download_response

from mayan.apps.common.tests.base import GenericViewTestCase

from ..models import Key
from ..permissions import permission_key_download, permission_key_upload

from .literals import TEST_KEY_DATA, TEST_KEY_FINGERPRINT
from .mixins import KeyTestMixin


class KeyViewTestCase(KeyTestMixin, GenericViewTestCase):
    def test_key_download_view_no_permission(self):
        self._create_test_key()

        response = self.get(
            viewname='django_gpg:key_download', kwargs={'pk': self.test_key.pk}
        )
        self.assertEqual(response.status_code, 403)

    def test_key_download_view_with_permission(self):
        self.expected_content_type = 'application/octet-stream; charset=utf-8'

        self._create_test_key()

        self.grant_access(obj=self.test_key, permission=permission_key_download)

        response = self.get(
            viewname='django_gpg:key_download', kwargs={'pk': self.test_key.pk}
        )
        assert_download_response(
            self, response=response, content=self.test_key.key_data,
            basename=self.test_key.key_id,
        )

    def test_key_upload_view_no_permission(self):
        response = self.post(
            viewname='django_gpg:key_upload', data={'key_data': TEST_KEY_DATA}
        )
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Key.objects.count(), 0)

    def test_key_upload_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        response = self.post(
            viewname='django_gpg:key_upload', data={'key_data': TEST_KEY_DATA},
            follow=True
        )

        self.assertContains(response=response, text='created', status_code=200)

        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(Key.objects.first().fingerprint, TEST_KEY_FINGERPRINT)
