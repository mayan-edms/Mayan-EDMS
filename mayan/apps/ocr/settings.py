from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace='ocr',
    module='ocr.settings',
    settings=[
        {'name': 'TESSERACT_PATH', 'global_name': 'OCR_TESSERACT_PATH', 'default': '/usr/bin/tesseract', 'exists': True},
        {'name': 'UNPAPER_PATH', 'global_name': 'OCR_UNPAPER_PATH', 'default': '/usr/bin/unpaper', 'description': _('File path to unpaper program.'), 'exists': True},
        {'name': 'PDFTOTEXT_PATH', 'global_name': 'OCR_PDFTOTEXT_PATH', 'default': '/usr/bin/pdftotext', 'description': _('File path to poppler\'s pdftotext program used to extract text from PDF files.'), 'exists': True},
        {'name': 'BACKEND', 'global_name': 'OCR_BACKEND', 'default': 'ocr.backends.tesseract.Tesseract', 'description': _('Full path to the backend to be used to do OCR.')},
    ]
)
