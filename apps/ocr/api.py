#Some code from http://wiki.github.com/hoffstaetter/python-tesseract
from __future__ import absolute_import

import codecs
import os
import subprocess
import tempfile
import sys

from django.utils.translation import ugettext as _
from django.utils.importlib import import_module

from common.settings import TEMPORARY_DIRECTORY
from converter.api import convert
from documents.models import DocumentPage, DocumentVersion

from .settings import TESSERACT_PATH, TESSERACT_LANGUAGE, UNPAPER_PATH
from .exceptions import TesseractError, UnpaperError
from .parsers import parse_document_page
from .parsers.exceptions import ParserError, ParserUnknownFile
from .literals import (DEFAULT_OCR_FILE_FORMAT, UNPAPER_FILE_FORMAT,
    DEFAULT_OCR_FILE_EXTENSION)


def get_language_backend():
    """
    Return the OCR cleanup language backend using the selected tesseract
    language in the configuration settings
    """
    try:
        module = import_module(u'.'.join([u'ocr', u'lang', TESSERACT_LANGUAGE]))
    except ImportError:
        sys.stderr.write(u'\nWarning: No OCR app language backend for language: %s\n\n' % TESSERACT_LANGUAGE)
        return None
    return module

language_backend = get_language_backend()


def cleanup(filename):
    """
    Try to remove the given filename, ignoring non-existent files
    """
    try:
        os.remove(filename)
    except OSError:
        pass


def run_tesseract(input_filename, lang=None):
    """
    Execute the command line binary of tesseract
    """
    fd, filepath = tempfile.mkstemp()
    os.close(fd)
    ocr_output = os.extsep.join([filepath, u'txt'])
    command = [unicode(TESSERACT_PATH), unicode(input_filename), unicode(filepath)]

    if lang is not None:
        command.extend([u'-l', lang])

    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        error_text = proc.stderr.read()
        cleanup(filepath)
        cleanup(ocr_output)
        if lang:
            # If tesseract gives an error with a language parameter
            # re-run it with no parameter again
            return run_tesseract(input_filename, lang=None)
        else:
            raise TesseractError(error_text)

    fd = codecs.open(ocr_output, 'r', 'utf-8')
    text = fd.read().strip()
    fd.close()

    os.unlink(filepath)

    return text


def do_document_ocr(document_version_pk):
    """
    Try first to extract text from document pages using the registered
    parser, if the parser fails or if there is no parser registered for
    the document mimetype do a visual OCR by calling tesseract
    """
    document_version = DocumentVersion.objects.get(pk=document_version_pk)
    for document_page in document_version.pages.all():
        try:
            # Try to extract text by means of a parser
            parse_document_page(document_page)
        except (ParserError, ParserUnknownFile):
            # Fall back to doing visual OCR

            document_filepath = document_page.document.get_image_cache_name(page=document_page.page_number, version=document_page.document_version.pk)
            unpaper_output_filename = u'%s_unpaper_out_page_%s%s%s' % (document_page.document.uuid, document_page.page_number, os.extsep, UNPAPER_FILE_FORMAT)
            unpaper_output_filepath = os.path.join(TEMPORARY_DIRECTORY, unpaper_output_filename)

            unpaper_input = convert(document_filepath, file_format=UNPAPER_FILE_FORMAT)
            execute_unpaper(input_filepath=unpaper_input, output_filepath=unpaper_output_filepath)

            #from PIL import Image, ImageOps
            #im = Image.open(document_filepath)
            ##if im.mode=='RGBA':
            ##    im=im.convert('RGB')
            ##im = im.convert('L')
            #im = ImageOps.grayscale(im)
            #im.save(unpaper_output_filepath)

            # Convert to TIFF
            pre_ocr_filepath = convert(input_filepath=unpaper_output_filepath, file_format=DEFAULT_OCR_FILE_FORMAT)
            # Tesseract needs an explicit file extension
            pre_ocr_filepath_w_ext = os.extsep.join([pre_ocr_filepath, DEFAULT_OCR_FILE_EXTENSION])
            os.rename(pre_ocr_filepath, pre_ocr_filepath_w_ext)
            try:
                ocr_text = run_tesseract(pre_ocr_filepath_w_ext, TESSERACT_LANGUAGE)

                document_page.content = ocr_cleanup(ocr_text)
                document_page.page_label = _(u'Text from OCR')
                document_page.save()
            finally:
                cleanup(pre_ocr_filepath_w_ext)
                cleanup(unpaper_input)
                cleanup(document_filepath)
                cleanup(unpaper_output_filepath)


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
