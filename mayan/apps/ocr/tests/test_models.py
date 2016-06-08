# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from documents.models import DocumentType
from documents.settings import setting_language_choices
from documents.tests import (
    TEST_DEU_DOCUMENT_PATH, TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)
from organizations.tests import OrganizationTestCase


class DocumentOCRTestCase(OrganizationTestCase):
    def setUp(self):
        super(DocumentOCRTestCase, self).setUp()

        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object,
            )

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()
        super(DocumentOCRTestCase, self).tearDown()

    def test_ocr_language_backends_end(self):
        content = self.document.pages.first().ocr_content.content

        self.assertTrue('Mayan EDMS Documentation' in content)


class GermanOCRSupportTestCase(OrganizationTestCase):
    def setUp(self):
        super(GermanOCRSupportTestCase, self).setUp()

        self.document_type = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        # Get corresponding language code for German from the default language
        # choices list
        language_code = [
            language for language in setting_language_choices.value if language[1] == 'German'
        ][0][0]

        self.assertEqual('deu', language_code)

        with open(TEST_DEU_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object, language=language_code
            )

    def tearDown(self):
        self.document_type.delete()
        super(GermanOCRSupportTestCase, self).tearDown()

    def test_ocr_language_backends_end(self):
        content = self.document.pages.first().ocr_content.content

        self.assertTrue(
            'Repository für elektronische Dokumente.' in content
        )
        self.assertTrue(
            'Es bietet einen elektronischen Tresor oder' in content
        )
