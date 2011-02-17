#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import os

import subprocess
import tempfile

from django.utils.translation import ugettext as _

from documents.models import DocumentPage
from common.conf.settings import TEMPORARY_DIRECTORY
from converter.api import convert_document_for_ocr

from ocr.conf.settings import TESSERACT_PATH


def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass

class TesseractError(Exception):
    pass
#    def __init__(self, status, message):
#        self.status = status
#        self.message = message

def get_errors(error_string):
    '''
    returns all lines in the error_string that start with the string "error"

    '''
    lines = error_string.splitlines()
    return lines[1]
    #error_lines = (line for line in lines if line.find('error') >= 0)
    #return '\n'.join(error_lines)

def run_tesseract(input_filename, output_filename_base, lang=None):
    command = [TESSERACT_PATH, input_filename, output_filename_base]
    if lang is not None:
        command += ['-l', lang]

    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())


def ocr_document(document):
    for page_index, document_page in enumerate(document.documentpage_set.all()):    
        imagefile = convert_document_for_ocr(document, page=page_index)
        desc, filepath = tempfile.mkstemp()
        try:
            status, error_string = run_tesseract(imagefile, filepath)
            if status:
                errors = get_errors(error_string)
                raise TesseractError(errors)
        finally:
            ocr_output = os.extsep.join([filepath, 'txt'])

        f = file(ocr_output)
        try:
            document_page, created = DocumentPage.objects.get_or_create(document=document,
                page_number=page_index+1)
            document_page.content = f.read().strip()
            document_page.page_label = _(u'Text from OCR')
            document_page.save()
        finally:
            f.close()
            cleanup(filepath)
            cleanup(ocr_output)
            cleanup(imagefile)
