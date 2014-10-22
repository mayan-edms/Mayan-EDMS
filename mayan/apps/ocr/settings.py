"""Configuration options for the ocr app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'ocr',
    module=u'ocr.settings',
    settings=[
        {'name': u'TESSERACT_PATH', 'global_name': u'OCR_TESSERACT_PATH', 'default': u'/usr/bin/tesseract', 'exists': True},
        {'name': u'UNPAPER_PATH', 'global_name': u'OCR_UNPAPER_PATH', 'default': u'/usr/bin/unpaper', 'description': _(u'File path to unpaper program.'), 'exists': True},
        {'name': u'PDFTOTEXT_PATH', 'global_name': u'OCR_PDFTOTEXT_PATH', 'default': u'/usr/bin/pdftotext', 'description': _(u'File path to poppler\'s pdftotext program used to extract text from PDF files.'), 'exists': True},
        {'name': u'BACKEND', 'global_name': u'OCR_BACKEND', 'default': u'ocr.backends.tesseract.Tesseract', 'description': _(u'Full path to the backend to be used to do OCR.')},
    ]
)
