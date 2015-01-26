from __future__ import unicode_literals

import io
import logging

import slate
from PIL import Image
import sh

from common.utils import fs_cleanup
from mimetype.api import get_mimetype

from . import ConverterBase
from ..exceptions import ConvertError, UnknownFileFormat
from ..literals import (
    DEFAULT_FILE_FORMAT, DEFAULT_PAGE_NUMBER, TRANSFORMATION_RESIZE,
    TRANSFORMATION_ROTATE, TRANSFORMATION_ZOOM
)
from ..settings import PDFTOPPM_PATH

try:
    pdftoppm = sh.Command(PDFTOPPM_PATH)
except sh.CommandNotFound:
    pdftoppm = None
else:
    pdftoppm = pdftoppm.bake('-png')

Image.init()
logger = logging.getLogger(__name__)


class Python(ConverterBase):
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
            while True:
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

        try:
            if mimetype == 'application/pdf' and pdftoppm:
                image_buffer = io.BytesIO()
                pdftoppm(input_filepath, f=page, l=page, _out=image_buffer)
                image_buffer.seek(0)
                im = Image.open(image_buffer)
            else:
                im = Image.open(input_filepath)
        except Exception as exception:
            logger.error('Error converting image; %s', exception)
            # Python Imaging Library doesn't recognize it as an image
            raise ConvertError
        except IOError:  # cannot identify image file
            raise UnknownFileFormat
        finally:
            if tmpfile:
                fs_cleanup(tmpfile)

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

    def get_available_transformations(self):
        return [
            TRANSFORMATION_RESIZE, TRANSFORMATION_ROTATE,
            TRANSFORMATION_ZOOM
        ]

    # From: http://united-coders.com/christian-harms/image-resizing-tips-general-and-for-python
    def resize(self, img, box, fit=False, out=None):
        """
        Downsample the image.
        @param img: Image -  an Image-object
        @param box: tuple(x, y) - the bounding box of the result image
        @param fit: boolean - crop the image to fill the box
        @param out: file-like-object - save the image into the output stream
        """
        # preresize image with factor 2, 4, 8 and fast algorithm
        factor = 1
        while img.size[0] / factor > 2 * box[0] and img.size[1] * 2 / factor > 2 * box[1]:
            factor *= 2
        if factor > 1:
            img.thumbnail((img.size[0] / factor, img.size[1] / factor), Image.NEAREST)

        # calculate the cropping box and get the cropped part
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

        # Resize the image with best quality algorithm ANTI-ALIAS
        img.thumbnail(box, Image.ANTIALIAS)

        if out:
            # save it into a file-like object
            img.save(out, 'JPEG', quality=75)
        else:
            return img

        # if isinstance(self.regex, basestring):
        #    self.regex = re.compile(regex)
