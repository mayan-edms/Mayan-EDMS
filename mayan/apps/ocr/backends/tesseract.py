from __future__ import unicode_literals

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import codecs
import errno
import logging
import os
import tempfile

from PIL import Image, ImageFilter
import pytesseract

from common.utils import fs_cleanup

from ..classes import OCRBackendBase
from ..exceptions import OCRError
from ..settings import setting_tesseract_path

logger = logging.getLogger(__name__)


class Tesseract(OCRBackendBase):
    def execute(self, *args, **kwargs):
        """
        Execute the command line binary of tesseract
        """
        super(Tesseract, self).execute(*args, **kwargs)

        image = Image.open(self.converter.get_page())
        try:
            result = pytesseract.image_to_string(image=image, lang=self.language)
            # If tesseract gives an error with a language parameter
            # re-run it with no language parameter
        except:
            result = pytesseract.image_to_string(image=image)

        return result
