from __future__ import absolute_import, unicode_literals

from django.core.files import File

from mayan.apps.django_gpg.models import Key
from mayan.apps.django_gpg.tests.literals import TEST_KEY_PRIVATE_PASSPHRASE

from ..models import DetachedSignature

from .literals import TEST_KEY_FILE_PATH, TEST_SIGNATURE_FILE_PATH


class DetachedSignatureViewTestMixin(object):
    def _request_test_document_version_signature_create_view(self):
        return self.post(
            viewname='signatures:document_version_signature_detached_create',
            kwargs={'pk': self.test_document_version.pk}, data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )

    def _request_test_document_version_signature_download_view(self):
        return self.get(
            viewname='signatures:document_version_signature_download',
            kwargs={'pk': self.test_signature.pk}
        )

    def _request_test_document_version_signature_upload_view(self):
        with open(TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            return self.post(
                viewname='signatures:document_version_signature_upload',
                kwargs={'pk': self.test_document.latest_version.pk},
                data={'signature_file': file_object}
            )


class EmbeddedSignatureViewTestMixin(object):
    def _request_test_document_version_signature_create_view(self):
        return self.post(
            viewname='signatures:document_version_signature_embedded_create',
            kwargs={'pk': self.test_document_version.pk}, data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )


class SignatureTestMixin(object):
    def _create_test_detached_signature(self):
        with open(TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            self.test_signature = DetachedSignature.objects.create(
                document_version=self.test_document.latest_version,
                signature_file=File(file_object)
            )

    def _create_test_key_public(self):
        with open(TEST_KEY_FILE_PATH, mode='rb') as file_object:
            self.test_key_public = Key.objects.create(
                key_data=file_object.read()
            )


class SignatureViewTestMixin(object):
    def _request_test_document_version_signature_delete_view(self):
        return self.post(
            viewname='signatures:document_version_signature_delete',
            kwargs={'pk': self.test_signature.pk}
        )

    def _request_test_document_version_signature_details_view(self):
        return self.get(
            viewname='signatures:document_version_signature_details',
            kwargs={'pk': self.test_signature.pk}
        )

    def _request_test_document_version_signature_list_view(self, document):
        return self.get(
            viewname='signatures:document_version_signature_list',
            kwargs={'pk': self.test_document.latest_version.pk}
        )

    def _request_all_test_document_version_signature_verify_view(self):
        return self.post(
            viewname='signatures:all_document_version_signature_verify'
        )
