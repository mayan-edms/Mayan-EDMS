from mayan.apps.django_gpg.tests.mixins import KeyTestMixin
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from ..permissions import permission_document_file_signature_view

from .mixins import DetachedSignatureTestMixin, SignatureViewTestMixin


class SignaturesViewTestCase(
    KeyTestMixin, DetachedSignatureTestMixin, SignatureViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_signature_detail_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()
        self._upload_test_detached_signature()

        self._clear_events()

        response = self._request_test_document_file_signature_details_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_detail_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._create_test_key_public()
        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self._clear_events()

        response = self._request_test_document_file_signature_details_view()
        self.assertContains(
            response=response, text=self.test_signature.signature_id,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        self._clear_events()

        response = self._request_test_document_file_signature_details_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_list_view_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self._clear_events()

        response = self._request_test_document_file_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_signature_list_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self._clear_events()

        response = self._request_test_document_file_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_signature_list_view_with_access(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_file_signature_list_view(
            document=self.test_document
        )
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
