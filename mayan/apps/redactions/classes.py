'''
from __future__ import unicode_literals

import logging

from PIL import Image

from converter import converter_class

logger = logging.getLogger(__name__)


class OCRBackendBase(object):
    def execute(self, file_object, language=None, process_barcodes=True, process_text=True, transformations=None):
        self.language = language
        self.process_barcodes = process_barcodes
        self.process_text = process_text

        if not transformations:
            transformations = []

        self.converter = converter_class(file_object=file_object)

        for transformation in transformations:
            self.converter.transform(transformation=transformation)

        self.image = Image.open(self.converter.get_page())
'''
