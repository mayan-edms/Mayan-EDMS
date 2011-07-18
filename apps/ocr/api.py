#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import codecs
import os
import subprocess
import tempfile
import sys

from django.utils.translation import ugettext as _
from django.utils.importlib import import_module

from converter.api import convert
from documents.models import DocumentPage

from ocr.conf.settings import TESSERACT_PATH
from ocr.conf.settings import TESSERACT_LANGUAGE
from ocr.exceptions import TesseractError
from ocr.conf.settings import UNPAPER_PATH
from ocr.parsers import parse_document_page
from ocr.parsers.exceptions import ParserError, ParserUnknownFile


def get_language_backend():
    """
    Return the OCR cleanup language backend using the selected tesseract
    language in the configuration settings
    """
    try:
        module = import_module(u'.'.join([u'ocr', u'lang', TESSERACT_LANGUAGE]))
    except ImportError:
        sys.stderr.write(u'\nError: No OCR app language backend for language: %s\n\n' % TESSERACT_LANGUAGE)
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


def run_tesseract(input_filename, output_filename_base, lang=None):
    """
    Execute the command line binary of tesseract
    """
    command = [unicode(TESSERACT_PATH), unicode(input_filename), unicode(output_filename_base)]
    if lang is not None:
        command += [u'-l', lang]

    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        error_text = proc.stderr.read()
        raise TesseractError(error_text)


def do_document_ocr(document):
    """
    first try to extract text from document pages using the registered
    parser if the parser fails or if there is no parser registered for
    the document mimetype do a visual OCR by calling tesseract
    """
    for document_page in document.documentpage_set.all():
        try:
            # Try to extract text by means of a parser
            parse_document_page(document_page)
        except (ParserError, ParserUnknownFile):
            # Fall back to doing visual OCR
            pass
            #desc, filepath = tempfile.mkstemp()
            #imagefile = None
            #source = u''
            #imagefile = convert_document_for_ocr(document, page=document_page.page_number)
            #run_tesseract(imagefile, filepath, TESSERACT_LANGUAGE)
            #ocr_output = os.extsep.join([filepath, u'txt'])
            #source = _(u'Text from OCR')
            #f = codecs.open(ocr_output, 'r', 'utf-8')
            #document_page.content = ocr_cleanup(f.read().strip())
            #document_page.page_label = source
            #document_page.save()
            #f.close()
            #cleanup(ocr_output)
        #finally:
        #    pass
            #os.close(desc)
            #cleanup(filepath)
            #if imagefile:
            #    cleanup(imagefile)


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
    command.append(input_filepath)
    command.append(output_filepath)
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        raise UnpaperError(proc.stderr.readline())

'''
def convert_document_for_ocr(document, page=DEFAULT_PAGE_NUMBER, file_format=DEFAULT_OCR_FILE_FORMAT):
    #Extract document file
    input_filepath = document_save_to_temp_dir(document, document.uuid)

    #Convert for OCR
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    transformation_output_file = u'%s_trans%s%s%s' % (temp_path, page, os.extsep, file_format)
    unpaper_input_file = u'%s_unpaper_in%s%spnm' % (temp_path, page, os.extsep)
    unpaper_output_file = u'%s_unpaper_out%s%spnm' % (temp_path, page, os.extsep)
    convert_output_file = u'%s_ocr%s%s%s' % (temp_path, page, os.extsep, file_format)

    try:
        document_page = document.documentpage_set.get(page_number=page)
        transformations, warnings = document_page.get_transformation_list()

        #Apply default transformations
        backend.convert_file(input_filepath=input_filepath, page=page, quality=QUALITY_HIGH, transformations=transformations, output_filepath=transformation_output_file)
        #Do OCR operations
        backend.convert_file(input_filepath=transformation_output_file, arguments=OCR_OPTIONS, output_filepath=unpaper_input_file)
        # Process by unpaper
        execute_unpaper(input_filepath=unpaper_input_file, output_filepath=unpaper_output_file)
        # Convert to tif
        backend.convert_file(input_filepath=unpaper_output_file, output_filepath=convert_output_file)
    finally:
        cleanup(transformation_output_file)
        cleanup(unpaper_input_file)
        cleanup(unpaper_output_file)

    return convert_output_file
'''


