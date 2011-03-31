import shlex
import subprocess

from converter.conf.settings import GM_PATH
from converter.api import QUALITY_DEFAULT, QUALITY_SETTINGS
from converter.exceptions import ConvertError, UnknownFormat, UnpaperError, \
    IdentifyError, UnkownConvertError

CONVERTER_ERROR_STRING_NO_DECODER = 'No decode delegate for this image format'

def execute_identify(input_filepath, arguments):
    command = []
    command.append(GM_PATH)
    command.append(u'identify')
    command.extend(shlex.split(str(arguments)))
    command.append(input_filepath)

    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        raise IdentifyError(proc.stderr.readline())
    return proc.stdout.read()
    
def execute_convert(input_filepath, output_filepath, quality=QUALITY_DEFAULT, arguments=None):
    command = []
    command.append(GM_PATH)
    command.append(u'convert')
    command.extend(shlex.split(str(QUALITY_SETTINGS[quality])))
    command.append(input_filepath)
    if arguments:
        command.extend(shlex.split(str(arguments)))
    command.append(output_filepath)
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        #Got an error from convert program
        error_line = proc.stderr.readline()
        if CONVERTER_ERROR_STRING_NO_DECODER in error_line:
            #Try to determine from error message which class of error is it
            raise UnknownFormat
        else:
            raise ConvertError(error_line)
