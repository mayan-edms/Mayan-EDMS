from django.core.files import File

from mayan.apps.django_gpg.tests.literals import TEST_KEY_PRIVATE_PASSPHRASE

from ..models import DetachedSignature

from .literals import TEST_SIGNATURE_FILE_PATH


class DetachedSignatureAPIViewTestMixin:
    def _request_test_document_signature_detached_delete_view(self):
        return self.delete(
            viewname='rest_api:detachedsignature-detail',
            kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
                'detached_signature_id': self.test_document_file.signatures.first().pk
            }
        )

    def _request_test_document_signature_detached_detail_view(self):
        return self.get(
            viewname='rest_api:detachedsignature-detail',
            kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
                'detached_signature_id': self.test_document_file.signatures.first().pk
            }
        )

    def _request_test_document_signature_detached_list_view(self):
        return self.get(
            viewname='rest_api:document-file-signature-detached-list',
            kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_signature_detached_sign_view(self):
        return self.post(
            viewname='rest_api:document-file-signature-detached-sign',
            kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk
            }, data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )

    def _request_test_document_signature_detached_upload_view(self):
        with open(file=TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            return self.post(
                viewname='rest_api:document-file-signature-detached-upload',
                kwargs={
                    'document_id': self.test_document.pk,
                    'document_file_id': self.test_document_file.pk
                }, data={'signature_file': file_object}
            )


class DetachedSignatureViewTestMixin:
    def _request_test_document_file_signature_create_view(self):
        return self.post(
            viewname='signatures:document_file_signature_detached_create',
            kwargs={
                'document_file_id': self.test_document_file.pk
            }, data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )

    def _request_test_document_file_signature_download_view(self):
        return self.get(
            viewname='signatures:document_file_signature_download',
            kwargs={'signature_id': self.test_signature.pk}
        )

    def _request_test_document_file_signature_upload_view(self):
        with open(file=TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            return self.post(
                viewname='signatures:document_file_signature_upload',
                kwargs={
                    'document_file_id': self.test_document.file_latest.pk
                }, data={'signature_file': file_object}
            )


class EmbeddedSignatureAPIViewTestMixin:
    def _request_test_document_signature_embedded_detail_view(self):
        return self.get(
            viewname='rest_api:embeddedsignature-detail',
            kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk,
                'embedded_signature_id': self.test_document_file.signatures.first().pk
            }
        )

    def _request_test_document_signature_embedded_list_view(self):
        return self.get(
            viewname='rest_api:document-file-signature-embedded-list',
            kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk
            }
        )

    def _request_test_document_signature_embedded_sign_view(self):
        return self.post(
            viewname='rest_api:document-file-signature-embedded-sign',
            kwargs={
                'document_id': self.test_document.pk,
                'document_file_id': self.test_document_file.pk
            }, data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )


class EmbeddedSignatureViewTestMixin:
    def _request_test_document_file_signature_create_view(self):
        return self.post(
            viewname='signatures:document_file_signature_embedded_create',
            kwargs={
                'document_file_id': self.test_document_file.pk
            }, data={
                'key': self.test_key_private.pk,
                'passphrase': TEST_KEY_PRIVATE_PASSPHRASE
            }
        )


class SignatureTestMixin:
    def _upload_test_detached_signature(self):
        with open(file=TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            self.test_signature = DetachedSignature.objects.create(
                document_file=self.test_document.file_latest,
                signature_file=File(file=file_object)
            )


class SignatureViewTestMixin:
    def _request_test_document_file_signature_delete_view(self):
        return self.post(
            viewname='signatures:document_file_signature_delete', kwargs={
                'signature_id': self.test_signature.pk
            }
        )

    def _request_test_document_file_signature_details_view(self):
        return self.get(
            viewname='signatures:document_file_signature_details',
            kwargs={'signature_id': self.test_signature.pk}
        )

    def _request_test_document_file_signature_list_view(self, document):
        return self.get(
            viewname='signatures:document_file_signature_list',
            kwargs={
                'document_file_id': self.test_document.file_latest.pk
            }
        )


class SignatureToolsViewTestMixin:
    def _request_all_test_document_file_signature_refresh_view(self):
        return self.post(
            viewname='signatures:all_document_file_signature_refresh'
        )

    def _request_all_test_document_file_signature_verify_view(self):
        return self.post(
            viewname='signatures:all_document_file_signature_verify'
        )
