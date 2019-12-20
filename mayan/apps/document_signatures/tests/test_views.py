from __future__ import absolute_import, unicode_literals

from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.models import DocumentVersion
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import (
    TEST_DOCUMENT_PATH, TEST_SMALL_DOCUMENT_PATH
)

from ..models import DetachedSignature, EmbeddedSignature
from ..permissions import (
    permission_document_version_sign_detached,
    permission_document_version_sign_embedded,
    permission_document_version_signature_delete,
    permission_document_version_signature_download,
    permission_document_version_signature_upload,
    permission_document_version_signature_verify,
    permission_document_version_signature_view
)

from .literals import TEST_SIGNED_DOCUMENT_PATH
from .mixins import (
    DetachedSignatureViewTestMixin, EmbeddedSignatureViewTestMixin,
    SignatureTestMixin, SignatureViewTestMixin
)

TEST_UNSIGNED_DOCUMENT_COUNT = 4
TEST_SIGNED_DOCUMENT_COUNT = 2


class SignaturesViewTestCase(
    SignatureTestMixin, SignatureViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_document = False

    def test_signature_delete_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_version_signature_delete_view()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(DetachedSignature.objects.count(), 1)

    def test_signature_delete_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_delete
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_version_signature_delete_view()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DetachedSignature.objects.count(), 0)

    def test_signature_detail_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        response = self._request_test_document_version_signature_details_view()
        self.assertEqual(response.status_code, 404)

    def test_signature_detail_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_version_signature_details_view()
        self.assertContains(
            response=response, text=self.test_signature.signature_id,
            status_code=200
        )

    def test_signature_list_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        response = self._request_test_document_version_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 404)

    def test_signature_list_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_version_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)

    def test_missing_signature_verify_view_no_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        for document in self.test_document_type.documents.all():
            document.delete(to_trash=False)

        old_hooks = DocumentVersion._post_save_hooks
        DocumentVersion._post_save_hooks = {}

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_versions().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        DocumentVersion._post_save_hooks = old_hooks

        response = self._request_all_test_document_version_signature_verify_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_versions().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

    def test_missing_signature_verify_view_with_permission(self):
        # Silence converter logging
        self._silence_logger(name='mayan.apps.converter.backends')

        for document in self.test_document_type.documents.all():
            document.delete(to_trash=False)

        old_hooks = DocumentVersion._post_save_hooks
        DocumentVersion._post_save_hooks = {}

        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        for count in range(TEST_UNSIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        for count in range(TEST_SIGNED_DOCUMENT_COUNT):
            self.upload_document()

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_versions().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT + TEST_SIGNED_DOCUMENT_COUNT
        )

        DocumentVersion._post_save_hooks = old_hooks

        self.grant_permission(
            permission=permission_document_version_signature_verify
        )

        response = self._request_all_test_document_version_signature_verify_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            EmbeddedSignature.objects.unsigned_document_versions().count(),
            TEST_UNSIGNED_DOCUMENT_COUNT
        )


class DetachedSignaturesViewTestCase(
    KeyTestMixin, SignatureTestMixin, DetachedSignatureViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_document = False

    def test_detached_signature_create_view_with_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_detached_signature_create_view_with_document_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_sign_detached
        )

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_detached_signature_create_view_with_key_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_detached_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_sign_detached
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures + 1
        )

    def test_signature_download_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        response = self._request_test_document_version_signature_download_view()
        self.assertEqual(response.status_code, 404)

    def test_signature_download_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()

        self._create_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_download
        )

        self.expected_content_types = ('application/octet-stream',)

        response = self._request_test_document_version_signature_download_view()

        with self.test_signature.signature_file as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
            )

    def test_signature_upload_view_no_permission(self):
        self.test_document_path = TEST_DOCUMENT_PATH

        self.upload_document()

        response = self._request_test_document_version_signature_upload_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(DetachedSignature.objects.count(), 0)

    def test_signature_upload_view_with_access(self):
        self.test_document_path = TEST_DOCUMENT_PATH
        self.upload_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_upload
        )

        response = self._request_test_document_version_signature_upload_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(DetachedSignature.objects.count(), 1)


class EmbeddedSignaturesViewTestCase(
    KeyTestMixin, EmbeddedSignatureViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_document = False

    def test_embedded_signature_create_view_with_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_embedded_signature_create_view_with_document_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_sign_embedded
        )

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_embedded_signature_create_view_with_key_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_embedded_signature_create_view_with_full_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_sign_embedded
        )
        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_version_signature_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures + 1
        )
