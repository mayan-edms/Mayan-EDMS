import os
import shlex
import subprocess
import tempfile

from documents.utils import from_descriptor_to_tempfile

from converter.conf.settings import CONVERT_PATH
from converter.conf.settings import OCR_OPTIONS

from converter import TEMPORARY_DIRECTORY


class ConvertError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message


def get_errors(error_string):
    '''
    returns all lines in the error_string that start with the string "error"

    '''
    lines = error_string.splitlines()
    return lines[0]
    #error_lines = (line for line in lines if line.find('error') >= 0)
    #return '\n'.join(error_lines)


def execute_convert(input_filepath, arguments, output_filepath):
    #TODO: Timeout & kill child
    command = [CONVERT_PATH, input_filepath]
    command.extend(shlex.split(str(arguments)))
    command.append(output_filepath)

    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())
    
#TODO: merge w/ convert
def in_cache(input_filepath, size, page=0, format='jpg'):
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    output_arg = '%s_%s%s%s' % (temp_path, size, os.extsep, format)
    input_arg = '%s[%s]' % (input_filepath, page)
    if os.path.exists(output_arg):
        return output_arg
    else:
        return None
    
    
def convert(input_filepath, size, cache=True, page=0, format='jpg'):
    #TODO: generate output file using lightweight hash function on
    #file name or file content
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    output_arg = '%s_%s%s%s' % (temp_path, size, os.extsep, format)
    input_arg = '%s[%s]' % (input_filepath, page)
    if os.path.exists(output_arg):
        return output_arg
    #TODO: Check mimetype and use corresponding utility
    try:
        status, error_string = execute_convert(input_arg, ['-resize', size], output_arg)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)
    finally:
        return output_arg
    

#TODO: slugify OCR_OPTIONS and add to file name to cache
def convert_document_for_ocr(document, page=0, format='tif'):
    #Extract document file
    document.file.open()
    desc = document.file.storage.open(document.file.path)
    input_filepath = from_descriptor_to_tempfile(desc, document.uuid)
        
    #Convert for OCR
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    output_arg = '%s_ocr%s%s%s' % (temp_path, page, os.extsep, format)
    input_arg = '%s[%s]' % (input_filepath, page)
    try:
        status, error_string = execute_convert(input_arg, OCR_OPTIONS, output_arg)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)
    finally:
        return output_arg
