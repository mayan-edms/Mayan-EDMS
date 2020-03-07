from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.django_gpg.permissions import permission_key_sign
from mayan.apps.django_gpg.tests.literals import TEST_KEY_PUBLIC_ID
from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import (
    permission_document_version_sign_detached,
    permission_document_version_sign_embedded,
    permission_document_version_signature_delete,
    permission_document_version_signature_view,
    permission_document_version_signature_upload
)

from .literals import TEST_SIGNED_DOCUMENT_PATH
from .mixins import (
    DetachedSignatureAPIViewTestMixin, EmbeddedSignatureAPIViewTestMixin,
    SignatureTestMixin
)


class DetachedSignatureDocumentAPIViewTestCase(
    DocumentTestMixin, DetachedSignatureAPIViewTestMixin,
    KeyTestMixin, SignatureTestMixin, BaseAPITestCase
):
    auto_upload_document = False

    def test_document_signature_detached_create_view_no_permission(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        response = self._request_test_document_signature_detached_create_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_detached_create_view_with_access(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_upload
        )

        response = self._request_test_document_signature_detached_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures + 1
        )

    def test_document_signature_detached_delete_no_permission(self):
        self.upload_document()
        self._upload_test_detached_signature()

        signatures = self.test_document.latest_version.signatures.count()

        response = self._request_test_document_signature_detached_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_detached_delete_with_access(self):
        self.upload_document()
        self._upload_test_detached_signature()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_delete
        )

        response = self._request_test_document_signature_detached_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures - 1
        )

    def test_document_signature_detached_detail_no_permission(self):
        self.upload_document()
        self._upload_test_detached_signature()

        response = self._request_test_document_signature_detached_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_signature_detached_detail_with_access(self):
        self.upload_document()
        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_signature_detached_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['key_id'], TEST_KEY_PUBLIC_ID
        )

    def test_document_signature_detached_list_view_no_permission(self):
        self.upload_document()
        self._upload_test_detached_signature()

        response = self._request_test_document_signature_detached_list_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_signature_detached_list_view_with_access(self):
        self.upload_document()
        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_signature_detached_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['key_id'], TEST_KEY_PUBLIC_ID
        )

    def test_document_signature_detached_sign_view_with_no_permission(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        response = self._request_test_document_signature_detached_sign_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_detached_sign_view_with_document_access(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_sign_detached
        )

        response = self._request_test_document_signature_detached_sign_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_detached_sign_view_with_key_access(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_signature_detached_sign_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_detached_sign_view_with_full_access(self):
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

        response = self._request_test_document_signature_detached_sign_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures + 1
        )


class EmbeddedSignatureDocumentAPIViewTestCase(
    DocumentTestMixin, EmbeddedSignatureAPIViewTestMixin,
    KeyTestMixin, BaseAPITestCase
):
    auto_upload_document = False

    def test_document_signature_embedded_sign_view_with_no_permission(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        response = self._request_test_document_signature_embedded_sign_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_embedded_sign_view_with_document_access(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_sign_embedded
        )

        response = self._request_test_document_signature_embedded_sign_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_embedded_sign_view_with_key_access(self):
        self.upload_document()
        self._create_test_key_private()

        signatures = self.test_document.latest_version.signatures.count()

        self.grant_access(
            obj=self.test_key_private,
            permission=permission_key_sign
        )

        response = self._request_test_document_signature_embedded_sign_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures
        )

    def test_document_signature_embedded_sign_view_with_full_access(self):
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

        response = self._request_test_document_signature_embedded_sign_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            self.test_document.latest_version.signatures.count(),
            signatures + 1
        )

    def test_document_signature_embedded_detail_no_permission(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        response = self._request_test_document_signature_embedded_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_signature_embedded_detail_with_access(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_signature_embedded_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['key_id'], TEST_KEY_PUBLIC_ID
        )

    def test_document_signature_embedded_list_view_no_permission(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        response = self._request_test_document_signature_embedded_list_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_signature_embedded_list_view_with_access(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self.upload_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_version_signature_view
        )

        response = self._request_test_document_signature_embedded_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['key_id'], TEST_KEY_PUBLIC_ID
        )
