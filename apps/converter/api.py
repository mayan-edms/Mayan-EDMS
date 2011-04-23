import os
import subprocess

from django.utils.importlib import import_module
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

from converter.conf.settings import UNPAPER_PATH
from converter.conf.settings import OCR_OPTIONS
from converter.conf.settings import DEFAULT_OPTIONS
from converter.conf.settings import LOW_QUALITY_OPTIONS
from converter.conf.settings import HIGH_QUALITY_OPTIONS
from converter.conf.settings import GRAPHICS_BACKEND

from converter.exceptions import UnpaperError

#from converter.conf.settings import UNOCONV_PATH
from common import TEMPORARY_DIRECTORY
from converter import TRANFORMATION_CHOICES
from documents.utils import document_save_to_temp_dir

QUALITY_DEFAULT = u'quality_default'
QUALITY_LOW = u'quality_low'
QUALITY_HIGH = u'quality_high'

QUALITY_SETTINGS = {QUALITY_DEFAULT: DEFAULT_OPTIONS,
    QUALITY_LOW: LOW_QUALITY_OPTIONS, QUALITY_HIGH: HIGH_QUALITY_OPTIONS}


def _lazy_load(fn):
    _cached = []

    def _decorated():
        if not _cached:
            _cached.append(fn())
        return _cached[0]
    return _decorated


@_lazy_load
def _get_backend():
    return import_module(GRAPHICS_BACKEND)

try:
    backend = _get_backend()
except ImportError:
    raise ImportError(u'Missing or incorrect converter backend: %s' % GRAPHICS_BACKEND)


def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass


def execute_unpaper(input_filepath, output_filepath):
    command = []
    command.append(UNPAPER_PATH)
    command.append(u'--overwrite')
    command.append(input_filepath)
    command.append(output_filepath)
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        raise UnpaperError(proc.stderr.readline())
"""
def execute_unoconv(input_filepath, output_filepath, arguments=''):
    command = [UNOCONV_PATH]
    command.extend(['--stdout'])
    command.extend(shlex.split(str(arguments)))
    command.append(input_filepath)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(output_filepath, 'w') as output:
        shutil.copyfileobj(proc.stdout, output)
    return (proc.wait(), proc.stderr.read())
"""


def cache_cleanup(input_filepath, size, quality=QUALITY_DEFAULT, page=0, file_format=u'jpg', extra_options=u''):
    filepath = create_image_cache_filename(input_filepath, size=size, page=page, file_format=file_format, quality=quality, extra_options=extra_options)
    try:
        os.remove(filepath)
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


def in_image_cache(input_filepath, size, page=0, file_format=u'jpg', quality=QUALITY_DEFAULT, extra_options=u'', zoom=100, rotation=0):
    output_filepath = create_image_cache_filename(input_filepath, size=size, page=page, file_format=file_format, quality=quality, extra_options=extra_options, zoom=zoom, rotation=rotation)
    if os.path.exists(output_filepath):
        return output_filepath
    else:
        return None


def convert(input_filepath, size, quality=QUALITY_DEFAULT, page=0, file_format=u'jpg', extra_options=u'', cleanup_files=True, zoom=100, rotation=0):
    unoconv_output = None
    output_filepath = create_image_cache_filename(input_filepath, size=size, page=page, file_format=file_format, quality=quality, extra_options=extra_options, zoom=zoom, rotation=rotation)
    if os.path.exists(output_filepath):
        return output_filepath
    '''
    if extension:
        if extension.lower() == 'ods':
            unoconv_output = '%s_pdf' % output_filepath
            status, error_string = execute_unoconv(input_filepath, unoconv_output, arguments='-f pdf')
            if status:
                errors = get_errors(error_string)
                raise ConvertError(status, errors)
            cleanup(input_filepath)
            input_filepath = unoconv_output
    '''
    try:
        input_arg = u'%s[%s]' % (input_filepath, page)
        extra_options += u' -resize %s' % size
        if zoom != 100:
            extra_options += u' -resize %d%% ' % zoom

        if rotation != 0 and rotation != 360:
            extra_options += u' -rotate %d ' % rotation

        if format == u'jpg':
            extra_options += u' -quality 85'

        backend.execute_convert(input_filepath=input_arg, arguments=extra_options, output_filepath=u'%s:%s' % (file_format, output_filepath), quality=quality)
    finally:
        if cleanup_files:
            cleanup(input_filepath)
        if unoconv_output:
            cleanup(unoconv_output)

    return output_filepath


def get_page_count(input_filepath):
    try:
        return len(backend.execute_identify(unicode(input_filepath)).splitlines())
    except Exception, e:
        #TODO: send to other page number identifying program
        return 1


def convert_document_for_ocr(document, page=0, file_format=u'tif'):
    #Extract document file
    input_filepath = document_save_to_temp_dir(document, document.uuid)

    #Convert for OCR
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    transformation_output_file = u'%s_trans%s%s%s' % (temp_path, page, os.extsep, format)
    unpaper_input_file = u'%s_unpaper_in%s%spnm' % (temp_path, page, os.extsep)
    unpaper_output_file = u'%s_unpaper_out%s%spnm' % (temp_path, page, os.extsep)
    convert_output_file = u'%s_ocr%s%s%s' % (temp_path, page, os.extsep, file_format)

    input_arg = u'%s[%s]' % (input_filepath, page)

    transformation_list = []
    try:
        #Catch invalid or non existing pages
        document_page = document.documentpage_set.get(document=document, page_number=page + 1)
        for page_transformation in document_page.documentpagetransformation_set.all():
            if page_transformation.transformation in TRANFORMATION_CHOICES:
                output = TRANFORMATION_CHOICES[page_transformation.transformation] % eval(page_transformation.arguments)
                transformation_list.append(output)
    except ObjectDoesNotExist:
        pass

    tranformation_string = ' '.join(transformation_list)
    try:
        #Apply default transformations
        backend.execute_convert(input_filepath=input_arg, quality=QUALITY_HIGH, arguments=tranformation_string, output_filepath=transformation_output_file)
        #Do OCR operations
        backend.execute_convert(input_filepath=transformation_output_file, arguments=OCR_OPTIONS, output_filepath=unpaper_input_file)
        # Process by unpaper
        execute_unpaper(input_filepath=unpaper_input_file, output_filepath=unpaper_output_file)
        # Convert to tif
        backend.execute_convert(input_filepath=unpaper_output_file, output_filepath=convert_output_file)
    finally:
        cleanup(transformation_output_file)
        cleanup(unpaper_input_file)
        cleanup(unpaper_output_file)

    return convert_output_file
