from django.conf import settings


TESSERACT_PATH = getattr(settings, 'OCR_TESSERACT_PATH', u'/usr/bin/tesseract')
TESSERACT_LANGUAGE = getattr(settings, 'OCR_TESSERACT_LANGUAGE', u'eng')
REPLICATION_DELAY = getattr(settings, 'OCR_REPLICATION_DELAY', 10)  # In seconds
NODE_CONCURRENT_EXECUTION = getattr(settings, 'OCR_NODE_CONCURRENT_EXECUTION', 1)
AUTOMATIC_OCR = getattr(settings, 'OCR_AUTOMATIC_OCR', False)
PDFTOTEXT_PATH = getattr(settings, 'OCR_PDFTOTEXT_PATH', u'/usr/bin/pdftotext')
QUEUE_PROCESSING_INTERVAL = getattr(settings, 'OCR_QUEUE_PROCESSING_INTERVAL', 10)  # In seconds
