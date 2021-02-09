DEFAULT_OCR_AUTO_OCR = True
DEFAULT_OCR_BACKEND = 'mayan.apps.ocr.backends.tesseract.Tesseract'
DEFAULT_OCR_BACKEND_ARGUMENTS = {'environment': {'OMP_THREAD_LIMIT': '1'}}

DO_OCR_RETRY_DELAY = 10
