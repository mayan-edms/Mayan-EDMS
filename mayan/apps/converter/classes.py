from __future__ import unicode_literals

import base64
import logging
import os

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from PIL import Image
import sh

from django.utils.translation import string_concat, ugettext_lazy as _

from common.settings import setting_temporary_directory
from common.utils import fs_cleanup, mkstemp
from mimetype.api import get_mimetype

from .exceptions import InvalidOfficeFormat, OfficeConversionError
from .literals import DEFAULT_PAGE_NUMBER, DEFAULT_FILE_FORMAT
from .settings import setting_libreoffice_path

CHUNK_SIZE = 1024
logger = logging.getLogger(__name__)

try:
    LIBREOFFICE = sh.Command(
        setting_libreoffice_path.value
    ).bake('--headless', '--convert-to', 'pdf')
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

        if not os.path.exists(setting_libreoffice_path.value):
            raise OfficeConversionError(
                _(
                    'LibreOffice not installed or not found at path: %s'
                ) % setting_libreoffice_path.value
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

        args = (input_filepath, '--outdir', setting_temporary_directory.value)

        kwargs = {'_env': {'HOME': setting_temporary_directory.value}}

        if libreoffice_filter:
            kwargs.update({'infilter': libreoffice_filter})

        try:
            LIBREOFFICE(*args, **kwargs)
        except sh.ErrorReturnCode as exception:
            raise OfficeConversionError(exception)
        finally:
            fs_cleanup(input_filepath)

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

    def get_page(self, output_format=DEFAULT_FILE_FORMAT, as_base64=False):
        if not self.image:
            self.seek(0)

        image_buffer = StringIO()

        new_mode = self.image.mode

        if output_format.upper() == 'JPEG':
            if self.image.mode == 'P':
                new_mode = 'RGB'
                if 'transparency' in self.image.info:
                    new_mode = 'RGBA'

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


class BaseTransformation(object):
    name = 'base_transformation'
    arguments = ()

    _registry = {}

    @staticmethod
    def encode_hash(decoded_value):
        return hex(abs(decoded_value))[2:]

    @staticmethod
    def decode_hash(encoded_value):
        return int(encoded_value, 16)

    @staticmethod
    def combine(transformations):
        result = None

        for index, transformation in enumerate(transformations):
            if not result:
                result = hash((BaseTransformation.decode_hash(transformation.cache_hash()), index))
            else:
                result ^= hash((BaseTransformation.decode_hash(transformation.cache_hash()), index))

        return BaseTransformation.encode_hash(result)

    @classmethod
    def register(cls, transformation):
        cls._registry[transformation.name] = transformation

    @classmethod
    def get_transformation_choices(cls):
        return [
            (name, klass.get_label()) for name, klass in cls._registry.items()
        ]

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def get_label(cls):
        return string_concat(cls.label, ': ', ', '.join(cls.arguments))

    def __init__(self, **kwargs):
        self.kwargs = {}
        for argument_name in self.arguments:
            setattr(self, argument_name, kwargs.get(argument_name))
            self.kwargs[argument_name] = kwargs.get(argument_name)

    def cache_hash(self):
        result = unicode.__hash__(self.name)
        for index, (key, value) in enumerate(self.kwargs.items()):
            result ^= hash((key, index)) ^ hash((value, index))

        return BaseTransformation.encode_hash(result)

    def execute_on(self, image):
        self.image = image
        self.aspect = 1.0 * image.size[0] / image.size[1]


class TransformationResize(BaseTransformation):
    name = 'resize'
    arguments = ('width', 'height')
    label = _('Resize')

    def execute_on(self, *args, **kwargs):
        super(TransformationResize, self).execute_on(*args, **kwargs)

        width = int(self.width)
        height = int(self.height or 1.0 * width / self.aspect)

        factor = 1
        while self.image.size[0] / factor > 2 * width and self.image.size[1] * 2 / factor > 2 * height:
            factor *= 2

        if factor > 1:
            self.image.thumbnail(
                (self.image.size[0] / factor, self.image.size[1] / factor),
                Image.NEAREST
            )

        # Resize the image with best quality algorithm ANTI-ALIAS
        self.image.thumbnail((width, height), Image.ANTIALIAS)

        return self.image


class TransformationRotate(BaseTransformation):
    name = 'rotate'
    arguments = ('degrees',)
    label = _('Rotate')

    def execute_on(self, *args, **kwargs):
        super(TransformationRotate, self).execute_on(*args, **kwargs)

        self.degrees %= 360

        if self.degrees == 0:
            return self.image

        return self.image.rotate(
            360 - self.degrees, resample=Image.BICUBIC, expand=True
        )


class TransformationZoom(BaseTransformation):
    name = 'zoom'
    arguments = ('percent',)
    label = _('Zoom')

    def execute_on(self, *args, **kwargs):
        super(TransformationZoom, self).execute_on(*args, **kwargs)

        if self.percent == 100:
            return self.image

        decimal_value = float(self.percent) / 100
        return self.image.resize(
            (
                int(self.image.size[0] * decimal_value),
                int(self.image.size[1] * decimal_value)
            ), Image.ANTIALIAS
        )


class TransformationCrop(BaseTransformation):
    name = 'crop'
    arguments = ('left', 'top', 'right', 'bottom',)
    label = _('Crop')

    def execute_on(self, *args, **kwargs):
        super(TransformationCrop, self).execute_on(*args, **kwargs)

        return self.image.crop(
            (self.left, self.top, self.right, self.bottom)
        )


BaseTransformation.register(TransformationResize)
BaseTransformation.register(TransformationRotate)
BaseTransformation.register(TransformationZoom)
BaseTransformation.register(TransformationCrop)
