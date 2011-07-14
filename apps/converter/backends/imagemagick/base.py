import subprocess
import re

from django.utils.translation import ugettext_lazy as _

from converter.conf.settings import IM_IDENTIFY_PATH
from converter.conf.settings import IM_CONVERT_PATH
from converter.api import QUALITY_DEFAULT, QUALITY_SETTINGS
from converter.exceptions import ConvertError, UnknownFormat, \
    IdentifyError
from converter.backends import ConverterBase

CONVERTER_ERROR_STRING_NO_DECODER = u'no decode delegate for this image format'


class ConverterClass(ConverterBase):
    def identify_file(self, input_filepath, arguments=None):
        command = []
        command.append(unicode(IM_IDENTIFY_PATH))
        if arguments:
            command.extend(arguments)
        command.append(unicode(input_filepath))

        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        if return_code != 0:
            raise IdentifyError(proc.stderr.readline())
        return proc.stdout.read()


    def convert_file(self, input_filepath, output_filepath, quality=QUALITY_DEFAULT, arguments=None):
        command = []
        command.append(unicode(IM_CONVERT_PATH))
        command.extend(unicode(QUALITY_SETTINGS[quality]).split())
        command.append(unicode(input_filepath))
        if arguments:
            command.extend(unicode(arguments).split())
        command.append(unicode(output_filepath))
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


    def get_format_list(self):
        """
        Call ImageMagick to parse all of it's supported file formats, and
        return a list of the names and descriptions
        """
        format_regex = re.compile(' *([A-Z0-9]+)[*]? +([A-Z0-9]+) +([rw\-+]+) *(.*).*')
        formats = []
        command = []
        command.append(unicode(IM_CONVERT_PATH))
        command.append(u'-list')
        command.append(u'format')
        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        if return_code != 0:
            raise ConvertError(proc.stderr.readline())
        
        for line in proc.stdout.readlines():
            fields = format_regex.findall(line)
            if fields:
                formats.append((fields[0][0], fields[0][3]))
        
        return formats


    def get_available_transformations(self):
        return {
            'rotate': {
                'label': _(u'Rotate [degrees]'),
                'arguments': [{'name': 'degrees'}],
                'command_line': u'-rotate %(degrees)d'
            }
        }
