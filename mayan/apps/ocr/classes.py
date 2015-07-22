from __future__ import unicode_literals

import logging

from converter import converter_class

from .models import DocumentPageContent
from .parsers import parse_document_page
from .parsers.exceptions import ParserError, ParserUnknownFile

logger = logging.getLogger(__name__)


class OCRBackendBase(object):
    def process_document_version(self, document_version):
        logger.info('Starting OCR for document version: %s', document_version)
        logger.debug('document version: %d', document_version.pk)

        language = document_version.document.language

        for page in document_version.pages.all():
            image = page.get_image()
            logger.info(
                'Processing page: %d of document version: %s',
                page.page_number, document_version
            )
            document_page_content, created = DocumentPageContent.objects.get_or_create(document_page=page)
            document_page_content.content = self.execute(
                file_object=image, language=language
            )
            document_page_content.save()
            image.close()
            logger.info(
                'Finished processing page: %d of document version: %s',
                page.page_number, document_version
            )

    def execute(self, file_object, language=None, transformations=None):
        self.language = language

        if not transformations:
            transformations = []

        self.converter = converter_class(file_object=file_object)

        for transformation in transformations:
            self.converter.transform(transformation=transformation)
