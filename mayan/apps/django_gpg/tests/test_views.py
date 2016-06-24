from __future__ import absolute_import, unicode_literals

from django_downloadview.test import assert_download_response

from common.tests.test_views import GenericViewTestCase
from user_management.tests import TEST_USER_USERNAME, TEST_USER_PASSWORD

from ..models import Key
from ..permissions import permission_key_download, permission_key_upload

from .literals import TEST_KEY_DATA, TEST_KEY_FINGERPRINT


class KeyViewTestCase(GenericViewTestCase):
    def test_key_download_view_no_permission(self):
        key = Key.objects.create(key_data=TEST_KEY_DATA)

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.get(
            viewname='django_gpg:key_download', args=(key.pk,)
        )

        self.assertEqual(response.status_code, 403)

    def test_key_download_view_with_permission(self):
        key = Key.objects.create(key_data=TEST_KEY_DATA)

        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_key_download.stored_permission)

        response = self.get(
            viewname='django_gpg:key_download', args=(key.pk,)
        )

        assert_download_response(
            self, response=response, content=key.key_data,
            basename=key.key_id,
        )

    def test_key_upload_view_no_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        response = self.post(
            viewname='django_gpg:key_upload', data={'key_data': TEST_KEY_DATA}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Key.objects.count(), 0)

    def test_key_upload_view_with_permission(self):
        self.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)

        self.role.permissions.add(permission_key_upload.stored_permission)

        response = self.post(
            viewname='django_gpg:key_upload', data={'key_data': TEST_KEY_DATA},
            follow=True
        )

        self.assertContains(response, 'created', status_code=200)

        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(Key.objects.first().fingerprint, TEST_KEY_FINGERPRINT)
