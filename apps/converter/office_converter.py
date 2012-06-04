from __future__ import absolute_import

import os
import subprocess
import logging

from mimetype.api import get_mimetype
from common.conf.settings import TEMPORARY_DIRECTORY
from common.utils import id_generator

from .conf.settings import UNOCONV_PATH, UNOCONV_USE_PIPE, LIBREOFFICE_PATH
from .exceptions import (OfficeConversionError,
    OfficeBackendError, UnknownFileFormat)

CACHED_FILE_SUFFIX = u'_office_converter'

CONVERTER_OFFICE_FILE_MIMETYPES = [
    u'application/msword',
    u'application/mswrite',
    u'application/mspowerpoint',
    u'application/msexcel',
    u'application/vnd.ms-excel',
    u'application/vnd.ms-powerpoint',
    u'application/vnd.oasis.opendocument.presentation',
    u'application/vnd.oasis.opendocument.text',
    u'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    u'application/vnd.oasis.opendocument.spreadsheet',
    u'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    u'application/vnd.oasis.opendocument.graphics',
    u'application/vnd.ms-office',
    u'text/plain',
    u'text/rtf',
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
            self.output_filepath = os.path.join(TEMPORARY_DIRECTORY, u''.join([self.input_filepath, CACHED_FILE_SUFFIX]))
            self.exists = os.path.exists(self.output_filepath)
            if not self.exists:
                try:
                    self.backend.convert(self.input_filepath, self.output_filepath)
                    self.exists = True
                except OfficeBackendError, msg:
                    # convert exception so that at least the mime type icon is displayed
                    raise UnknownFileFormat(msg)

    def __unicode__(self):
        return getattr(self, 'output_filepath', None)

    def __str__(self):
        return str(self.__unicode__())


class OfficeConverterBackendUnoconv(object):
    def __init__(self):
        self.unoconv_path = UNOCONV_PATH if UNOCONV_PATH else u'/usr/bin/unoconv'
        if not os.path.exists(self.unoconv_path):
            raise OfficeBackendError('cannot find unoconv executable')

    def convert(self, input_filepath, output_filepath):
        """
        Executes the program unoconv using subprocess's Popen
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

        command = []
        command.append(self.unoconv_path)

        if UNOCONV_USE_PIPE:
            command.append(u'--pipe')
            command.append(u'mayan-%s' % id_generator())

        command.append(u'--format')
        command.append(u'pdf')
        command.append(u'--output')
        command.append(self.output_filepath)
        command.append(self.input_filepath)

        try:
            proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            return_code = proc.wait()
            logger.debug('return_code: %s' % return_code)

            readline = proc.stderr.readline()
            logger.debug('stderr: %s' % readline)
            if return_code != 0:
                raise OfficeBackendError(readline)
        except OSError, msg:
            raise OfficeBackendError(msg)
        except Exception, msg:
            logger.error('Unhandled exception', exc_info=msg)


class OfficeConverterBackendDirect(object):
    def __init__(self):
        self.libreoffice_path = LIBREOFFICE_PATH if LIBREOFFICE_PATH else u'/usr/bin/libreoffice'
        if not os.path.exists(self.libreoffice_path):
            raise OfficeBackendError('cannot find LibreOffice executable')
        logger.debug('self.libreoffice_path: %s' % self.libreoffice_path)

    def convert(self, input_filepath, output_filepath):
        """
        Executes libreoffice using subprocess's Popen
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

        command = []
        command.append(self.libreoffice_path)

        command.append(u'--headless')
        command.append(u'--convert-to')
        command.append(u'pdf')
        command.append(self.input_filepath)
        command.append(u'--outdir')
        command.append(TEMPORARY_DIRECTORY)

        logger.debug('command: %s' % command)

        try:
            os.environ['HOME'] = TEMPORARY_DIRECTORY
            proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            return_code = proc.wait()
            logger.debug('return_code: %s' % return_code)

            readline = proc.stderr.readline()
            logger.debug('stderr: %s' % readline)
            if return_code != 0:
                raise OfficeBackendError(readline)
            filename, extension = os.path.splitext(os.path.basename(self.input_filepath))
            logger.debug('filename: %s' % filename)
            logger.debug('extension: %s' % extension)

            converted_output = os.path.join(TEMPORARY_DIRECTORY, os.path.extsep.join([filename, 'pdf']))
            logger.debug('converted_output: %s' % converted_output)
         
            os.rename(converted_output, self.output_filepath)      
        except OSError, msg:
            raise OfficeBackendError(msg)
        except Exception, msg:
            logger.error('Unhandled exception', exc_info=msg)

