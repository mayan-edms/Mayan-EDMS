===========
OCR backend
===========

Mayan EDMS ships an OCR backend that uses the FLOSS engine Tesseract, but it can
use other engines. To support other engines a wrapper that subclasess the
``OCRBackendBase`` class defined in mayan/apps/ocr/classes. This subclass should
expose the ``execute`` method. For an example of how the Tesseract backend
is implemented take a look at the file ``mayan/apps/ocr/backends/tesseract.py``

Once you create you own backend, in your local.py settings add the option
OCR_BACKEND and point it to your new OCR backend class path.

The default value of OCR_BACKEND is ``"ocr.backends.tesseract.Tesseract"``

