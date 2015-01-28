from __future__ import unicode_literals

import logging
import os
import subprocess

from common.settings import TEMPORARY_DIRECTORY
from mimetype.api import get_mimetype

from .exceptions import OfficeBackendError, UnknownFileFormat
from .settings import LIBREOFFICE_PATH

CACHED_FILE_SUFFIX = '_office_converter'

CONVERTER_OFFICE_FILE_MIMETYPES = [
    'application/msword',
    'application/mswrite',
    'application/mspowerpoint',
    'application/msexcel',
    'application/pgp-keys',
    'application/vnd.ms-excel',
    'application/vnd.ms-excel.addin.macroEnabled.12',
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
    'application/vnd.ms-powerpoint',
    'application/vnd.oasis.opendocument.chart',
    'application/vnd.oasis.opendocument.chart-template',
    'application/vnd.oasis.opendocument.formula',
    'application/vnd.oasis.opendocument.formula-template',
    'application/vnd.oasis.opendocument.graphics',
    'application/vnd.oasis.opendocument.graphics-template',
    'application/vnd.oasis.opendocument.image',
    'application/vnd.oasis.opendocument.image-template',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.oasis.opendocument.presentation-template',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.presentationml.slide',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.oasis.opendocument.spreadsheet-template',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.text-master',
    'application/vnd.oasis.opendocument.text-template',
    'application/vnd.oasis.opendocument.text-web',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-office',
    'application/xml',
    'text/x-c',
    'text/x-c++',
    'text/x-pascal',
    'text/x-msdos-batch',
    'text/x-python',
    'text/x-shellscript',
    'text/plain',
    'text/rtf',
]

logger = logging.getLogger(__name__)


class OfficeConverter(object):
    def __init__(self):
        self.backend_class = OfficeConverterBackendDirect
        self.backend = self.backend_class()
        self.exists = False
        self.mimetype = None
        self.encoding = None

    def mimetypes(self):
        return CONVERTER_OFFICE_FILE_MIMETYPES

    def convert(self, input_filepath, mimetype=None):
        self.exists = False
        self.mimetype = None
        self.encoding = None

        self.input_filepath = input_filepath

        # Make sure file is of a known office format
        if mimetype:
            self.mimetype = mimetype
        else:
            self.mimetype, self.encoding = get_mimetype(open(self.input_filepath), self.input_filepath, mimetype_only=True)

        if self.mimetype in CONVERTER_OFFICE_FILE_MIMETYPES:
            # Cache results of conversion
            self.output_filepath = os.path.join(TEMPORARY_DIRECTORY, ''.join([self.input_filepath, CACHED_FILE_SUFFIX]))
            self.exists = os.path.exists(self.output_filepath)
            if not self.exists:
                try:
                    self.backend.convert(self.input_filepath, self.output_filepath)
                    self.exists = True
                except OfficeBackendError as exception:
                    # convert exception so that at least the mime type icon is displayed
                    raise UnknownFileFormat(exception)


class OfficeConverterBackendDirect(object):
    def __init__(self):
        self.libreoffice_path = LIBREOFFICE_PATH
        if not os.path.exists(self.libreoffice_path):
            raise OfficeBackendError('cannot find LibreOffice executable')
        logger.debug('self.libreoffice_path: %s', self.libreoffice_path)

    def convert(self, input_filepath, output_filepath):
        """
        Executes libreoffice using subprocess's Popen
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

        command = []
        command.append(self.libreoffice_path)

        command.append('--headless')
        command.append('--convert-to')
        command.append('pdf')
        command.append(self.input_filepath)
        command.append('--outdir')
        command.append(TEMPORARY_DIRECTORY)

        logger.debug('command: %s', command)

        try:
            os.environ['HOME'] = TEMPORARY_DIRECTORY
            proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            return_code = proc.wait()
            logger.debug('return_code: %s', return_code)

            readline = proc.stderr.readline()
            logger.debug('stderr: %s', readline)
            if return_code != 0:
                raise OfficeBackendError(readline)
            filename, extension = os.path.splitext(os.path.basename(self.input_filepath))
            logger.debug('filename: %s', filename)
            logger.debug('extension: %s', extension)

            converted_output = os.path.join(TEMPORARY_DIRECTORY, os.path.extsep.join([filename, 'pdf']))
            logger.debug('converted_output: %s', converted_output)

            os.rename(converted_output, self.output_filepath)
        except OSError as exception:
            raise OfficeBackendError(exception)
        except Exception as exception:
            logger.error('Unhandled exception', exc_info=exception)
