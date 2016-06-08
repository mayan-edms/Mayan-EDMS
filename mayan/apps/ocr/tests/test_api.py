from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from rest_framework import status

from documents.models import DocumentType
from documents.tests import TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
from rest_api.tests import GenericAPITestCase


class OCRAPITestCase(GenericAPITestCase):
    """
    Test the OCR app API endpoints
    """

    def setUp(self):
        super(OCRAPITestCase, self).setUp()

        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object,
            )

    def tearDown(self):
        self.document_type.delete()
        super(OCRAPITestCase, self).tearDown()

    def test_submit_document(self):
        response = self.client.post(
            reverse(
                'rest_api:document-ocr-submit-view',
                args=(self.document.pk,)
            )
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        content = self.document.pages.first().ocr_content.content

        self.assertTrue('Mayan EDMS Documentation' in content)

    def test_submit_document_version(self):
        response = self.client.post(
            reverse(
                'rest_api:document-version-ocr-submit-view',
                args=(self.document.latest_version.pk,)
            )
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        content = self.document.pages.first().ocr_content.content

        self.assertTrue('Mayan EDMS Documentation' in content)

    def test_get_document_version_page_content(self):
        response = self.client.get(
            reverse(
                'rest_api:document-page-content-view',
                args=(self.document.latest_version.pages.first().pk,)
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            'Mayan EDMS Documentation' in response.data['content']
        )
