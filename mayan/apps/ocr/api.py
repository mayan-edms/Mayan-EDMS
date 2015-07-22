from __future__ import unicode_literals

import logging
import os
import tempfile

import sh

from common.settings import setting_temporary_directory

from .exceptions import UnpaperError
from .parsers import parse_document_page
from .parsers.exceptions import ParserError, ParserUnknownFile
from .settings import UNPAPER_PATH

logger = logging.getLogger(__name__)

try:
    UNPAPER = sh.Command(UNPAPER_PATH).bake(
        overwrite=True, no_multi_pages=True
    )
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
            fd, output_filepath = tempfile.mkstemp(
                dir=setting_temporary_directory.value
            )

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
