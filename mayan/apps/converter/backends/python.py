import io
import logging
import shutil
import struct

from PIL import Image
import PyPDF2
import sh

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.utils import NamedTemporaryFile

from ..classes import ConverterBase
from ..exceptions import PageCountError
from ..settings import setting_graphics_backend_arguments

from ..literals import (
    DEFAULT_PDFTOPPM_DPI, DEFAULT_PDFTOPPM_FORMAT, DEFAULT_PDFTOPPM_PATH,
    DEFAULT_PDFINFO_PATH, DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS
)

logger = logging.getLogger(name=__name__)
pdftoppm_path = setting_graphics_backend_arguments.value.get(
    'pdftoppm_path', DEFAULT_PDFTOPPM_PATH
)

try:
    pdftoppm = sh.Command(path=pdftoppm_path)
except sh.CommandNotFound:
    pdftoppm = None
else:
    pdftoppm_format = '-{}'.format(
        setting_graphics_backend_arguments.value.get(
            'pdftoppm_format', DEFAULT_PDFTOPPM_FORMAT
        )
    )

    pdftoppm_dpi = format(
        setting_graphics_backend_arguments.value.get(
            'pdftoppm_dpi', DEFAULT_PDFTOPPM_DPI
        )
    )

    pdftoppm = pdftoppm.bake(pdftoppm_format, '-r', pdftoppm_dpi)

pdfinfo_path = setting_graphics_backend_arguments.value.get(
    'pdfinfo_path', DEFAULT_PDFINFO_PATH
)

try:
    pdfinfo = sh.Command(path=pdfinfo_path)
except sh.CommandNotFound:
    pdfinfo = None


pillow_maximum_image_pixels = setting_graphics_backend_arguments.value.get(
    'pillow_maximum_image_pixels', DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS
)
Image.MAX_IMAGE_PIXELS = pillow_maximum_image_pixels


class Python(ConverterBase):
    def convert(self, *args, **kwargs):
        super().convert(*args, **kwargs)

        if self.mime_type == 'application/pdf' and pdftoppm:
            new_file_object = NamedTemporaryFile()
            input_filepath = new_file_object.name
            self.file_object.seek(0)
            shutil.copyfileobj(fsrc=self.file_object, fdst=new_file_object)
            self.file_object.seek(0)
            new_file_object.seek(0)

            image_buffer = io.BytesIO()
            try:
                pdftoppm(
                    input_filepath, f=self.page_number + 1,
                    l=self.page_number + 1, _out=image_buffer
                )
                image_buffer.seek(0)
                return Image.open(fp=image_buffer)
            finally:
                new_file_object.close()

    def get_page_count(self):
        super().get_page_count()

        page_count = 1

        if self.mime_type == 'application/pdf' or self.soffice_file:
            if self.soffice_file:
                file_object = self.soffice_file
            else:
                file_object = self.file_object

            try:
                # Try PyPDF to determine the page number
                pdf_reader = PyPDF2.PdfFileReader(
                    stream=file_object, strict=False
                )
                page_count = pdf_reader.getNumPages()
            except Exception as exception:
                if force_text(s=exception) == 'File has not been decrypted':
                    # File is encrypted, try to decrypt using a blank
                    # password.
                    file_object.seek(0)
                    pdf_reader = PyPDF2.PdfFileReader(
                        stream=file_object, strict=False
                    )
                    try:
                        pdf_reader.decrypt(password=b'')
                        page_count = pdf_reader.getNumPages()
                    except Exception as exception:
                        file_object.seek(0)
                        if force_text(s=exception) == 'only algorithm code 1 and 2 are supported':
                            # PDF uses an unsupported encryption
                            # Try poppler-util's pdfinfo
                            page_count = self.get_pdfinfo_page_count(file_object)
                            return page_count
                        else:
                            error_message = _(
                                'Exception determining PDF page count; %s'
                            ) % exception
                            logger.error(error_message, exc_info=True)
                            raise PageCountError(error_message)
                elif force_text(s=exception) == 'EOF marker not found':
                    # PyPDF2 issue: https://github.com/mstamy2/PyPDF2/issues/177
                    # Try poppler-util's pdfinfo
                    logger.debug('PyPDF2 GitHub issue #177 : EOF marker not found')
                    file_object.seek(0)
                    page_count = self.get_pdfinfo_page_count(file_object)
                    return page_count
                else:
                    error_message = _(
                        'Exception determining PDF page count; %s'
                    ) % exception
                    logger.error(error_message, exc_info=True)
                    raise PageCountError(error_message)
            else:
                logger.debug('Document contains %d pages', page_count)
                return page_count
            finally:
                file_object.seek(0)
        else:
            try:
                image = Image.open(fp=self.file_object)
            except IOError as exception:
                error_message = _(
                    'Exception determining page count using Pillow; %s'
                ) % exception
                logger.error(error_message)
                raise PageCountError(error_message)
            finally:
                self.file_object.seek(0)

            # Get total page count by attempting to seek to an increasing
            # page count number until an EOFError or struct.error exception
            # are raised.
            try:
                while True:
                    image.seek(image.tell() + 1)
                    page_count += 1
            except EOFError:
                """End of sequence"""
            except struct.error:
                """
                struct.error was raise for a TIFF file converted to JPEG
                GitLab issue #767 "Upload Error: unpack_from requires a
                buffer of at least 2 bytes"
                """
                logger.debug('image page count detection raised struct.error')

            return page_count

    def get_pdfinfo_page_count(self, file_object):
        process = pdfinfo('-', _in=file_object)
        page_count = int(
            list(filter(
                lambda line: line.startswith('Pages:'),
                force_text(s=process.stdout).split('\n')
            ))[0].replace('Pages:', '')
        )
        file_object.seek(0)
        logger.debug(
            'Document contains %d pages', page_count
        )
        return page_count
