import os
import subprocess
import hashlib

from common import TEMPORARY_DIRECTORY
from documents.utils import document_save_to_temp_dir

from converter.conf.settings import UNOCONV_PATH
from converter.exceptions import OfficeConversionError
from converter.literals import DEFAULT_PAGE_NUMBER, \
    QUALITY_DEFAULT, DEFAULT_ZOOM_LEVEL, \
    DEFAULT_ROTATION, DEFAULT_FILE_FORMAT, QUALITY_HIGH

from converter import backend
from converter.literals import TRANSFORMATION_CHOICES
from converter.literals import TRANSFORMATION_RESIZE, \
    TRANSFORMATION_ROTATE, TRANSFORMATION_DENSITY, \
    TRANSFORMATION_ZOOM
from converter.literals import DIMENSION_SEPARATOR    
from converter.utils import cleanup

HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()
    
CONVERTER_OFFICE_FILE_EXTENSIONS = [
    u'ods', u'docx', u'doc'
]


def execute_unoconv(input_filepath, arguments=''):
    """
    Executes the program unoconv using subprocess's Popen
    """
    command = []
    command.append(UNOCONV_PATH)
    command.extend(unicode(arguments).split())
    command.append(input_filepath)
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        raise OfficeConversionError(proc.stderr.readline())


def cache_cleanup(input_filepath, *args, **kwargs):
    try:
        os.remove(create_image_cache_filename(input_filepath, *args, **kwargs))
    except OSError:
        pass


def create_image_cache_filename(input_filepath, *args, **kwargs):
    if input_filepath:
        hash_value = HASH_FUNCTION(u''.join([input_filepath, unicode(args), unicode(kwargs)]))
        return os.path.join(TEMPORARY_DIRECTORY, hash_value)
    else:
        return None
        

def convert_office_document(input_filepath):
    if os.path.exists(UNOCONV_PATH):
        execute_unoconv(input_filepath, arguments='-f pdf')
        return input_filepath + u'.pdf'
    return None


def convert_document(document, *args, **kwargs):
    document_filepath = create_image_cache_filename(document.checksum, *args, **kwargs)
    if os.path.exists(document_filepath):
        return document_filepath

    return convert(document_save_to_temp_dir(document, document.checksum), *args, **kwargs)


def convert(input_filepath, cleanup_files=True, *args, **kwargs):
    size = kwargs.get('size')
    file_format = kwargs.get('file_format', DEFAULT_FILE_FORMAT)
    zoom = kwargs.get('zoom', DEFAULT_ZOOM_LEVEL)
    rotation = kwargs.get('rotation', DEFAULT_ROTATION)
    page = kwargs.get('page', DEFAULT_PAGE_NUMBER)
    quality = kwargs.get('quality', QUALITY_DEFAULT)
    transformations = kwargs.get('transformations', [])

    unoconv_output = None

    output_filepath = create_image_cache_filename(input_filepath, *args, **kwargs)
    if os.path.exists(output_filepath):
        return output_filepath

    path, extension = os.path.splitext(input_filepath)
    if extension[1:].lower() in CONVERTER_OFFICE_FILE_EXTENSIONS:
        result = convert_office_document(input_filepath)
        if result:
            unoconv_output = result
            input_filepath = result

    if size:
        transformations.append(
            {
                'transformation': TRANSFORMATION_RESIZE,
                'arguments': dict(zip([u'width', u'height'], size.split(DIMENSION_SEPARATOR)))
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

    try:
        backend.convert_file(input_filepath=input_filepath, output_filepath=output_filepath, quality=quality, transformations=transformations, page=page, file_format=file_format)
    finally:
        if cleanup_files:
            cleanup(input_filepath)
        if unoconv_output:
            cleanup(unoconv_output)

    return output_filepath


def get_page_count(input_filepath):
    return backend.get_page_count(input_filepath)


def get_document_dimensions(document, *args, **kwargs):
    document_filepath = create_image_cache_filename(document.checksum, *args, **kwargs)
    if os.path.exists(document_filepath):
        options = [u'-format', u'%w %h']
        return [int(dimension) for dimension in backend.identify_file(unicode(document_filepath), options).split()]
    else:
        return [0, 0]


def get_available_transformations_choices():
    result = []
    for transformation in backend.get_available_transformations():
        transformation_template = u'%s %s' % (TRANSFORMATION_CHOICES[transformation]['label'], u','.join(['<%s>' % argument['name'] if argument['required'] else '[%s]' % argument['name'] for argument in TRANSFORMATION_CHOICES[transformation]['arguments']]))
        result.append([transformation, transformation_template])
        
    return result
