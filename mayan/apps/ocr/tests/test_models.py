# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from common.tests import BaseTestCase
from documents.models import DocumentType
from documents.runtime import language_choices
from documents.tests import (
    DocumentTestMixin, TEST_DEU_DOCUMENT_PATH, TEST_DOCUMENT_TYPE_LABEL
)

TEST_DOCUMENT_CONTENT = 'Mayan EDMS Documentation'
TEST_DOCUMENT_CONTENT_DEU_1 = 'Repository für elektronische Dokumente.'
TEST_DOCUMENT_CONTENT_DEU_2 = 'Es bietet einen'


class DocumentOCRTestCase(DocumentTestMixin, BaseTestCase):
    # PyOCR's leak descriptor in get_available_languages and image_to_string
    # Disable descriptor leak test until fixed in upstream
    _skip_file_descriptor_test = True

    def test_ocr_language_backends_end(self):
        content = self.document.pages.first().ocr_content.content
        self.assertTrue(TEST_DOCUMENT_CONTENT in content)


class GermanOCRSupportTestCase(BaseTestCase):
    # PyOCR's leak descriptor in get_available_languages and image_to_string
    # Disable descriptor leak test until fixed in upstream
    _skip_file_descriptor_test = True

    def setUp(self):
        super(GermanOCRSupportTestCase, self).setUp()

        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        # Get corresponding language code for German from the default language
        # choices list
        language_code = [
            language for language in language_choices if language[1] == 'German'
        ][0][0]

        self.assertEqual('deu', language_code)

        with open(TEST_DEU_DOCUMENT_PATH, mode='rb') as file_object:
            self.document = self.document_type.new_document(
                file_object=file_object, language=language_code
            )

    def tearDown(self):
        self.document_type.delete()
        super(GermanOCRSupportTestCase, self).tearDown()

    def test_ocr_language_backends_end(self):
        content = self.document.pages.first().ocr_content.content

        self.assertTrue(
            TEST_DOCUMENT_CONTENT_DEU_1 in content
        )
        self.assertTrue(
            TEST_DOCUMENT_CONTENT_DEU_2 in content
        )
