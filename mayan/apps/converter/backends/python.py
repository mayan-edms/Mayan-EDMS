from __future__ import unicode_literals

import io
import logging
import os
import tempfile

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import slate
from PIL import Image
import sh

from common.utils import fs_cleanup

from ..classes import ConverterBase
from ..settings import setting_pdftoppm_path

try:
    pdftoppm = sh.Command(setting_pdftoppm_path.value)
except sh.CommandNotFound:
    pdftoppm = None
else:
    pdftoppm = pdftoppm.bake('-png')

Image.init()
logger = logging.getLogger(__name__)


class Python(ConverterBase):

    def convert(self, *args, **kwargs):
        super(Python, self).convert(*args, **kwargs)

        if self.mime_type == 'application/pdf' and pdftoppm:

            new_file_object, input_filepath = tempfile.mkstemp()

            if self.soffice_file_object:
                os.write(new_file_object, self.soffice_file_object.read())
                self.soffice_file_object.close()
            else:
                os.write(new_file_object, self.file_object.read())
                self.file_object.seek(0)

            os.close(new_file_object)

            image_buffer = io.BytesIO()
            try:
                pdftoppm(input_filepath, f=self.page_number + 1, l=self.page_number + 1, _out=image_buffer)
                image_buffer.seek(0)
                return Image.open(image_buffer)
            finally:
                fs_cleanup(input_filepath)

    def get_page_count(self):
        page_count = 1

        if self.mime_type == 'application/pdf':
            # If file is a PDF open it with slate to determine the page count
            try:
                pages = slate.PDF(self.file_object)
            except Exception as exception:
                logger.error('slate exception; %s', exception)
                return 1
                # TODO: Maybe return UnknownFileFormat to display proper unknwon file format message in document description
            else:
                return len(pages)
            finally:
                self.file_object.seek(0)

        try:
            image = Image.open(self.file_object)
        finally:
            self.file_object.seek(0)

        try:
            while True:
                image.seek(image.tell() + 1)
                page_count += 1
        except EOFError:
            # end of sequence
            pass

        return page_count
