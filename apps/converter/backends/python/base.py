from PIL import Image

from django.utils.translation import ugettext_lazy as _

from converter.literals import QUALITY_DEFAULT, QUALITY_SETTINGS
from converter.exceptions import ConvertError, UnknownFormat, IdentifyError
from converter.backends import ConverterBase
from converter.literals import TRANSFORMATION_RESIZE, \
    TRANSFORMATION_ROTATE

class ConverterClass(ConverterBase):
    def identify_file(self, input_filepath, arguments=None):
        pass


    def get_page_count(self, input_filepath):
        page_count = 1
        im = Image.open(input_filepath)

        try:
            while 1:
                im.seek(im.tell()+1)
                page_count += 1
                # do something to im
        except EOFError:
            pass # end of sequence
            
        return page_count
        
            
    def convert_file(self, input_filepath, output_filepath, quality=QUALITY_DEFAULT, arguments=None):
        im = Image.open(input_filepath)
        outfile, format = output_filepath.split(u':')
        im.save(outfile, format)
        '''
        command = []
        command.append(unicode(GM_PATH))
        command.append(u'convert')
        command.extend(unicode(QUALITY_SETTINGS[quality]).split())
        command.extend(unicode(GM_SETTINGS).split())
        command.append(unicode(input_filepath))
        if arguments:
            command.extend(unicode(arguments).split())
        command.append(unicode(output_filepath))
        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return_code = proc.wait()
        if return_code != 0:
            #Got an error from convert program
            error_line = proc.stderr.readline()
            if (CONVERTER_ERROR_STRING_NO_DECODER in error_line) or (CONVERTER_ERROR_STARTS_WITH in error_line):
                #Try to determine from error message which class of error is it
                raise UnknownFormat
            else:
                raise ConvertError(error_line)
        '''

    def get_format_list(self):
        """
        Introspect PIL's internal registry to obtain a list of the
        supported file types
        """
        formats = []
        for format_name in Image.ID:
            formats.append((format_name, u''))
        
        return formats


    def get_available_transformations(self):
        return [
            TRANSFORMATION_RESIZE, TRANSFORMATION_ROTATE
        ]


    def get_page_count(self, input_filepath):
        try:
            return len(self.identify_file(unicode(input_filepath)).splitlines())
        except:
            #TODO: send to other page number identifying program
            return 1
