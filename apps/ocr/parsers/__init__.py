import slate
import logging

from django.utils.translation import ugettext as _

from converter import office_converter
from converter import office_converter
from converter.office_converter import OfficeConverter
from converter.exceptions import OfficeBackendError, OfficeConversionError
from documents.utils import document_save_to_temp_dir

from ocr.parsers.exceptions import ParserError, ParserUnknownFile


mimetype_registry = {}
logger = logging.getLogger(__name__)


def register_parser(function, mimetype=None, mimetypes=None):
    if mimetypes:
        for mimetype in mimetypes:
            mimetype_registry[mimetype] = {'function': function}
    else:
        mimetype_registry[mimetype] = {'function': function}


def pdf_parser(document_page, descriptor=None):
    if not descriptor:
        descriptor = document_page.document_version.open()
    
    pdf_pages = slate.PDF(descriptor)
    descriptor.close()

    if pdf_pages[document_page.page_number - 1] == '\x0c':
        raise ParserError

    document_page.content = pdf_pages[document_page.page_number - 1]
    document_page.page_label = _(u'Text extracted from PDF')
    document_page.save()


def office_parser(document_page):
    logger.debug('executing')
    try:
        office_converter = OfficeConverter()
        document_file = document_save_to_temp_dir(document_page.document, document_page.document.checksum)
        logger.debug('document_file: %s', document_file)
        
        office_converter.convert(document_file, mimetype=document_page.document.file_mimetype)
        if office_converter.exists:
            input_filepath = office_converter.output_filepath
            logger.debug('office_converter.output_filepath: %s', input_filepath)

            pdf_parser(document_page, descriptor=open(input_filepath))
        else:
            raise ParserError

    except OfficeConversionError, msg:
        print msg
        raise ParserError
    

def parse_document_page(document_page):
    logger.debug('executing')
    logger.debug('document_page: %s' % document_page)
    logger.debug('mimetype: %s' % document_page.document.file_mimetype)

    try:
        mimetype_registry[document_page.document.file_mimetype]['function'](document_page)
    except KeyError:
        raise ParserUnknownFile


register_parser(mimetype=u'application/pdf', function=pdf_parser)
register_parser(mimetypes=office_converter.CONVERTER_OFFICE_FILE_MIMETYPES, function=office_parser)
