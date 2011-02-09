#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import os

import subprocess
import tempfile

from django.utils.translation import ugettext as _

from documents.models import DocumentPage
from documents.conf.settings import TEMPORARY_DIRECTORY
from converter.api import convert_document_for_ocr

from ocr.conf.settings import TESSERACT_PATH


def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass

class TesseractError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message


def run_tesseract(input_filename, output_filename_base, lang=None):
    command = [TESSERACT_PATH, input_filename, output_filename_base]
    if lang is not None:
        command += ['-l', lang]

    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())


def ocr_document(document):
    total_pages = 1
    page = 0
    while page < total_pages:
        imagefile = convert_document_for_ocr(document, page=page)
        desc, filepath = tempfile.mkstemp()
        try:
            status, error_string = run_tesseract(imagefile, filepath)
            if status:
                errors = get_errors(error_string)
                raise TesseractError(status, errors)
        finally:
            ocr_output = os.extsep.join([filepath, 'txt'])
            f = file(ocr_output)
            try:
                document_page, created = DocumentPage.objects.get_or_create(document=document,
                    page_number=page)
                document_page.content = f.read().strip()
                document_page.page_label = _(u'Text from OCR')
                document_page.save()
            finally:
                f.close()
                cleanup(filepath)
                cleanup(ocr_output)
                cleanup(imagefile)
            
        page += 1
        
