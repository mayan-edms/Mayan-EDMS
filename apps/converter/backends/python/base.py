import tempfile
import os

import slate
from PIL import Image

try:
    import ghostscript
    USE_GHOSTSCRIPT = True
except RuntimeError:
    USE_GHOSTSCRIPT = False

from mimetype.api import get_mimetype

from converter.exceptions import UnknownFileFormat
from converter.backends import ConverterBase
from converter.literals import TRANSFORMATION_RESIZE, \
    TRANSFORMATION_ROTATE, TRANSFORMATION_ZOOM
from converter.literals import DEFAULT_PAGE_NUMBER, \
    DEFAULT_FILE_FORMAT
from converter.utils import cleanup


class ConverterClass(ConverterBase):
    def get_page_count(self, input_filepath):
        page_count = 1

        mimetype, encoding = get_mimetype(open(input_filepath, 'rb'), input_filepath, mimetype_only=True)
        if mimetype == 'application/pdf':
            # If file is a PDF open it with slate to determine the page
            # count
            with open(input_filepath) as fd:
                try:
                    pages = slate.PDF(fd)
                except:
                    return 1
                    # TODO: Maybe return UnknownFileFormat to display proper unknwon file format message in document description
            return len(pages)
            
        try:
            im = Image.open(input_filepath)
        except IOError:  # cannot identify image file
            raise UnknownFileFormat
            
        try:
            while 1:
                im.seek(im.tell() + 1)
                page_count += 1
                # do something to im
        except EOFError:
            pass  # end of sequence
            
        return page_count

    def convert_file(self, input_filepath, output_filepath, transformations=None, page=DEFAULT_PAGE_NUMBER, file_format=DEFAULT_FILE_FORMAT, **kwargs):
        tmpfile = None
        mimetype = kwargs.get('mimetype', None)
        if not mimetype:
            mimetype, encoding = get_mimetype(open(input_filepath, 'rb'), input_filepath, mimetype_only=True)

        if mimetype == 'application/pdf' and USE_GHOSTSCRIPT:
            # If file is a PDF open it with ghostscript and convert it to
            # TIFF
            first_page_tmpl = '-dFirstPage=%d' % page
            last_page_tmpl = '-dLastPage=%d' % page
            fd, tmpfile = tempfile.mkstemp()
            os.close(fd)
            output_file_tmpl = '-sOutputFile=%s' % tmpfile
            input_file_tmpl = '-f%s' % input_filepath
            args = [
                'gs', '-q', '-dQUIET', '-dSAFER', '-dBATCH',
                '-dNOPAUSE', '-dNOPROMPT', 
                first_page_tmpl, last_page_tmpl,
                '-sDEVICE=jpeg', '-dJPEGQ=95',
                '-r150', output_file_tmpl,
                input_file_tmpl,
                '-c "60000000 setvmthreshold"',  # use 30MB
                '-dNOGC',  # No garbage collection
                '-dMaxBitmap=500000000',
                '-dAlignToPixels=0',
                '-dGridFitTT=0',
                '-dTextAlphaBits=4',
                '-dGraphicsAlphaBits=4',                
            ] 

            ghostscript.Ghostscript(*args)
            page = 1  # Don't execute the following while loop
            input_filepath = tmpfile    

        try:
            im = Image.open(input_filepath)
        except Exception:
            # Python Imaging Library doesn't recognize it as an image
            raise UnknownFileFormat
        finally:
            if tmpfile:
                cleanup(tmpfile)
        
        current_page = 0
        try:
            while current_page == page - 1:
                im.seek(im.tell() + 1)
                current_page += 1
                # do something to im
        except EOFError:
            # end of sequence
            pass
        
        try:
            if transformations:
                aspect = 1.0 * im.size[0] / im.size[1]
                for transformation in transformations:
                    arguments = transformation.get('arguments')
                    if transformation['transformation'] == TRANSFORMATION_RESIZE:
                        width = int(arguments.get('width', 0))
                        height = int(arguments.get('height', 1.0 * width * aspect))
                        im = self.resize(im, (width, height))
                    elif transformation['transformation'] == TRANSFORMATION_ZOOM:
                        decimal_value = float(arguments.get('percent', 100)) / 100
                        im = im.transform((int(im.size[0] * decimal_value), int(im.size[1] * decimal_value)), Image.EXTENT, (0, 0, im.size[0], im.size[1])) 
                    elif transformation['transformation'] == TRANSFORMATION_ROTATE:
                        # PIL counter degress counter-clockwise, reverse them
                        im = im.rotate(360 - arguments.get('degrees', 0))
        except:
            # Ignore all transformation error
            pass

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
            if format_name == 'GBR':
                formats.append('GBR_PIL')
            else:
                formats.append(format_name)
        
        if USE_GHOSTSCRIPT:
            formats.append('PDF')
            formats.append('PS')
        
        return formats

    def get_available_transformations(self):
        return [
            TRANSFORMATION_RESIZE, TRANSFORMATION_ROTATE, \
            TRANSFORMATION_ZOOM
        ]

    # From: http://united-coders.com/christian-harms/image-resizing-tips-general-and-for-python
    def resize(self, img, box, fit=False, out=None):
        '''Downsample the image.
        @param img: Image -  an Image-object
        @param box: tuple(x, y) - the bounding box of the result image
        @param fit: boolean - crop the image to fill the box
        @param out: file-like-object - save the image into the output stream
        '''
        #preresize image with factor 2, 4, 8 and fast algorithm
        factor = 1
        while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
            factor *=2
        if factor > 1:
            img.thumbnail((img.size[0] / factor, img.size[1] / factor), Image.NEAREST)

        #calculate the cropping box and get the cropped part
        if fit:
            x1 = y1 = 0
            x2, y2 = img.size
            wRatio = 1.0 * x2 / box[0]
            hRatio = 1.0 * y2 / box[1]
            if hRatio > wRatio:
                y1 = y2 / 2 - box[1] * wRatio / 2
                y2 = y2 / 2 + box[1] * wRatio / 2
            else:
                x1 = x2 / 2 - box[0] * hRatio / 2
                x2 = x2 / 2 + box[0] * hRatio / 2
            img = img.crop((x1, y1, x2, y2))

        #Resize the image with best quality algorithm ANTI-ALIAS
        img.thumbnail(box, Image.ANTIALIAS)

        if out:
            #save it into a file-like object
            img.save(out, 'JPEG', quality=75)
        else:
            return img

        #if isinstance(self.regex, basestring):
        #    self.regex = re.compile(regex)
