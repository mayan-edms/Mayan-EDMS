from __future__ import unicode_literals

import base64
from io import BytesIO
import logging
import os

from PIL import Image
import sh
import yaml

from django.utils.translation import ugettext_lazy as _

from common.settings import setting_temporary_directory
from common.utils import fs_cleanup, mkdtemp, mkstemp
from mimetype.api import get_mimetype

from .exceptions import InvalidOfficeFormat, OfficeConversionError
from .literals import (
    DEFAULT_LIBREOFFICE_PATH, DEFAULT_PAGE_NUMBER, DEFAULT_PILLOW_FORMAT
)
from .settings import setting_graphics_backend_config

CHUNK_SIZE = 1024
logger = logging.getLogger(__name__)

try:
    LIBREOFFICE = sh.Command(
        yaml.load(setting_graphics_backend_config.value).get(
            'libreoffice_path', DEFAULT_LIBREOFFICE_PATH
        )
    ).bake('--headless', '--convert-to', 'pdf:writer_pdf_Export')
except sh.CommandNotFound:
    LIBREOFFICE = None


CONVERTER_OFFICE_FILE_MIMETYPES = (
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
)


class ConverterBase(object):
    def __init__(self, file_object, mime_type=None):
        self.file_object = file_object
        self.image = None
        self.mime_type = mime_type or get_mimetype(
            file_object=file_object, mimetype_only=False
        )[0]
        self.soffice_file = None

    def to_pdf(self):
        if self.mime_type in CONVERTER_OFFICE_FILE_MIMETYPES:
            return self.soffice()
        else:
            raise InvalidOfficeFormat(_('Not an office file format.'))

    def seek(self, page_number):
        # Starting with #0
        self.file_object.seek(0)

        try:
            self.image = Image.open(self.file_object)
        except IOError:
            # Cannot identify image file
            self.image = self.convert(page_number=page_number)
        else:
            self.image.seek(page_number)
            self.image.load()

    def soffice(self):
        """
        Executes LibreOffice as a subprocess
        """
        if not LIBREOFFICE:
            raise OfficeConversionError(
                _('LibreOffice not installed or not found.')
            )

        new_file_object, input_filepath = mkstemp()
        self.file_object.seek(0)
        os.write(new_file_object, self.file_object.read())
        self.file_object.seek(0)
        os.lseek(new_file_object, 0, os.SEEK_SET)
        os.close(new_file_object)

        libreoffice_filter = None
        if self.mime_type == 'text/plain':
            libreoffice_filter = 'Text (encoded):UTF8,LF,,,'

        libreoffice_home_directory = mkdtemp()
        args = (
            input_filepath, '--outdir', setting_temporary_directory.value,
            '-env:UserInstallation=file://{}'.format(
                os.path.join(
                    libreoffice_home_directory, 'LibreOffice_Conversion'
                )
            ),
        )

        kwargs = {'_env': {'HOME': libreoffice_home_directory}}

        if libreoffice_filter:
            kwargs.update({'infilter': libreoffice_filter})

        try:
            LIBREOFFICE(*args, **kwargs)
        except sh.ErrorReturnCode as exception:
            raise OfficeConversionError(exception)
        except Exception as exception:
            logger.error('Exception launching Libre Office; %s', exception)
            raise
        finally:
            fs_cleanup(input_filepath)
            fs_cleanup(libreoffice_home_directory)

        filename, extension = os.path.splitext(
            os.path.basename(input_filepath)
        )
        logger.debug('filename: %s', filename)
        logger.debug('extension: %s', extension)

        converted_output = os.path.join(
            setting_temporary_directory.value, os.path.extsep.join(
                (filename, 'pdf')
            )
        )
        logger.debug('converted_output: %s', converted_output)

        with open(converted_output) as converted_file_object:
            while True:
                data = converted_file_object.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

        fs_cleanup(input_filepath)
        fs_cleanup(converted_output)

    def get_page(self, output_format=None, as_base64=False):
        output_format = output_format or yaml.load(
            setting_graphics_backend_config.value
        ).get(
            'pillow_format', DEFAULT_PILLOW_FORMAT
        )

        if not self.image:
            self.seek(0)

        image_buffer = BytesIO()
        new_mode = self.image.mode

        if output_format.upper() == 'JPEG':
            # JPEG doesn't support transparency channel, convert the image to
            # RGB. Removes modes: P and RGBA
            new_mode = 'RGB'

        self.image.convert(new_mode).save(image_buffer, format=output_format)

        if as_base64:
            return 'data:{};base64,{}'.format(Image.MIME[output_format], base64.b64encode(image_buffer.getvalue()))
        else:
            image_buffer.seek(0)

        return image_buffer

    def convert(self, page_number=DEFAULT_PAGE_NUMBER):
        self.page_number = page_number

    def transform(self, transformation):
        if not self.image:
            self.seek(0)

        self.image = transformation.execute_on(self.image)

    def transform_many(self, transformations):
        if not self.image:
            self.seek(0)

        for transformation in transformations:
            self.image = transformation.execute_on(self.image)

    def get_page_count(self):
        try:
            self.soffice_file = self.to_pdf()
        except InvalidOfficeFormat as exception:
            logger.debug('Is not an office format document; %s', exception)

    def detect_orientation(self, page_number):
        # Must be overrided by subclass
        pass
