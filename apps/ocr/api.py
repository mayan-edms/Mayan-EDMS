#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import codecs
import os
import subprocess
import tempfile

from django.utils.translation import ugettext as _
from django.contrib import messages

from common.conf.settings import TEMPORARY_DIRECTORY

from documents.models import Document

from converter.api import convert_document_for_ocr

from ocr.conf.settings import TESSERACT_PATH
from ocr.conf.settings import TESSERACT_LANGUAGE


class TesseractError(Exception):
    pass


def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass


def run_tesseract(input_filename, output_filename_base, lang=None):
    command = [TESSERACT_PATH, input_filename, output_filename_base]
    if lang is not None:
        command += ['-l', lang]
    
    proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        error_text = proc.stderr.read()
        raise TesseractError(error_text)


def do_document_ocr(document):
    for page_index, document_page in enumerate(document.documentpage_set.all()):
        imagefile = convert_document_for_ocr(document, page=page_index)
        desc, filepath = tempfile.mkstemp()
        try:
            run_tesseract(imagefile, filepath, TESSERACT_LANGUAGE)
            ocr_output = os.extsep.join([filepath, 'txt'])
            f = codecs.open(ocr_output, 'r', 'utf-8')
            document_page = document.documentpage_set.get(page_number=page_index+1)
            document_page.content = f.read().strip()
            document_page.page_label = _(u'Text from OCR')
            document_page.save()
            f.close()
            cleanup(ocr_output)
        except TesseractError, e:
            cleanup(filepath)
            cleanup(imagefile)
            raise TesseractError(e)
        finally:
            cleanup(filepath)
            cleanup(imagefile)
