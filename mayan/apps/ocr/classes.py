from __future__ import unicode_literals

import logging

from converter import converter_class

from .models import DocumentPageContent

logger = logging.getLogger(__name__)


class OCRBackendBase(object):
    def process_document_version(self, document_version):
        logger.info('Starting OCR for document version: %s', document_version)
        logger.debug('document version: %d', document_version.pk)

        language = document_version.document.language

        for document_page in document_version.pages.all():
            self.process_document_page(document_page=document_page, language=language)

    def process_document_page(self, document_page, language=None):
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
                    file_object=image, language=language
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
