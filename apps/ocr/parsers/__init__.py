import codecs
import os
import subprocess
import tempfile
import sys

import slate

from django.utils.translation import ugettext as _

from ocr.parsers.exceptions import ParserError, ParserUnknownFile

mimetype_registry = {}


def register_parser(mimetype, function):
    mimetype_registry[mimetype] = {'function': function}


def pdf_parser(document_page):
    fd = document_page.document.open()
    pdf_pages = slate.PDF(fd)
    fd.close()
    
    if pdf_pages[document_page.page_number - 1] == '\x0c':
        raise ParserError
    
    document_page.content = pdf_pages[document_page.page_number - 1]
    document_page.page_label = _(u'Text extracted from PDF')
    document_page.save()
       

def parse_document_page(document_page):
    try:
        mimetype_registry[document_page.document.file_mimetype]['function'](document_page)
    except KeyError:
        raise ParserUnknownFile

        
register_parser('application/pdf', pdf_parser)
