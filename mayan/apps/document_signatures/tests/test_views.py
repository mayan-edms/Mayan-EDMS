from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.models import DocumentFile
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import (
    TEST_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH
)

from ..models import DetachedSignature, EmbeddedSignature
from ..permissions import (
    permission_document_file_sign_detached,
    permission_document_file_sign_embedded,
    permission_document_file_signature_delete,
    permission_document_file_signature_download,
    permission_document_file_signature_upload,
    permission_document_file_signature_verify,
    permission_document_file_signature_view
)

from .literals import (
    TEST_SIGNED_DOCUMENT_COUNT, TEST_SIGNED_DOCUMENT_PATH,
    TEST_UNSIGNED_DOCUMENT_COUNT
)
from .mixins import (
    DetachedSignatureViewTestMixin, EmbeddedSignatureViewTestMixin,
    SignatureTestMixin, SignatureToolsViewTestMixin, SignatureViewTestMixin
)


class SignaturesViewTestCase(
    KeyTestMixin, SignatureTestMixin, SignatureViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_signature_delete_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature_count = DetachedSignature.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        response = self._request_test_document_file_signature_delete_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(DetachedSignature.objects.count(), signature_count)

    def test_signature_delete_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature_count = DetachedSignature.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_delete
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        response = self._request_test_document_file_signature_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            DetachedSignature.objects.count(), signature_count - 1
        )

    def test_trashed_document_signature_delete_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature_count = DetachedSignature.objects.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_delete
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_signature_delete_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            DetachedSignature.objects.count(), signature_count
        )

    def test_signature_detail_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._upload_test_detached_signature()

        response = self._request_test_document_file_signature_details_view()
        self.assertEqual(response.status_code, 404)

    def test_signature_detail_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._create_test_key_public()
        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        response = self._request_test_document_file_signature_details_view()
        self.assertContains(
            response=response, text=self.test_signature.signature_id,
            status_code=200
        )

    def test_trashed_document_signature_detail_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._create_test_key_public()
        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_signature_details_view()
        self.assertEqual(response.status_code, 404)

    def test_signature_list_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        response = self._request_test_document_file_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 404)

    def test_signature_list_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        response = self._request_test_document_file_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)

    def test_trashed_document_signature_list_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self.test_document.delete()

        response = self._request_test_document_file_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 404)


class DetachedSignaturesViewTestCase(
    KeyTestMixin, SignatureTestMixin, DetachedSignatureViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_detached_signature_create_view_with_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

    def test_detached_signature_create_view_with_document_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_detached
        )

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

    def test_detached_signature_create_view_with_key_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

    def test_detached_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_detached
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count + 1
        )

    def test_trashed_document_detached_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_detached
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        self.test_document.delete()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

    def test_signature_download_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        response = self._request_test_document_file_signature_download_view()
        self.assertEqual(response.status_code, 404)

    def test_signature_download_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_download
        )

        self.expected_content_types = ('application/octet-stream',)

        response = self._request_test_document_file_signature_download_view()

        with self.test_signature.signature_file as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
            )

    def test_trashed_document_signature_download_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_download
        )

        self.test_document.delete()

        response = self._request_test_document_file_signature_download_view()
        self.assertEqual(response.status_code, 404)

    def test_signature_upload_view_no_permission(self):
        self.test_document_path = TEST_DOCUMENT_PATH

        signature_count = DetachedSignature.objects.count()

        self._upload_test_document()

        response = self._request_test_document_file_signature_upload_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DetachedSignature.objects.count(), signature_count)

    def test_signature_upload_view_with_access(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_upload
        )

        signature_count = DetachedSignature.objects.count()

        response = self._request_test_document_file_signature_upload_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DetachedSignature.objects.count(), signature_count + 1
        )

    def test_trashed_document_signature_upload_view_with_access(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_upload
        )

        self.test_document.delete()

        signature_count = DetachedSignature.objects.count()

        response = self._request_test_document_file_signature_upload_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(DetachedSignature.objects.count(), signature_count)


class EmbeddedSignaturesViewTestCase(
    KeyTestMixin, EmbeddedSignatureViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_embedded_signature_create_view_with_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

    def test_embedded_signature_create_view_with_document_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_embedded
        )

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

    def test_embedded_signature_create_view_with_key_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )

    def test_embedded_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_embedded
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            str(self.test_document.file_latest.pk) in response.url
        )

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count + 1
        )

    def test_trashed_document_embedded_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._create_test_key_private()

        signature_count = self.test_document.file_latest.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_sign_embedded
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        self.test_document.delete()

        response = self._request_test_document_file_signature_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.signatures.count(),
            signature_count
        )


class SignatureToolsViewTestCase(
    KeyTestMixin, SignatureTestMixin, SignatureToolsViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class DetachedSignatureProxy(DetachedSignature):
            def save(self, *args, **kwargs):
                return super(DetachedSignature, self).save(*args, **kwargs)

            class Meta:
                proxy = True

        class EmbeddedSignatureProxy(EmbeddedSignature):
            def save(self, *args, **kwargs):
                return super(EmbeddedSignature, self).save(*args, **kwargs)

            class Meta:
                proxy = True

        cls.DetachedSignatureProxy = DetachedSignatureProxy
        cls.EmbeddedSignatureProxy = EmbeddedSignatureProxy

    def test_missing_signature_verify_view_no_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentFile._post_save_hooks
        DocumentFile._post_save_hooks = {}

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        DocumentFile._post_save_hooks = old_hooks

        response = self._request_all_test_document_file_signature_verify_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

    def test_missing_signature_verify_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentFile._post_save_hooks
        DocumentFile._post_save_hooks = {}

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        DocumentFile._post_save_hooks = old_hooks

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        response = self._request_all_test_document_file_signature_verify_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

    def test_trashed_document_missing_signature_verify_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        old_hooks = DocumentFile._post_save_hooks
        DocumentFile._post_save_hooks = {}

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self._upload_test_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        DocumentFile._post_save_hooks = old_hooks

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        self.test_document.delete()

        response = self._request_all_test_document_file_signature_verify_view()

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_files().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )

    def test_signature_refresh_view_no_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature = self.DetachedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        signature = self.EmbeddedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        response = self._request_all_test_document_file_signature_refresh_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            DetachedSignature.objects.first().date_time,
            None
        )
        self.assertEqual(
            EmbeddedSignature.objects.first().date_time,
            None
        )

    def test_signature_refresh_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature = self.DetachedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        signature = self.EmbeddedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        response = self._request_all_test_document_file_signature_refresh_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            DetachedSignature.objects.first().date_time,
            None
        )
        self.assertNotEqual(
            EmbeddedSignature.objects.first().date_time,
            None
        )

    def test_trashed_document_signature_refresh_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        signature = self.DetachedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        signature = self.EmbeddedSignatureProxy.objects.first()
        signature.date_time = None
        signature.save()

        self.test_documents[0].delete()
        self.test_documents[1].delete()

        self.grant_permission(
            permission=permission_document_file_signature_verify
        )

        response = self._request_all_test_document_file_signature_refresh_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            DetachedSignature.objects.first().date_time,
            None
        )
        self.assertNotEqual(
            EmbeddedSignature.objects.first().date_time,
            None
        )
