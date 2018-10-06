from __future__ import unicode_literals

from django.core.files import File
from django.urls import reverse

from documents.tests import (
    GenericDocumentViewTestCase, TEST_DOCUMENT_PATH
)

from ..links import (
    link_document_version_signature_delete,
    link_document_version_signature_details,
)
from ..models import DetachedSignature
from ..permissions import (
    permission_document_version_signature_delete,
    permission_document_version_signature_view
)
from .literals import TEST_SIGNATURE_FILE_PATH, TEST_SIGNED_DOCUMENT_PATH


class DocumentSignatureLinksTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentSignatureLinksTestCase, self).setUp()
        self.login_user()

    def test_document_version_signature_detail_link_no_permission(self):
        with open(TEST_SIGNED_DOCUMENT_PATH, mode='rb') as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        self.add_test_view(
            test_object=document.latest_version.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_version_signature_details.resolve(
            context=context
        )

        self.assertEqual(resolved_link, None)

    def test_document_version_signature_detail_link_with_permission(self):
        with open(TEST_SIGNED_DOCUMENT_PATH, mode='rb') as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        self.role.permissions.add(
            permission_document_version_signature_view.stored_permission
        )

        self.add_test_view(
            test_object=document.latest_version.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_version_signature_details.resolve(
            context=context
        )

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                'signatures:document_version_signature_details',
                args=(document.latest_version.signatures.first().pk,)
            )
        )

    def test_document_version_signature_delete_link_no_permission(self):
        with open(TEST_DOCUMENT_PATH, mode='rb') as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.add_test_view(
            test_object=document.latest_version.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_version_signature_delete.resolve(
            context=context
        )

        self.assertEqual(resolved_link, None)

    def test_document_version_signature_delete_link_with_permission(self):
        with open(TEST_DOCUMENT_PATH, mode='rb') as file_object:
            document = self.document_type.new_document(
                file_object=file_object
            )

        with open(TEST_SIGNATURE_FILE_PATH, mode='rb') as file_object:
            DetachedSignature.objects.create(
                document_version=document.latest_version,
                signature_file=File(file_object)
            )

        self.role.permissions.add(
            permission_document_version_signature_delete.stored_permission
        )

        self.add_test_view(
            test_object=document.latest_version.signatures.first()
        )
        context = self.get_test_view()
        resolved_link = link_document_version_signature_delete.resolve(
            context=context
        )

        self.assertNotEqual(resolved_link, None)
        self.assertEqual(
            resolved_link.url,
            reverse(
                'signatures:document_version_signature_delete',
                args=(document.latest_version.signatures.first().pk,)
            )
        )
