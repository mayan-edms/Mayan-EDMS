import os

import subprocess
import tempfile

#from django.core.files.base import File
from documents.conf.settings import TEMPORARY_DIRECTORY

def convert(input_filepath, size, cache=True, page=0, format='jpg'):
    temp_directory = TEMPORARY_DIRECTORY if TEMPORARY_DIRECTORY else tempfile.mkdtemp()
    #TODO: generate output file using lightweight hash function on
    #file name or file content
    #descriptor, temp_filepath = tempfile.mkstemp()

    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(temp_directory, temp_filename)
    output_arg = '%s_%s%s%s' % (temp_path, size, os.extsep, format)
    input_arg = '%s[%s]' % (input_filepath, page)
    if os.path.exists(output_arg):
        return output_arg
        
    #TODO: Check mimetype and use corresponding utility
    convert = subprocess.Popen(['convert', input_arg, '-resize', size,  output_arg])
    return_code = convert.wait()
    if return_code:
        raise Exception
    #TODO: check return code & messages
    #TODO: Timeout & kill child
    return output_arg
