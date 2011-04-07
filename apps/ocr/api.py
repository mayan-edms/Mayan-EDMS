# -*- coding: iso-8859-1 -*-
#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import codecs
import os
import subprocess
import re
import tempfile

from django.utils.translation import ugettext as _

from common import TEMPORARY_DIRECTORY
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


def ocr_cleanup(text):
    output = []
    for line in text.splitlines():
        line = line.strip()
        for word in line.split():
            result = check_word(word)
            if result:
                output.append(result)
        output.append('\n')
            
    return u' '.join(output)


def check_word(word):
    ALL_ALPHANUM = re.compile('([0-9a-záéíóúüñ])', re.I)
    NON_ALPHANUM = re.compile('([^0-9a-záéíóúüñ])', re.I)

    TOO_MANY_VOWELS = re.compile('[aáeéiíoóuúü]{3}', re.I)
    TOO_MANY_CONSONANTS = re.compile('[bcdfghjklmnñpqrstvwxyz]{5}', re.I)
    ALL_ALPHA = re.compile('^[a-z]+$', re.I)
    SINGLE_LETTER_WORDS = re.compile('^[aeoóuy]$', re.I)

    #(L) If a string is longer than 20 characters, it is
    #garbage:
    if len(word) > 20:
        return None

    #(A) If a string’s ratio of alphanumeric characters to total 
    #characters. is less than 50%, the string is garbage:
    if len(ALL_ALPHANUM.findall(word)) < len(word) / 2:
        return None

    #Remove word if all the letters in the word are non alphanumeric
    if len(NON_ALPHANUM.findall(word)) == len(word):
        return None
    
    #Removed words with too many consecutie vowels
    if TOO_MANY_VOWELS.findall(word):
        return None 

    #Removed words with too many consecutie consonants
    if TOO_MANY_CONSONANTS.findall(word):
        return None 

    #Only allow specific single letter words
    if len(word) == 1 and not SINGLE_LETTER_WORDS.findall(word):
        return None
        
    return word
    
    

from ocr.api import ocr_cleanup
from documents.models import DocumentPage
def clean_pages():
    for page in DocumentPage.objects.all():
        if page.content:
            page.content = ocr_cleanup(page.content)
            #print page.content
            print page.pk
            page.save()
