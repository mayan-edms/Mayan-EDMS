from __future__ import unicode_literals

import io
import logging
import os
import tempfile

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from PIL import Image
from pdfminer.pdfpage import PDFPage
import sh

from django.utils.translation import ugettext_lazy as _

from common.utils import fs_cleanup

from ..classes import ConverterBase
from ..exceptions import PageCountError
from ..settings import setting_pdftoppm_path

try:
    pdftoppm = sh.Command(setting_pdftoppm_path.value)
except sh.CommandNotFound:
    pdftoppm = None
else:
    pdftoppm = pdftoppm.bake('-jpeg')

Image.init()
logger = logging.getLogger(__name__)


class IteratorIO(object):
    def __init__(self, iterator):
        self.file_buffer = StringIO()

        for chunk in iterator:
            self.file_buffer.write(chunk)

        self.file_buffer.seek(0)


class Python(ConverterBase):

    def convert(self, *args, **kwargs):
        super(Python, self).convert(*args, **kwargs)

        if self.mime_type == 'application/pdf' and pdftoppm:

            new_file_object, input_filepath = tempfile.mkstemp()
            self.file_object.seek(0)
            os.write(new_file_object, self.file_object.read())
            self.file_object.seek(0)

            os.close(new_file_object)

            image_buffer = io.BytesIO()
            try:
                pdftoppm(
                    input_filepath, f=self.page_number + 1,
                    l=self.page_number + 1, _out=image_buffer
                )
                image_buffer.seek(0)
                return Image.open(image_buffer)
            finally:
                fs_cleanup(input_filepath)

    def get_page_count(self):
        super(Python, self).get_page_count()

        page_count = 1

        if self.mime_type == 'application/pdf' or self.soffice_file:
            # If file is a PDF open it with slate to determine the page count
            if self.soffice_file:
                file_object = IteratorIO(self.soffice_file).file_buffer
            else:
                file_object = self.file_object

            try:
                page_count = len(list(PDFPage.get_pages(file_object)))
            except Exception as exception:
                error_message = _(
                    'Exception determining PDF page count; %s'
                ) % exception
                logger.error(error_message)
                raise PageCountError(error_message)
            else:
                logger.debug('Document contains %d pages', page_count)
                return page_count
            finally:
                file_object.seek(0)
        else:
            try:
                image = Image.open(self.file_object)
            except IOError as exception:
                error_message = _(
                    'Exception determining PDF page count; %s'
                ) % exception
                logger.error(error_message)
                raise PageCountError(error_message)
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
