from __future__ import unicode_literals

import logging
import os
import tempfile

import sh

from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from common.settings import TEMPORARY_DIRECTORY
from common.utils import fs_cleanup
from converter import converter_class
from documents.models import DocumentPage

from .exceptions import UnpaperError
from .literals import (
    DEFAULT_OCR_FILE_EXTENSION, DEFAULT_OCR_FILE_FORMAT, UNPAPER_FILE_FORMAT
)
from .parsers import parse_document_page
from .parsers.exceptions import ParserError, ParserUnknownFile
from .settings import UNPAPER_PATH

logger = logging.getLogger(__name__)


class OCRBackendBase(object):
    def process_document_version(self, document_version):
        logger.info('Starting OCR for document version: %s', document_version)
        logger.debug('document version: %d', document_version.pk)

        language = document_version.document.language

        for page in document_version.pages.all():
            image = page.get_image()
            logger.info('Processing page: %d', page.page_number)
            page.content = self.execute(file_object=image, language=language)
            page.save()
            image.close()
            logger.info('Finished processing page: %d', page.page_number)

    def execute(self, file_object, language=None, transformations=None):
        if not transformations:
            transformations = []

        self.converter = converter_class(file_object=file_object)

        for transformation in transformations:
            self.converter.transform(transformation=transformation)
