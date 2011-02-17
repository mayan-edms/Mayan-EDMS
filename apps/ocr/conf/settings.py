from django.conf import settings

TESSERACT_PATH = getattr(settings, 'OCR_TESSERACT_PATH', u'/usr/bin/tesseract')
MAX_CONCURRENT_EXECUTION = getattr(settings, 'OCR_MAX_CONCURRENT_EXECUTION', 2)
