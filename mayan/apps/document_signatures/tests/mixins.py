from __future__ import absolute_import, unicode_literals

from django.core.files import File

from mayan.apps.django_gpg.models import Key

from ..models import DetachedSignature

from .literals import TEST_KEY_FILE, TEST_SIGNATURE_FILE_PATH


class SignaturesTestMixin(object):
    def _create_test_detached_signature(self):
        with open(TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            self.test_signature = DetachedSignature.objects.create(
                document_version=self.test_document.latest_version,
                signature_file=File(file_object)
            )

    def _create_test_key(self):
        with open(TEST_KEY_FILE, mode='rb') as file_object:
            self.test_key = Key.objects.create(key_data=file_object.read())
