# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.base import File
from django.test import TestCase

from documents.models import DocumentType
from documents.settings import setting_language_choices
from documents.test_models import (
    TEST_DOCUMENT_PATH, TEST_DOCUMENT_TYPE, TEST_SMALL_DOCUMENT_PATH
)

from .parsers import PDFMinerParser, PopplerParser


class ParserTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE
        )

        ocr_settings = self.document_type.ocr_settings
        ocr_settings.auto_ocr = False
        ocr_settings.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(
                file_object=File(file_object)
            )

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()

    def test_pdfminer_parser(self):
        parser = PDFMinerParser()

        parser.process_document_version(self.document.latest_version)

        self.assertTrue(
            'Mayan EDMS Documentation' in self.document.pages.first().ocr_content.content
        )

    def test_poppler_parser(self):
        parser = PopplerParser()

        parser.process_document_version(self.document.latest_version)

        self.assertTrue(
            'Mayan EDMS Documentation' in self.document.pages.first().ocr_content.content
        )
