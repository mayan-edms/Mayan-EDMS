import subprocess
import re

from converter.conf.settings import IM_IDENTIFY_PATH
from converter.conf.settings import IM_CONVERT_PATH
from converter.exceptions import ConvertError, UnknownFileFormat, \
    IdentifyError
from converter.backends import ConverterBase
from converter.literals import TRANSFORMATION_RESIZE, \
    TRANSFORMATION_ROTATE, TRANSFORMATION_DENSITY, \
    TRANSFORMATION_ZOOM
from converter.literals import DIMENSION_SEPARATOR, DEFAULT_PAGE_NUMBER, \
    DEFAULT_FILE_FORMAT
    
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

    def convert_file(self, input_filepath, output_filepath, transformations=None, page=DEFAULT_PAGE_NUMBER, file_format=DEFAULT_FILE_FORMAT, **kwargs):
        arguments = []
        try:
            if transformations:
                for transformation in transformations:
                    if transformation['transformation'] == TRANSFORMATION_RESIZE:
                        dimensions = []
                        dimensions.append(unicode(transformation['arguments']['width']))
                        if 'height' in transformation['arguments']:
                            dimensions.append(unicode(transformation['arguments']['height']))                    
                        arguments.append(u'-resize')
                        arguments.append(u'%s' % DIMENSION_SEPARATOR.join(dimensions))

                    elif transformation['transformation'] == TRANSFORMATION_ZOOM:
                        arguments.append(u'-resize')
                        arguments.append(u'%d%%' % transformation['arguments']['percent'])
                        
                    elif transformation['transformation'] == TRANSFORMATION_ROTATE:
                        arguments.append(u'-rotate')
                        arguments.append(u'%s' % transformation['arguments']['degrees'])
        except:
            pass
                    
        if file_format.lower() == u'jpeg' or file_format.lower() == u'jpg':
            arguments.append(u'-quality')
            arguments.append(u'85')
        
        # Imagemagick page number is 0 base
        input_arg = u'%s[%d]' % (input_filepath, page - 1)

        # Specify the file format next to the output filename
        output_filepath = u'%s:%s' % (file_format, output_filepath)
                  
        command = []
        command.append(unicode(IM_CONVERT_PATH))
        command.append(unicode(input_arg))
        if arguments:
            command.extend(arguments)
        command.append(unicode(output_filepath))
        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        if return_code != 0:
            #Got an error from convert program
            error_line = proc.stderr.readline()
            if CONVERTER_ERROR_STRING_NO_DECODER in error_line:
                #Try to determine from error message which class of error is it
                raise UnknownFileFormat
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
                formats.append(fields[0][0])
        
        return formats


    def get_available_transformations(self):
        return [
            TRANSFORMATION_RESIZE, TRANSFORMATION_ROTATE, \
            TRANSFORMATION_ZOOM
        ]


    def get_page_count(self, input_filepath):
        try:
            return len(self.identify_file(unicode(input_filepath)).splitlines())
        except IdentifyError:
            raise UnknownFileFormat
