from __future__ import unicode_literals

import logging
import os
import tempfile

import sh

from django.utils.translation import ugettext as _

from common.settings import TEMPORARY_DIRECTORY
from common.utils import fs_cleanup, load_backend
from converter.api import convert
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


def do_document_ocr(document_version):
    """
    Try first to extract text from document pages using the registered
    parser, if the parser fails or if there is no parser registered for
    the document mimetype do a visual OCR by calling the corresponding
    OCR backend
    """
    for document_page in document_version.pages.all():
        try:
            # Try to extract text by means of a parser
            parse_document_page(document_page)
        except (ParserError, ParserUnknownFile):
            # Fall back to doing visual OCR

            document_filepath = document_page.document.get_image_cache_name(page=document_page.page_number, version=document_page.document_version.pk)

            logger.debug('document_filepath: %s', document_filepath)

            unpaper_input = convert(document_filepath, file_format=UNPAPER_FILE_FORMAT)

            logger.debug('unpaper_input: %s', unpaper_input)

            unpaper_output = execute_unpaper(input_filepath=unpaper_input)

            logger.debug('unpaper_output: %s', unpaper_output)

            # Convert to TIFF
            pre_ocr_filepath = convert(input_filepath=unpaper_output, file_format=DEFAULT_OCR_FILE_FORMAT)

            logger.debug('pre_ocr_filepath: %s', pre_ocr_filepath)

            # Tesseract needs an explicit file extension
            pre_ocr_filepath_w_ext = os.extsep.join([pre_ocr_filepath, DEFAULT_OCR_FILE_EXTENSION])

            logger.debug('pre_ocr_filepath_w_ext: %s', pre_ocr_filepath_w_ext)

            os.rename(pre_ocr_filepath, pre_ocr_filepath_w_ext)
            try:
                ocr_text = ocr_backend.execute(pre_ocr_filepath_w_ext, document_version.document.language)

                document_page.content = ocr_cleanup(document_version.document.language, ocr_text)
                document_page.page_label = _('Text from OCR')
                document_page.save()
            finally:
                fs_cleanup(pre_ocr_filepath_w_ext)
                fs_cleanup(unpaper_input)
                fs_cleanup(document_filepath)
                fs_cleanup(unpaper_output)


def ocr_cleanup(language, text):
    """
    Cleanup the OCR's output passing it thru the selected language's
    cleanup filter
    """
    try:
        language_backend = load_backend('.'.join(['ocr', 'lang', language, 'LanguageBackend']))()
    except ImportError:
        language_backend = None

    output = []
    for line in text.splitlines():
        line = line.strip()
        for word in line.split():
            if language_backend:
                try:
                    result = language_backend.check_word(word)
                except Exception as exception:
                    logger.error(exception)
                    raise Exception('ocr_cleanup() %s' % unicode(exception))
            else:
                result = word
            if result:
                output.append(result)
        output.append('\n')

    return ' '.join(output)


def clean_pages():
    """
    Tool that executes the OCR cleanup code on all of the existing
    documents
    """
    for page in DocumentPage.objects.all():
        if page.content:
            page.content = ocr_cleanup(page.document.language, page.content)
            page.save()


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
