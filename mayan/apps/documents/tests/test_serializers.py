from django.http import HttpRequest

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.serializers.document_serializers import (
    DocumentFileSerializer, DocumentVersionSerializer
)


class SerializerTestMixin:
    def setUp(self):
        super().setUp()
        self.test_request = HttpRequest()
        self.test_request.META['SERVER_NAME'] = '127.0.0.1'
        self.test_request.META['SERVER_PORT'] = '80'


class DocumentFileSerializerTestCase(
    SerializerTestMixin, GenericDocumentTestCase
):
    def test_document_url(self):
        serializer = DocumentFileSerializer(
            context={'request': self.test_request},
            instance=self.test_document_file
        )

        self.assertFalse(
            self.test_document.pk == self.test_document_file.pk,
            msg='Rerun test to ensure document and document file do not have the same ID.'
        )
        self.assertTrue(
            str(self.test_document.pk) in serializer.data['document_url']
        )


class DocumentVersionSerializerTestCase(
    SerializerTestMixin, GenericDocumentTestCase
):
    def test_document_url(self):
        serializer = DocumentVersionSerializer(
            context={'request': self.test_request},
            instance=self.test_document_version
        )

        self.assertFalse(
            self.test_document.pk == self.test_document_version.pk,
            msg='Rerun test to ensure document and document version do not have the same ID.'
        )
        self.assertTrue(
            str(self.test_document.pk) in serializer.data['document_url']
        )
