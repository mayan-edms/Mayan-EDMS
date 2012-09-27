import os
import slate
import logging
import tempfile
import subprocess

from django.utils.translation import ugettext as _

from converter import office_converter
from converter.office_converter import OfficeConverter
from converter.exceptions import OfficeConversionError
from documents.utils import document_save_to_temp_dir
from common.utils import copyfile
from common.textparser import TextParser as OriginalTextParser, TEXT_PARSER_MIMETYPES

from ocr.parsers.exceptions import ParserError, ParserUnknownFile
from ocr.settings import PDFTOTEXT_PATH


mimetype_registry = {}
logger = logging.getLogger(__name__)


def register_parser(mimetypes, parsers):
    for mimetype in mimetypes:
        for parser in parsers:
            try:
                parser_instance = parser()
            except ParserError:
                # If parser fails initialization is not added to the list for this mimetype
                pass
            else:
                mimetype_registry.setdefault(mimetype, []).append(parser_instance)


def parse_document_page(document_page, descriptor=None, mimetype=None):
    logger.debug('executing')
    logger.debug('document_page: %s' % document_page)
    logger.debug('mimetype: %s' % document_page.document.file_mimetype)

    if not mimetype:
        mimetype = document_page.document.file_mimetype

    try:
        for parser in mimetype_registry[mimetype]:
            try:
                parser.parse(document_page, descriptor)
            except ParserError:
                # If parser raises error, try next parser in the list
                pass
            else:
                # If parser was successfull there is no need to try
                # others in the list for this mimetype
                return

        raise ParserError('Parser list exhausted')
    except KeyError:
        raise ParserUnknownFile


class Parser(object):
    """
    Parser base class
    """

    def parse(self, document_page, descriptor=None):
        raise NotImplementedError("Your %s class has not defined a parse() method, which is required." % self.__class__.__name__)


class SlateParser(Parser):
    """
    Parser for PDF files using the slate library for Python
    """
    def parse(self, document_page, descriptor=None):
        logger.debug('Starting SlateParser')

        if not descriptor:
            descriptor = document_page.document_version.open()

        pdf_pages = slate.PDF(descriptor)
        descriptor.close()

        if pdf_pages[document_page.page_number - 1] == '\x0c':
            raise ParserError

        document_page.content = pdf_pages[document_page.page_number - 1]
        document_page.page_label = _(u'Text extracted from PDF')
        document_page.save()


class OfficeParser(Parser):
    """
    Parser for office document formats
    """
    def parse(self, document_page, descriptor=None):
        logger.debug('executing')
        try:
            office_converter = OfficeConverter()
            document_file = document_save_to_temp_dir(document_page.document, document_page.document.checksum)
            logger.debug('document_file: %s', document_file)

            office_converter.convert(document_file, mimetype=document_page.document.file_mimetype)
            if office_converter.exists:
                input_filepath = office_converter.output_filepath
                logger.debug('office_converter.output_filepath: %s', input_filepath)

                # Now that the office document has been converted to PDF
                # call the coresponding PDF parser in this new file
                parse_document_page(document_page, descriptor=open(input_filepath), mimetype=u'application/pdf')
            else:
                raise ParserError

        except OfficeConversionError, msg:
            logger.error(msg)
            raise ParserError


class PopplerParser(Parser):
    """
    PDF parser using the pdftotext execute from the poppler package
    """
    def __init__(self):
        self.pdftotext_path = PDFTOTEXT_PATH if PDFTOTEXT_PATH else u'/usr/bin/pdftotext'
        if not os.path.exists(self.pdftotext_path):
            raise ParserError('cannot find pdftotext executable')
        logger.debug('self.pdftotext_path: %s' % self.pdftotext_path)

    def parse(self, document_page, descriptor=None):
        from common.settings import TEMPORARY_DIRECTORY

        logger.debug('parsing PDF with PopplerParser')
        pagenum = str(document_page.page_number)

        if descriptor:
            destination_descriptor, temp_filepath = tempfile.mkstemp(dir=TEMPORARY_DIRECTORY)
            copyfile(descriptor, temp_filepath)
            document_file = temp_filepath
        else:
            document_file = document_save_to_temp_dir(document_page.document, document_page.document.checksum)

        logger.debug('document_file: %s', document_file)

        logger.debug('parsing PDF page %s' % pagenum)

        command = []
        command.append(self.pdftotext_path)
        command.append('-f')
        command.append(pagenum)
        command.append('-l')
        command.append(pagenum)
        command.append(document_file)
        command.append('-')

        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        if return_code != 0:
            logger.error(proc.stderr.readline())
            raise ParserError

        output = proc.stdout.read()
        if output == '\x0c':
            logger.debug('Parser didn\'t any output')
            raise ParserError('No output')

        document_page.content = output
        document_page.page_label = _(u'Text extracted from PDF')
        document_page.save()


class TextParser(Parser):
    def parse(self, document_page, descriptor=None):
        from common.settings import TEMPORARY_DIRECTORY

        logger.debug('parsing with TextParser')
        pagenum = str(document_page.page_number)

        if descriptor:
            destination_descriptor, temp_filepath = tempfile.mkstemp(dir=TEMPORARY_DIRECTORY)
            copyfile(descriptor, temp_filepath)
            document_file = temp_filepath
        else:
            document_file = document_save_to_temp_dir(document_page.document, document_page.document.checksum)

        logger.debug('document_file: %s', document_file)

        logger.debug('parsing text page %s' % pagenum)

        parser = OriginalTextParser()

        document_page.content = u'\n'.join(parser.render_to_viewport(filename=document_file)[int(pagenum) - 1])
        document_page.page_label = _(u'Text extracted from file')
        document_page.save()
        

register_parser(mimetypes=[u'application/pdf'], parsers=[PopplerParser, SlateParser])
register_parser(mimetypes=TEXT_PARSER_MIMETYPES, parsers=[TextParser])
register_parser(mimetypes=office_converter.CONVERTER_OFFICE_FILE_MIMETYPES, parsers=[OfficeParser])
