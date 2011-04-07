#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import codecs
import os
import subprocess
import tempfile
import sys

from django.utils.translation import ugettext as _
from django.utils.importlib import import_module

from common import TEMPORARY_DIRECTORY
from converter.api import convert_document_for_ocr
from documents.models import DocumentPage

from ocr.conf.settings import TESSERACT_PATH
from ocr.conf.settings import TESSERACT_LANGUAGE

    
def get_language_backend():
    try:
        module = import_module(u'.'.join([u'ocr',u'lang', TESSERACT_LANGUAGE]))
    except ImportError:
        sys.stderr.write('\nError: No OCR app language backend for language: %s\n\n' % TESSERACT_LANGUAGE)
        return None
    return module

backend = get_language_backend()


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
    
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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
            document_page = document.documentpage_set.get(page_number=page_index + 1)
            document_page.content = ocr_cleanup(f.read().strip())
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


def ocr_cleanup(text):
    output = []
    for line in text.splitlines():
        line = line.strip()
        for word in line.split():
            if backend:
                result = backend.check_word(word)
            else:
                result = word
            if result:
                output.append(result)
        output.append('\n')
            
    return u' '.join(output)

   
def clean_pages():
    for page in DocumentPage.objects.all():
        if page.content:
            page.content = ocr_cleanup(page.content)
            page.save()
