from django.conf import settings

TESSERACT_PATH = getattr(settings, 'OCR_TESSERACT_PATH', u'/usr/bin/tesseract')
