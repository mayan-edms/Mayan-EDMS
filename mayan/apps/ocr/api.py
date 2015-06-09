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
from .runtime import ocr_backend
from .settings import UNPAPER_PATH

logger = logging.getLogger(__name__)

try:
    UNPAPER = sh.Command(UNPAPER_PATH).bake(overwrite=True, no_multi_pages=True)
except sh.CommandNotFound:
    logger.debug('unpaper not found')
    UNPAPER = None

"""
for document_page in document_version.pages.all():
    try:
        # Try to extract text by means of a parser
        parse_document_page(document_page)
    except (ParserError, ParserUnknownFile):
        # Fall back to doing visual OCR
"""


def execute_unpaper(input_filepath, output_filepath=None):
    """
    Executes the program unpaper using subprocess's Popen
    """
    if UNPAPER:
        if not output_filepath:
            fd, output_filepath = tempfile.mkstemp(dir=TEMPORARY_DIRECTORY)

        try:
            UNPAPER(input_filepath, output_filepath)
        except sh.ErrorReturnCode as exception:
            logger.error(exception)
            raise UnpaperError(exception.stderr)
        else:
            return output_filepath
        finally:
            os.close(fd)
    else:
        return input_filepath
