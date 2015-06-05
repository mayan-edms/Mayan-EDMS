from __future__ import unicode_literals

import logging
import os
import subprocess
from tempfile import mkstemp

from django.utils.encoding import smart_str
from django.utils.module_loading import import_string

from common.settings import TEMPORARY_DIRECTORY
from common.utils import fs_cleanup
from mimetype.api import get_mimetype

from .exceptions import OfficeConversionError, UnknownFileFormat
from .literals import (
    DEFAULT_PAGE_NUMBER, DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION,
    DEFAULT_FILE_FORMAT, TRANSFORMATION_CHOICES, TRANSFORMATION_RESIZE,
    TRANSFORMATION_ROTATE, TRANSFORMATION_ZOOM, DIMENSION_SEPARATOR
)
from .office_converter import OfficeConverter
from .runtime import backend, office_converter
from .settings import GRAPHICS_BACKEND, LIBREOFFICE_PATH

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


logger.debug('initializing office backend')
try:
    office_converter = OfficeConverter()
except OfficeBackendError as exception:
    logger.error('error initializing office backend; %s', exception)
    office_converter = None
else:
    logger.debug('office_backend initialized')

backend = import_string(GRAPHICS_BACKEND)()


class BaseTransformation(object):
    name = 'base_transformation'
    arguments = ()

    def __init__(self, **kwargs):
        for argument_name in self.arguments:
            setattr(self, argument_name, kwargs.get(argument_name))


class TransformationResize(BaseTransformation):
    name = 'resize'
    arguments = ('width', 'height')


class TransformationRotate(BaseTransformation):
    name = 'rotate'
    arguments = ('degrees',)


class TransformationScale(BaseTransformation):
    name = 'scale'
    arguments = ('percent',)


class Converter(object):
    """
    def cache_cleanup(input_filepath, *args, **kwargs):
        try:
            os.remove(create_image_cache_filename(input_filepath, *args, **kwargs))
        except OSError:
            pass
    """

    """
    def create_image_cache_filename(input_filepath, *args, **kwargs):
        if input_filepath:
            hash_value = HASH_FUNCTION(''.join([HASH_FUNCTION(smart_str(input_filepath)), unicode(args), unicode(kwargs)]))
            return os.path.join(TEMPORARY_DIRECTORY, hash_value)
        else:
            return None
    """


    @staticmethod
    def soffice(file_object):
        """
        Executes libreoffice using subprocess's Popen
        """

        new_file_object, input_filepath = tempfile.mkstemp()
        new_file_object.write(file_object.read())
        file_object.seek(0)
        new_file_object.seek(0)
        new_file_object.close()

        command = []
        command.append(LIBREOFFICE_PATH)

        command.append('--headless')
        command.append('--convert-to')
        command.append('pdf')
        command.append(input_filepath)
        command.append('--outdir')
        command.append(TEMPORARY_DIRECTORY)

        logger.debug('command: %s', command)

        os.environ['HOME'] = TEMPORARY_DIRECTORY
        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        logger.debug('return_code: %s', return_code)

        readline = proc.stderr.readline()
        logger.debug('stderr: %s', readline)
        if return_code != 0:
            #raise OfficeBackendError(readline)
            raise Exception(readline)

        filename, extension = os.path.splitext(os.path.basename(input_filepath))
        logger.debug('filename: %s', filename)
        logger.debug('extension: %s', extension)

        converted_output = os.path.join(TEMPORARY_DIRECTORY, os.path.extsep.join([filename, 'pdf']))
        logger.debug('converted_output: %s', converted_output)

        return open(converted_output)
        #os.rename(converted_output, output_filepath)
        # TODO: remove temp file


    def __init__(self, file_object, mime_type=None):
        self.file_object = file_object
        self.mime_type = mime_type or get_mimetype(file_object=file_object, mimetype_only=False)[0]

        if self.mime_type in CONVERTER_OFFICE_FILE_MIMETYPES:
            if os.path.exists(LIBREOFFICE_PATH):
                #file_object, filename = mkstemp()

                # Cache results of conversion
                #output_filepath = os.path.join(TEMPORARY_DIRECTORY, ''.join([self.input_filepath, CACHED_FILE_SUFFIX]))

                result = Converter.soffice(file_object)
                file_object.close()
                self.file_object = result
                self.mime_type = 'application/pdf'

                #try:
                #    self.backend.convert(self.input_filepath, self.output_filepath)
                #    self.exists = True
                #except OfficeBackendError as exception:
                #    # convert exception so that at least the mime type icon is displayed
                #    raise UnknownFileFormat(exception)
                #else:
                #    result = office_converter.convert(self.file_object, mimetype=mime_type)
                #    self.file_object.close()
                #    self.file_object = result
            else:
                # TODO: NO LIBREOFFICE ERROR
                pass


    def transform(self, transformations, page=DEFAULT_PAGE_NUMBER):
        pass

    def convert(self, output_format=DEFAULT_FILE_FORMAT, page=DEFAULT_PAGE_NUMBER):#, *args, **kwargs):
        #size = kwargs.get('size')
        #file_format = kwargs.get('file_format', DEFAULT_FILE_FORMAT)
        #zoom = kwargs.get('zoom', DEFAULT_ZOOM_LEVEL)
        #rotation = kwargs.get('rotation', DEFAULT_ROTATION)
        #page = kwargs.get('page', DEFAULT_PAGE_NUMBER)
        #transformations = kwargs.get('transformations', [])

        #if transformations is None:
        #    transformations = []

        #if output_filepath is None:
        #    output_filepath = create_image_cache_filename(input_filepath, *args, **kwargs)

        #if os.path.exists(output_filepath):
        #    return output_filepath

        '''
        if office_converter:
            try:
                office_converter.convert(input_filepath, mimetype=mimetype)
                if office_converter.exists:
                    input_filepath = office_converter.output_filepath
                    mimetype = 'application/pdf'
                else:
                    # Recycle the already detected mimetype
                    mimetype = office_converter.mimetype

            except OfficeConversionError:
                raise UnknownFileFormat('office converter exception')

        if size:
            transformations.append(
                {
                    'transformation': TRANSFORMATION_RESIZE,
                    'arguments': dict(zip(['width', 'height'], size.split(DIMENSION_SEPARATOR)))
                }
            )

        if zoom != 100:
            transformations.append(
                {
                    'transformation': TRANSFORMATION_ZOOM,
                    'arguments': {'percent': zoom}
                }
            )

        if rotation != 0 and rotation != 360:
            transformations.append(
                {
                    'transformation': TRANSFORMATION_ROTATE,
                    'arguments': {'degrees': rotation}
                }
            )
        '''

        return backend.convert(file_object=self.file_object, mimetype=self.mime_type, output_format=output_format, page=page)

        def get_page_count(self):
            return backend.get_page_count(file_object)



'''
def get_available_transformations_choices():
    result = []
    for transformation in backend.get_available_transformations():
        result.append((transformation, TRANSFORMATION_CHOICES[transformation]['label']))

    return result
'''

