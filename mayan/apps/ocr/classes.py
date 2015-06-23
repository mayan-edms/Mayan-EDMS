from __future__ import unicode_literals

import logging
import os
import tempfile

from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from common.utils import fs_cleanup
from converter import converter_class
from documents.models import DocumentPage

from .exceptions import UnpaperError
from .literals import (
    DEFAULT_OCR_FILE_EXTENSION, DEFAULT_OCR_FILE_FORMAT, UNPAPER_FILE_FORMAT
)
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
            logger.info('Processing page: %d of document version: %s', page.page_number, document_version)
            document_page_content, created = DocumentPageContent.objects.get_or_create(document_page=page)
            result =  self.execute(file_object=image, language=language)
            document_page_content.content = self.execute(file_object=image, language=language)
            document_page_content.save()
            image.close()
            logger.info('Finished processing page: %d of document version: %s', page.page_number, document_version)

    def execute(self, file_object, language=None, transformations=None):
        if not transformations:
            transformations = []

        self.converter = converter_class(file_object=file_object)

        for transformation in transformations:
            self.converter.transform(transformation=transformation)
