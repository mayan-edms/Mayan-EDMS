from django.http import HttpRequest

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.serializers.document_serializers import (
    DocumentFileSerializer, DocumentVersionSerializer
)


class SerializerTestMixin:
    def setUp(self):
        super().setUp()
        self._test_request = HttpRequest()
        self._test_request.META['SERVER_NAME'] = '127.0.0.1'
        self._test_request.META['SERVER_PORT'] = '80'


class DocumentFileSerializerTestCase(
    SerializerTestMixin, GenericDocumentTestCase
):
    def test_document_url(self):
        serializer = DocumentFileSerializer(
            context={'request': self._test_request},
            instance=self._test_document_file
        )

        self.assertFalse(
            self._test_document.pk == self._test_document_file.pk,
            msg='Rerun test to ensure document and document file do not have the same ID.'
        )
        self.assertTrue(
            str(self._test_document.pk) in serializer.data['document_url']
        )


class DocumentVersionSerializerTestCase(
    SerializerTestMixin, GenericDocumentTestCase
):
    def test_document_url(self):
        serializer = DocumentVersionSerializer(
            context={'request': self._test_request},
            instance=self._test_document_version
        )

        self.assertFalse(
            self._test_document.pk == self._test_document_version.pk,
            msg='Rerun test to ensure document and document version do not have the same ID.'
        )
        self.assertTrue(
            str(self._test_document.pk) in serializer.data['document_url']
        )
