import os
import shlex
import subprocess
import tempfile
import shutil

from django.template.defaultfilters import slugify

from converter.conf.settings import CONVERT_PATH
from converter.conf.settings import UNPAPER_PATH
from converter.conf.settings import IDENTIFY_PATH
from converter.conf.settings import OCR_OPTIONS
from converter.conf.settings import DEFAULT_OPTIONS
from converter.conf.settings import LOW_QUALITY_OPTIONS
from converter.conf.settings import HIGH_QUALITY_OPTIONS

#from converter.conf.settings import UNOCONV_PATH

from converter import TEMPORARY_DIRECTORY, TRANFORMATION_CHOICES
from utils import from_descriptor_to_tempfile


QUALITY_DEFAULT = 'quality_default'
QUALITY_LOW = 'quality_low'
QUALITY_HIGH = 'quality_high'

QUALITY_SETTINGS = {QUALITY_DEFAULT:DEFAULT_OPTIONS, QUALITY_LOW:LOW_QUALITY_OPTIONS,
    QUALITY_HIGH:HIGH_QUALITY_OPTIONS}

class ConvertError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass

def get_errors(error_string):
    '''
    returns all lines in the error_string that start with the string "error"

    '''
    lines = error_string.splitlines()
    return lines[0]
    #error_lines = (line for line in lines if line.find('error') >= 0)
    #return '\n'.join(error_lines)


#TODO: Timeout & kill child
def execute_convert(input_filepath, output_filepath, quality=QUALITY_DEFAULT, arguments=None):
    command = []
    command.append(CONVERT_PATH)
    command.extend(shlex.split(str(QUALITY_SETTINGS[quality])))
    command.append(input_filepath)
    if arguments:
        command.extend(shlex.split(str(arguments)))
    command.append(output_filepath)
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())


def execute_unpaper(input_filepath, output_filepath):
    command = []
    command.append(UNPAPER_PATH)
    command.append('--overwrite')
    command.append(input_filepath)
    command.append(output_filepath)
    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())


def execute_unoconv(input_filepath, output_filepath, arguments=''):
    command = [UNOCONV_PATH]
    command.extend(['--stdout'])
    command.extend(shlex.split(str(arguments)))
    command.append(input_filepath)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(output_filepath, 'w') as output:
        shutil.copyfileobj(proc.stdout, output)
    return (proc.wait(), proc.stderr.read())


def execute_identify(input_filepath, arguments):
    command = []
    command.append(IDENTIFY_PATH)
    command.extend(shlex.split(str(arguments)))
    command.append(input_filepath)

    proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read(), proc.stdout.read())


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
    #TODO: Check mimetype and use corresponding utility
    try:
        input_arg = '%s[%s]' % (input_filepath, page)
        extra_options += ' -resize %s' % size
        status, error_string = execute_convert(input_filepath=input_arg, arguments=extra_options, output_filepath='%s:%s' % (format, output_filepath), quality=quality)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)
    finally:
        if cleanup_files:
            cleanup(input_filepath)
        if unoconv_output:
            cleanup(unoconv_output)
        return output_filepath


def get_page_count(input_filepath):
    try:
        status, error_string, output = execute_identify(input_filepath, '-format %n')
        if status:
            errors = get_errors(error_string)
            return 1
            #raise ConvertError(status, errors)
    finally:
        if output:
            return int(output)
        else:
            return 1

#TODO: slugify OCR_OPTIONS and add to file name to cache
def convert_document_for_ocr(document, page=0, format='tif'):
    #Extract document file
    document.file.open()
    desc = document.file.storage.open(document.file.path)
    input_filepath = from_descriptor_to_tempfile(desc, document.uuid)
        
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
        status, error_string = execute_convert(input_filepath=input_arg, quality=QUALITY_HIGH, arguments=tranformation_string, output_filepath=transformation_output_file)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)
        #Do OCR operations
        status, error_string = execute_convert(input_filepath=transformation_output_file, arguments=OCR_OPTIONS, output_filepath=unpaper_input_file)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)        
        # Process by unpaper
        status, error_string = execute_unpaper(input_filepath=unpaper_input_file, output_filepath=unpaper_output_file)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)        
        # Convert to tif
        status, error_string = execute_convert(input_filepath=unpaper_output_file, output_filepath=convert_output_file)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)
    finally:
        cleanup(transformation_output_file)
        cleanup(unpaper_input_file)
        cleanup(unpaper_output_file)
        return convert_output_file
