import os
import shlex
import subprocess
import tempfile
import shutil

from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify


from converter.conf.settings import UNPAPER_PATH
from converter.conf.settings import OCR_OPTIONS
from converter.conf.settings import DEFAULT_OPTIONS
from converter.conf.settings import LOW_QUALITY_OPTIONS
from converter.conf.settings import HIGH_QUALITY_OPTIONS
from converter.conf.settings import GRAPHICS_BACKEND

from exceptions import ConvertError, UnknownFormat, UnpaperError, \
    IdentifyError, UnkownConvertError
    
#from converter.conf.settings import UNOCONV_PATH
from common import TEMPORARY_DIRECTORY
from converter import TRANFORMATION_CHOICES
from documents.utils import document_save_to_temp_dir

QUALITY_DEFAULT = 'quality_default'
QUALITY_LOW = 'quality_low'
QUALITY_HIGH = 'quality_high'

QUALITY_SETTINGS = {QUALITY_DEFAULT:DEFAULT_OPTIONS, QUALITY_LOW:LOW_QUALITY_OPTIONS,
    QUALITY_HIGH:HIGH_QUALITY_OPTIONS}

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
    
backend = _get_backend()

def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass

def execute_unpaper(input_filepath, output_filepath):
    command = []
    command.append(UNPAPER_PATH)
    command.append('--overwrite')
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

        
def cache_cleanup(input_filepath, size, page=0, format='jpg'):
    filepath = create_image_cache_filename(input_filepath, size, page, format)
    try:
        os.remove(filepath)
    except OSError:
        pass

def create_image_cache_filename(input_filepath, quality=QUALITY_DEFAULT, extra_options='', *args, **kwargs):
    if input_filepath:
        temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
        temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)

        final_filepath = []
        [final_filepath.append(str(arg)) for arg in args]
        final_filepath.extend(['%s_%s' % (key, value) for key, value in kwargs.items()])
        final_filepath.append(QUALITY_SETTINGS[quality])
        final_filepath.append(extra_options)
        
        temp_path += slugify('_'.join(final_filepath))

        return temp_path
    else:
        return None
   
def in_image_cache(input_filepath, size, page=0, format='jpg', quality=QUALITY_DEFAULT, extra_options=''):
    output_filepath = create_image_cache_filename(input_filepath, size=size, page=page, format=format, quality=quality, extra_options=extra_options)
    if os.path.exists(output_filepath):
        return output_filepath
    else:
        return None
    
def convert(input_filepath, size, quality=QUALITY_DEFAULT, cache=True, page=0, format='jpg', extra_options='', mimetype=None, extension=None, cleanup_files=True):
    unoconv_output = None
    output_filepath = create_image_cache_filename(input_filepath, size=size, page=page, format=format, quality=quality, extra_options=extra_options)
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
        input_arg = '%s[%s]' % (input_filepath, page)
        extra_options += ' -resize %s' % size
        backend.execute_convert(input_filepath=input_arg, arguments=extra_options, output_filepath='%s:%s' % (format, output_filepath), quality=quality)
    finally:
        if cleanup_files:
            cleanup(input_filepath)
        if unoconv_output:
            cleanup(unoconv_output)
        
    return output_filepath

def get_page_count(input_filepath):
    try:
        return int(backend.execute_identify(input_filepath, '-format %n'))
    except Exception, e:
        #TODO: send to other page number identifying program
        return 1

def convert_document_for_ocr(document, page=0, format='tif'):
    #Extract document file
    input_filepath = document_save_to_temp_dir(document, document.uuid)
            
    #Convert for OCR
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    transformation_output_file = '%s_trans%s%s%s' % (temp_path, page, os.extsep, format)
    unpaper_input_file = '%s_unpaper_in%s%spnm' % (temp_path, page, os.extsep)
    unpaper_output_file = '%s_unpaper_out%s%spnm' % (temp_path, page, os.extsep)
    convert_output_file = '%s_ocr%s%s%s' % (temp_path, page, os.extsep, format)
    
    input_arg = '%s[%s]' % (input_filepath, page)

    transformation_list = []
    try:
        #Catch invalid or non existing pages
        document_page = document.documentpage_set.get(document=document, page_number=page+1)
        for page_transformation in document_page.documentpagetransformation_set.all():
            try:
                if page_transformation.transformation in TRANFORMATION_CHOICES:
                    output = TRANFORMATION_CHOICES[page_transformation.transformation] % eval(page_transformation.arguments)
                    transformation_list.append(output)
            except Exception, e:
                if request.user.is_staff:
                    messages.warning(request, _(u'Error for transformation %(transformation)s:, %(error)s') % 
                        {'transformation':page_transformation.get_transformation_display(),
                        'error':e})
                else:
                    pass
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
