from __future__ import unicode_literals

import logging

import sh

from PIL import Image
import pytesseract

from ..classes import OCRBackendBase
from ..exceptions import OCRError
from ..settings import setting_tesseract_path

logger = logging.getLogger(__name__)


class Tesseract(OCRBackendBase):
    def __init__(self, *args, **kwargs):
        super(Tesseract, self).__init__(*args, **kwargs)
        try:
            self.binary = sh.Command(setting_tesseract_path.value)
        except sh.CommandNotFound:
            self.binary = None

    def get_languages(self):
        if self.binary:
            result = self.binary(list_langs=True)

            return [
                language for language in result.stderr.split('\n') if language
            ]
        else:
            return ()

    def execute(self, *args, **kwargs):
        """
        Execute the command line binary of tesseract
        """
        super(Tesseract, self).execute(*args, **kwargs)

        # TODO: pass tesseract binary path to the pytesseract
        image = Image.open(self.converter.get_page())
        try:
            result = pytesseract.image_to_string(
                image=image, lang=self.language
            )
            # If tesseract gives an error with a language parameter
            # re-run it with no language parameter
        except Exception as exception:
            error_message = 'Exception calling pytesseract with language option: {}; {}'.format(self.language, exception)

            if self.binary:
                if self.language not in self.get_languages():
                    error_message = '{}\nThe requested Tesseract language file for "{}" is not available and needs to be installed.\nIf using Debian or Ubuntu run: apt-get install tesseract-ocr-{}'.format(error_message, self.language, self.language)

            logger.error(error_message)
            raise OCRError(error_message)

        return result
