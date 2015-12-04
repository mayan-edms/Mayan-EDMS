# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.files.base import File
from django.test import TestCase

from documents.models import DocumentType
from documents.settings import setting_language_choices
from documents.tests import (
    TEST_DEU_DOCUMENT_PATH, TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)


class DocumentOCRTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object),
            )

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()

    def test_ocr_language_backends_end(self):
        content = self.document.pages.first().ocr_content.content

        self.assertTrue('Mayan EDMS Documentation' in content)


class GermanOCRSupportTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
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
                file_object=File(file_object), language=language_code
            )

    def tearDown(self):
        self.document_type.delete()

    def test_ocr_language_backends_end(self):
        content = self.document.pages.first().ocr_content.content

        self.assertTrue(
            'Repository für elektronische Dokumente.' in content
        )
        self.assertTrue(
            'Es bietet einen elektronischen Tresor oder' in content
        )
