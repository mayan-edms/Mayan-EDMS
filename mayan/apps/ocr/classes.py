from __future__ import unicode_literals

import logging

from django.utils.module_loading import import_string

from converter import converter_class

from .exceptions import NoMIMETypeMatch, ParserError
from .models import DocumentPageContent
from .parsers import Parser
from .settings import setting_ocr_backend

logger = logging.getLogger(__name__)


class TextExtractor(object):
    @classmethod
    def perform_ocr(cls, document_page):
        ocr_backend_class = import_string(setting_ocr_backend.value)
        backend = ocr_backend_class()
        backend.process_document_page(document_page)

    @classmethod
    def process_document_page(cls, document_page):
        """
        Extract text for a document version's page. Try parsing the page and if
        no there are not parsers for the MIME type or the parser return nothing
        fallback to doing and OCR of the page.
        """

        try:
            Parser.parse_document_page(document_page=document_page)
        except (NoMIMETypeMatch, ParserError):
            cls.perform_ocr(document_page=document_page)
        else:
            if not document_page.ocr_content.content:
                cls.perform_ocr(document_page=document_page)

    @classmethod
    def process_document_version(cls, document_version):
        for document_page in document_version.pages.all():
            cls.process_document_page(document_page=document_page)


class OCRBackendBase(object):
    def process_document_version(self, document_version):
        logger.info('Starting OCR for document version: %s', document_version)
        logger.debug('document version: %d', document_version.pk)

        for document_page in document_version.pages.all():
            self.process_document_page(document_page=document_page)

    def process_document_page(self, document_page):
            logger.info(
                'Processing page: %d of document version: %s',
                document_page.page_number, document_page.document_version
            )

            image = document_page.get_image()

            try:
                document_page_content, created = DocumentPageContent.objects.get_or_create(
                    document_page=document_page
                )
                document_page_content.content = self.execute(
                    file_object=image, language=document_page.document.language
                )
                document_page_content.save()
            finally:
                image.close()

            logger.info(
                'Finished processing page: %d of document version: %s',
                document_page.page_number, document_page.document_version
            )

    def execute(self, file_object, language=None, transformations=None):
        self.language = language

        if not transformations:
            transformations = []

        self.converter = converter_class(file_object=file_object)

        for transformation in transformations:
            self.converter.transform(transformation=transformation)
