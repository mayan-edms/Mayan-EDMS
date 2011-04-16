#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import codecs
import os
import subprocess
import tempfile
import sys

from django.utils.translation import ugettext as _
from django.utils.importlib import import_module

from converter.api import convert_document_for_ocr
from documents.models import DocumentPage

from ocr.conf.settings import TESSERACT_PATH
from ocr.conf.settings import TESSERACT_LANGUAGE
from ocr.conf.settings import PDFTOTEXT_PATH
from exceptions import TesseractError, PdftotextError


def get_language_backend():
    try:
        module = import_module(u'.'.join([u'ocr', u'lang', TESSERACT_LANGUAGE]))
    except ImportError:
        sys.stderr.write(u'\nError: No OCR app language backend for language: %s\n\n' % TESSERACT_LANGUAGE)
        return None
    return module

backend = get_language_backend()


def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass


def run_tesseract(input_filename, output_filename_base, lang=None):
    command = [unicode(TESSERACT_PATH), unicode(input_filename), unicode(output_filename_base)]
    if lang is not None:
        command += [u'-l', lang]

    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        error_text = proc.stderr.read()
        raise TesseractError(error_text)


def run_pdftotext(input_filename, output_filename, page_number=None):
    command = [unicode(PDFTOTEXT_PATH)]
    if page_number:
        command.extend(['-nopgbrk', '-f', unicode(page_number), '-l', unicode(page_number)])
    command.extend([unicode(input_filename), unicode(output_filename)])
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        error_text = proc.stderr.read()
        raise PdftotextError(error_text)
  

def do_document_ocr(document):
    for page_index, document_page in enumerate(document.documentpage_set.all()):
        desc, filepath = tempfile.mkstemp()
        imagefile = None
        source = u''
        try:
            if document.file_mimetype == u'application/pdf':
                pdf_filename = os.extsep.join([filepath, u'pdf'])
                document.save_to_file(pdf_filename)
                run_pdftotext(pdf_filename, filepath, document_page.page_number)
                cleanup(pdf_filename)
                if os.stat(filepath).st_size == 0:
                    #PDF page had no text, run tesseract on the page
                    imagefile = convert_document_for_ocr(document, page=page_index)
                    run_tesseract(imagefile, filepath, TESSERACT_LANGUAGE)
                    ocr_output = os.extsep.join([filepath, 'txt'])
                    source = _(u'Text from OCR')
                else:
                    ocr_output = filepath
                    source = _(u'Text extracted from PDF')
            else:
                imagefile = convert_document_for_ocr(document, page=page_index)
                run_tesseract(imagefile, filepath, TESSERACT_LANGUAGE)
                ocr_output = os.extsep.join([filepath, 'txt'])
                source = _(u'Text from OCR')
            f = codecs.open(ocr_output, 'r', 'utf-8')
            document_page = document.documentpage_set.get(page_number=page_index + 1)
            document_page.content = ocr_cleanup(f.read().strip())
            document_page.page_label = source
            document_page.save()
            f.close()
            cleanup(ocr_output)
        finally:
            cleanup(filepath)
            if imagefile:
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
        output.append(u'\n')

    return u' '.join(output)


def clean_pages():
    for page in DocumentPage.objects.all():
        if page.content:
            page.content = ocr_cleanup(page.content)
            page.save()
