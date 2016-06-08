from __future__ import unicode_literals

from django.test import override_settings

from documents.models import DocumentType
from documents.tests.literals import (
    TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)
from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import DocumentPageContent


@override_settings(OCR_AUTO_OCR=False)
class OrganizationOCRViewTestCase(OrganizationViewTestCase):
    def create_document_type(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.document_type = DocumentType.on_organization.create(
                label=TEST_DOCUMENT_TYPE
            )

    def create_document(self):
        self.create_document_type()
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):

            with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
                self.document = self.document_type.new_document(
                    file_object=file_object
                )

    def test_document_content_view(self):
        self.create_document()
        self.document.submit_for_ocr()

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.get(
                'ocr:document_content', args=(self.document.pk,)
            )
            self.assertContains(response, text='Mayan', status_code=200)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get(
                'ocr:document_content', args=(self.document.pk,)
            )
            self.assertEqual(response.status_code, 404)

    def test_document_submit_view(self):
        self.create_document()

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'ocr:document_submit', args=(self.document.pk,), follow=True
            )
            self.assertContains(response, text='uccess', status_code=200)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'ocr:document_submit', args=(self.document.pk,), follow=True
            )
            self.assertEqual(response.status_code, 404)

    def test_document_submit_all_view(self):
        self.create_document()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.post('ocr:document_submit_all', follow=True)

            with self.assertRaises(DocumentPageContent.DoesNotExist):
                # Use .objects manager to make sure we get all document pages
                # and that it indeed doesn't exists = no OCR happened.
                DocumentPageContent.objects.get(
                    document_page=self.document.pages.first()
                )

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.post('ocr:document_submit_all', follow=True)

            self.assertIn(
                'Mayan', self.document.pages.first().ocr_content.content
            )

    def test_document_type_ocr_settings_view(self):
        self.create_document_type()

        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.get(
                'ocr:document_type_ocr_settings', args=(self.document_type.pk,)
            )
            self.assertEqual(response.status_code, 200)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.get(
                'ocr:document_type_ocr_settings', args=(self.document_type.pk,)
            )
            self.assertEqual(response.status_code, 404)
