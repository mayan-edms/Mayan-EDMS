from django.urls import reverse

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.documents.tests.literals import TEST_SMALL_DOCUMENT_PATH

from ..links import (
    link_document_file_signature_delete,
    link_document_file_signature_details,
)
from ..permissions import (
    permission_document_file_signature_delete,
    permission_document_file_signature_view
)
from .literals import TEST_SIGNED_DOCUMENT_PATH
from .mixins import SignatureTestMixin


class DocumentSignatureLinksTestCase(
    SignatureTestMixin, GenericDocumentViewTestCase
):
    def test_document_file_signature_detail_link_no_permission(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.add_test_view(
            test_object=self.test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_details.resolve(
            context=context
        )

        self.assertEqual(resolved_link, None)

    def test_document_file_signature_detail_link_with_permission(self):
        self.test_document_path = TEST_SIGNED_DOCUMENT_PATH
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_view
        )

        self.add_test_view(
            test_object=self.test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_details.resolve(
            context=context
        )

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_signature_details.view,
                kwargs={
                    'signature_id': self.test_document.file_latest.signatures.first().pk,
                }
            )
        )

    def test_document_file_signature_delete_link_no_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.add_test_view(
            test_object=self.test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_delete.resolve(
            context=context
        )
        self.assertEqual(resolved_link, None)

    def test_document_file_signature_delete_link_with_permission(self):
        self.test_document_path = TEST_SMALL_DOCUMENT_PATH
        self._upload_test_document()

        self._upload_test_detached_signature()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_signature_delete
        )

        self.add_test_view(
            test_object=self.test_document.file_latest.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_file_signature_delete.resolve(
            context=context
        )
        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                viewname=link_document_file_signature_delete.view,
                kwargs={
                    'signature_id': self.test_document.file_latest.signatures.first().pk,
                }
            )
        )
