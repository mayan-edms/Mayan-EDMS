import os
import subprocess

from django.utils.importlib import import_module
from django.template.defaultfilters import slugify

from common import TEMPORARY_DIRECTORY
from documents.utils import document_save_to_temp_dir

from converter.conf.settings import UNPAPER_PATH
from converter.conf.settings import OCR_OPTIONS
from converter.conf.settings import UNOCONV_PATH
from converter.exceptions import UnpaperError, OfficeConversionError
from converter.literals import DEFAULT_PAGE_NUMBER, \
    DEFAULT_OCR_FILE_FORMAT, QUALITY_DEFAULT, DEFAULT_ZOOM_LEVEL, \
    DEFAULT_ROTATION, DEFAULT_FILE_FORMAT, QUALITY_PRINT

from converter import backend
from converter.literals import TRANSFORMATION_CHOICES
from converter.literals import TRANSFORMATION_RESIZE, \
    TRANSFORMATION_ROTATE, TRANSFORMATION_DENSITY, \
    TRANSFORMATION_ZOOM
from converter.literals import DIMENSION_SEPARATOR    

    
CONVERTER_OFFICE_FILE_EXTENSIONS = [
    u'ods', u'docx', u'doc'
]

def cleanup(filename):
    """
    Tries to remove the given filename. Ignores non-existent files
    """
    try:
        os.remove(filename)
    except OSError:
        pass


def execute_unpaper(input_filepath, output_filepath):
    """
    Executes the program unpaper using subprocess's Popen
    """
    command = []
    command.append(UNPAPER_PATH)
    command.append(u'--overwrite')
    command.append(input_filepath)
    command.append(output_filepath)
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        raise UnpaperError(proc.stderr.readline())


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
        temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
        temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)

        final_filepath = []
        [final_filepath.append(str(arg)) for arg in args]
        final_filepath.extend([u'%s_%s' % (key, value) for key, value in kwargs.items()])

        temp_path += slugify(u'_'.join(final_filepath))

        return temp_path
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


def convert(input_filepath, *args, **kwargs):
    size = kwargs.get('size')
    file_format = kwargs.get('file_format', DEFAULT_FILE_FORMAT)
    zoom = kwargs.get('zoom', DEFAULT_ZOOM_LEVEL)
    rotation = kwargs.get('rotation', DEFAULT_ROTATION)
    page = kwargs.get('page', DEFAULT_PAGE_NUMBER)
    cleanup_files = kwargs.get('cleanup_files', True)
    quality = kwargs.get('quality', QUALITY_DEFAULT)
    transformations = kwargs.get('transformations', [])

    unoconv_output = None

    output_filepath = create_image_cache_filename(input_filepath, *args, **kwargs)
    #if os.path.exists(output_filepath):
    #    return output_filepath

    path, extension = os.path.splitext(input_filepath)
    if extension[1:].lower() in CONVERTER_OFFICE_FILE_EXTENSIONS:
        result = convert_office_document(input_filepath)
        if result:
            unoconv_output = result
            input_filepath = result
            extra_options = u''

    #TODO: not here in the backend
    input_arg = u'%s[%s]' % (input_filepath, page-1)
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
        backend.convert_file(input_filepath=input_arg, output_filepath=u'%s:%s' % (file_format, output_filepath), quality=quality, transformations=transformations)
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


def convert_document_for_ocr(document, page=DEFAULT_PAGE_NUMBER, file_format=DEFAULT_OCR_FILE_FORMAT):
    #Extract document file
    input_filepath = document_save_to_temp_dir(document, document.uuid)

    #Convert for OCR
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    transformation_output_file = u'%s_trans%s%s%s' % (temp_path, page, os.extsep, file_format)
    unpaper_input_file = u'%s_unpaper_in%s%spnm' % (temp_path, page, os.extsep)
    unpaper_output_file = u'%s_unpaper_out%s%spnm' % (temp_path, page, os.extsep)
    convert_output_file = u'%s_ocr%s%s%s' % (temp_path, page, os.extsep, file_format)

    input_arg = u'%s[%s]' % (input_filepath, page-1)

    try:
        document_page = document.documentpage_set.get(page_number=page + 1)
        transformation_string, warnings = document_page.get_transformation_string()

        #Apply default transformations
        backend.convert_file(input_filepath=input_arg, quality=QUALITY_HIGH, arguments=transformation_string, output_filepath=transformation_output_file)
        #Do OCR operations
        backend.convert_file(input_filepath=transformation_output_file, arguments=OCR_OPTIONS, output_filepath=unpaper_input_file)
        # Process by unpaper
        execute_unpaper(input_filepath=unpaper_input_file, output_filepath=unpaper_output_file)
        # Convert to tif
        backend.convert_file(input_filepath=unpaper_output_file, output_filepath=convert_output_file)
    finally:
        cleanup(transformation_output_file)
        cleanup(unpaper_input_file)
        cleanup(unpaper_output_file)

    return convert_output_file


def get_available_transformations_choices():
    result = []
    for transformation in backend.get_available_transformations():
        transformation_template = u'%s %s' % (TRANSFORMATION_CHOICES[transformation]['label'], u','.join(['<%s>' % argument['name'] if argument['required'] else '[%s]' % argument['name'] for argument in TRANSFORMATION_CHOICES[transformation]['arguments']]))
        result.append([transformation, transformation_template])
        
    return result
