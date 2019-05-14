from __future__ import unicode_literals

from io import BytesIO
import logging
import os
import shutil

from PIL import Image
import sh
import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django.utils.translation import ugettext_lazy as _

from mayan.apps.mimetype.api import get_mimetype
from mayan.apps.storage.settings import setting_temporary_directory
from mayan.apps.storage.utils import (
    NamedTemporaryFile, fs_cleanup, mkdtemp
)

from .exceptions import InvalidOfficeFormat, OfficeConversionError
from .literals import (
    DEFAULT_LIBREOFFICE_PATH, DEFAULT_PAGE_NUMBER, DEFAULT_PILLOW_FORMAT
)
from .settings import setting_graphics_backend_config

CHUNK_SIZE = 1024
logger = logging.getLogger(__name__)


libreoffice_path = yaml.load(
    stream=setting_graphics_backend_config.value, Loader=SafeLoader
).get(
    'libreoffice_path', DEFAULT_LIBREOFFICE_PATH
)

try:
    LIBREOFFICE = sh.Command(libreoffice_path).bake(
        '--headless', '--convert-to', 'pdf:writer_pdf_Export'
    )
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
        Image.init()

    def convert(self, page_number=DEFAULT_PAGE_NUMBER):
        self.page_number = page_number

    def detect_orientation(self, page_number):
        # Must be overrided by subclass
        pass

    def get_page(self, output_format=None):
        output_format = output_format or yaml.load(
            stream=setting_graphics_backend_config.value, Loader=SafeLoader
        ).get(
            'pillow_format', DEFAULT_PILLOW_FORMAT
        )

        if not self.image:
            self.seek_page(page_number=0)

        image_buffer = BytesIO()
        new_mode = self.image.mode

        if output_format.upper() == 'JPEG':
            # JPEG doesn't support transparency channel, convert the image to
            # RGB. Removes modes: P and RGBA
            new_mode = 'RGB'

        self.image.convert(new_mode).save(image_buffer, format=output_format)

        image_buffer.seek(0)

        return image_buffer

    def get_page_count(self):
        try:
            self.soffice_file = self.to_pdf()
        except InvalidOfficeFormat as exception:
            logger.debug('Is not an office format document; %s', exception)

    def seek_page(self, page_number):
        """
        Seek the specified page number from the source file object.
        If the file is a paged image get the page if not convert it to a
        paged image format and return the specified page as an image.
        """
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

        with NamedTemporaryFile() as temporary_file_object:
            # Copy the source file object of the converter instance to a
            # named temporary file to be able to pass it to the LibreOffice
            # execution.
            self.file_object.seek(0)
            shutil.copyfileobj(
                fsrc=self.file_object, fdst=temporary_file_object
            )
            self.file_object.seek(0)
            temporary_file_object.seek(0)

            libreoffice_home_directory = mkdtemp()
            args = (
                temporary_file_object.name, '--outdir', setting_temporary_directory.value,
                '-env:UserInstallation=file://{}'.format(
                    os.path.join(
                        libreoffice_home_directory, 'LibreOffice_Conversion'
                    )
                ),
            )

            kwargs = {'_env': {'HOME': libreoffice_home_directory}}

            if self.mime_type == 'text/plain':
                kwargs.update(
                    {'infilter': 'Text (encoded):UTF8,LF,,,'}
                )

            try:
                LIBREOFFICE(*args, **kwargs)
            except sh.ErrorReturnCode as exception:
                temporary_file_object.close()
                raise OfficeConversionError(exception)
            except Exception as exception:
                temporary_file_object.close()
                logger.error('Exception launching Libre Office; %s', exception)
                raise
            finally:
                fs_cleanup(libreoffice_home_directory)

            # LibreOffice return a PDF file with the same name as the input
            # provided but with the .pdf extension.

            # Get the converted output file path out of the temporary file
            # name plus the temporary directory

            filename, extension = os.path.splitext(
                os.path.basename(temporary_file_object.name)
            )

            logger.debug('filename: %s', filename)
            logger.debug('extension: %s', extension)

            converted_file_path = os.path.join(
                setting_temporary_directory.value, os.path.extsep.join(
                    (filename, 'pdf')
                )
            )
            logger.debug('converted_file_path: %s', converted_file_path)

        # Don't use context manager with the NamedTemporaryFile on purpose
        # so that it is deleted when the caller closes the file and not
        # before.

        temporary_converted_file_object = NamedTemporaryFile()

        # Copy the LibreOffice output file to a new named temporary file
        # and delete the converted file
        with open(converted_file_path, mode='rb') as converted_file_object:
            shutil.copyfileobj(
                fsrc=converted_file_object, fdst=temporary_converted_file_object
            )
        fs_cleanup(converted_file_path)
        temporary_converted_file_object.seek(0)
        return temporary_converted_file_object

    def to_pdf(self):
        if self.mime_type in CONVERTER_OFFICE_FILE_MIMETYPES:
            return self.soffice()
        else:
            raise InvalidOfficeFormat(_('Not an office file format.'))

    def transform(self, transformation):
        if not self.image:
            self.seek_page(page_number=0)

        self.image = transformation.execute_on(image=self.image)

    def transform_many(self, transformations):
        if not self.image:
            self.seek_page(page_number=0)

        for transformation in transformations:
            self.image = transformation.execute_on(image=self.image)
