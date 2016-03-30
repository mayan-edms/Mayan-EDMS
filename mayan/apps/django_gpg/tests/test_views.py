from __future__ import absolute_import, unicode_literals

from django.core.files import File

from django_downloadview.test import assert_download_response

from documents.models import Document, DocumentVersion
from documents.tests.literals import TEST_DOCUMENT_PATH
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests import (
    TEST_USER_USERNAME, TEST_USER_PASSWORD
)

from ..models import Key
from ..permissions import permission_key_download

from .literals import (
    TEST_DETACHED_SIGNATURE, TEST_FILE, TEST_KEY_DATA, TEST_KEY_FINGERPRINT,
    TEST_KEY_PASSPHRASE, TEST_SEARCH_FINGERPRINT, TEST_SEARCH_UID,
    TEST_SIGNED_FILE, TEST_SIGNED_FILE_CONTENT
)


class KeyViewTestCase(GenericDocumentViewTestCase):
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
