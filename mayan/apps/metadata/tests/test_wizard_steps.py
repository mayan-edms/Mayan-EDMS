from __future__ import unicode_literals

from furl import furl

from django.urls import reverse

from documents.models import Document
from documents.permissions import permission_document_create
from documents.tests import (
    GenericDocumentViewTestCase, TEST_SMALL_DOCUMENT_PATH,
)
from metadata.tests.literals import TEST_METADATA_VALUE_UNICODE
from metadata.tests.mixins import MetadataTypeMixin

from sources.models import WebFormSource

from sources.tests.literals import (
    TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N,
)


class DocumentUploadMetadataTestCase(MetadataTypeMixin, GenericDocumentViewTestCase):
    def setUp(self):
        super(DocumentUploadMetadataTestCase, self).setUp()
        self.login_user()
        self.source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS_N
        )

        self.document.delete()

        self.document_type.metadata.create(
            metadata_type=self.metadata_type, required=True
        )

    def test_unicode_interactive_with_unicode_metadata(self):
        url = furl(reverse('sources:upload_interactive'))
        url.args['metadata0_id'] = self.metadata_type.pk
        url.args['metadata0_value'] = TEST_METADATA_VALUE_UNICODE

        self.grant_access(
            permission=permission_document_create, obj=self.document_type
        )
        # Upload the test document
        with open(TEST_SMALL_DOCUMENT_PATH) as file_descriptor:
            response = self.post(
                path=url, data={
                    'document-language': 'eng', 'source-file': file_descriptor,
                    'document_type_id': self.document_type.pk,
                }
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(
            Document.objects.first().metadata.first().value,
            TEST_METADATA_VALUE_UNICODE
        )
