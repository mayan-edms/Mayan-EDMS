from __future__ import absolute_import

import logging
import os
import subprocess

from django.utils.translation import ugettext as _

from common.conf.settings import TEMPORARY_DIRECTORY
from common.utils import fs_cleanup
from converter.api import convert
from documents.models import DocumentPage

from .conf.settings import UNPAPER_PATH, LANGUAGE
from .exceptions import UnpaperError
from .literals import (DEFAULT_OCR_FILE_FORMAT, UNPAPER_FILE_FORMAT,
    DEFAULT_OCR_FILE_EXTENSION)
from .parsers import parse_document_page
from .parsers.exceptions import ParserError, ParserUnknownFile
from .runtime import language_backend, ocr_backend

logger = logging.getLogger(__name__)


def do_document_ocr(queue_document):
    """
    Try first to extract text from document pages using the registered
    parser, if the parser fails or if there is no parser registered for
    the document mimetype do a visual OCR by calling the corresponding
    OCR backend
    """
    for document_page in queue_document.document.pages.all():
        try:
            # Try to extract text by means of a parser
            parse_document_page(document_page)
        except (ParserError, ParserUnknownFile):
            # Fall back to doing visual OCR

            document_filepath = document_page.document.get_image_cache_name(page=document_page.page_number, version=document_page.document_version.pk)
            unpaper_output_filename = u'%s_unpaper_out_page_%s%s%s' % (document_page.document.uuid, document_page.page_number, os.extsep, UNPAPER_FILE_FORMAT)
            unpaper_output_filepath = os.path.join(TEMPORARY_DIRECTORY, unpaper_output_filename)

            logger.debug('document_filepath: %s' % document_filepath)

            unpaper_input = convert(document_filepath, file_format=UNPAPER_FILE_FORMAT)

            logger.debug('unpaper_input: %s' % unpaper_input)

            execute_unpaper(input_filepath=unpaper_input, output_filepath=unpaper_output_filepath)

            logger.debug('unpaper_output_filepath: %s' % unpaper_output_filepath)

            # from PIL import Image, ImageOps
            # im = Image.open(document_filepath)
            # #if im.mode=='RGBA':
            # #    im=im.convert('RGB')
            # #im = im.convert('L')
            # im = ImageOps.grayscale(im)
            # im.save(unpaper_output_filepath)

            # Convert to TIFF
            pre_ocr_filepath = convert(input_filepath=unpaper_output_filepath, file_format=DEFAULT_OCR_FILE_FORMAT)

            logger.debug('pre_ocr_filepath: %s' % pre_ocr_filepath)

            # Tesseract needs an explicit file extension
            pre_ocr_filepath_w_ext = os.extsep.join([pre_ocr_filepath, DEFAULT_OCR_FILE_EXTENSION])

            logger.debug('pre_ocr_filepath_w_ext: %s' % pre_ocr_filepath_w_ext)

            os.rename(pre_ocr_filepath, pre_ocr_filepath_w_ext)
            try:
                ocr_text = ocr_backend.execute(pre_ocr_filepath_w_ext, LANGUAGE)

                document_page.content = ocr_cleanup(ocr_text)
                document_page.page_label = _(u'Text from OCR')
                document_page.save()
            finally:
                fs_cleanup(pre_ocr_filepath_w_ext)
                fs_cleanup(unpaper_input)
                fs_cleanup(document_filepath)
                fs_cleanup(unpaper_output_filepath)


def ocr_cleanup(text):
    """
    Cleanup the OCR's output passing it thru the selected language's
    cleanup filter
    """

    output = []
    for line in text.splitlines():
        line = line.strip()
        for word in line.split():
            if language_backend:
                result = language_backend.check_word(word)
            else:
                result = word
            if result:
                output.append(result)
        output.append(u'\n')

    return u' '.join(output)


def clean_pages():
    """
    Tool that executes the OCR cleanup code on all of the existing
    documents
    """
    for page in DocumentPage.objects.all():
        if page.content:
            page.content = ocr_cleanup(page.content)
            page.save()


def execute_unpaper(input_filepath, output_filepath):
    """
    Executes the program unpaper using subprocess's Popen
    """
    command = []
    command.append(UNPAPER_PATH)
    command.append(u'--overwrite')
    command.append(u'--no-multi-pages')
    command.append(input_filepath)
    command.append(output_filepath)
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        raise UnpaperError(proc.stderr.readline())
