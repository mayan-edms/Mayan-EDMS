***********
OCR backend
***********

Mayan EDMS ships an OCR backend that uses the FLOSS engine Tesseract
(https://github.com/tesseract-ocr/tesseract/), but it can
use other engines. To support other engines create a wrapper that subclasses the
``OCRBackendBase`` class defined in mayan/apps/ocr/classes. This subclass should
expose the ``execute`` method. For an example of how the Tesseract backend
is implemented take a look at the file ``mayan/apps/ocr/backends/tesseract.py``

Once you create you own backend, in your local.py settings add the option
OCR_BACKEND and point it to your new OCR backend class path.

The default value of OCR_BACKEND is ``"ocr.backends.tesseract.Tesseract"``

To add support to OCR more languages when using Tesseract, install the
corresponding language file. If using a Debian based OS, this command will
display the available language files:

    apt-cache search tesseract-ocr

If using the Docker image, pass the environment variable MAYAN_APT_INSTALLS
with the corresponding Tesseract language option. Example::

    -e MAYAN_APT_INSTALLS='tesseract-ocr-deu'
