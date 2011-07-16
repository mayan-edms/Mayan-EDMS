from PIL import Image

from django.utils.translation import ugettext_lazy as _

from converter.literals import QUALITY_DEFAULT, QUALITY_SETTINGS
from converter.exceptions import ConvertError, UnknownFormat, IdentifyError
from converter.backends import ConverterBase
from converter.literals import TRANSFORMATION_RESIZE, \
    TRANSFORMATION_ROTATE, TRANSFORMATION_ZOOM
from converter.literals import QUALITY_DEFAULT, DEFAULT_PAGE_NUMBER, \
    DEFAULT_FILE_FORMAT

class ConverterClass(ConverterBase):
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
    
    def convert_file(self, input_filepath, output_filepath, transformations=None, quality=QUALITY_DEFAULT, page=DEFAULT_PAGE_NUMBER, file_format=DEFAULT_FILE_FORMAT):
        try:
            im = Image.open(input_filepath)
        except Exception: # Python Imaging Library doesn't recognize it as an image
            raise UnknownFormat
        
        current_page = 0
        try:
            while current_page == page - 1:
                im.seek(im.tell() + 1)
                current_page += 1
                # do something to im
        except EOFError:
            pass # end of sequence        

        if transformations:
            for transformation in transformations:
                aspect = 1.0 * im.size[1] / im.size[0]
                if transformation['transformation'] == TRANSFORMATION_RESIZE:
                    width = int(transformation['arguments']['width'])
                    height = int(transformation['arguments'].get('height', 1.0 * width * aspect))
                    im = im.resize((width, height), Image.ANTIALIAS)
                elif transformation['transformation'] == TRANSFORMATION_ZOOM:
                    decimal_value = float(transformation['arguments']['percent']) / 100
                    im = im.transform((im.size[0] * decimal_value, im.size[1] * decimal_value), Image.EXTENT, (0, 0, im.size[0], im.size[1])) 
                elif transformation['transformation'] == TRANSFORMATION_ROTATE:
                    # PIL counter degress counter-clockwise, reverse them
                    im = im.rotate(360 - transformation['arguments']['degrees'])

        if im.mode not in ('L', 'RGB'):
            im = im.convert('RGB')
        im.save(output_filepath, format=file_format)

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
            TRANSFORMATION_RESIZE, TRANSFORMATION_ROTATE, \
            TRANSFORMATION_ZOOM
        ]
