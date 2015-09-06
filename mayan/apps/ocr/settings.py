from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='ocr', label=_('OCR'))
setting_tesseract_path = namespace.add_setting(
    global_name='OCR_TESSERACT_PATH', default='/usr/bin/tesseract',
    help_text=_('File path to tesseract program.'), is_path=True
)
setting_pdftotext_path = namespace.add_setting(
    global_name='OCR_PDFTOTEXT_PATH', default='/usr/bin/pdftotext',
    help_text=_(
        'File path to poppler\'s pdftotext program used to extract text '
        'from PDF files.'
    ),
    is_path=True
)
setting_ocr_backend = namespace.add_setting(
    global_name='OCR_BACKEND', default='ocr.backends.tesseract.Tesseract',
    help_text=_('Full path to the backend to be used to do OCR.')
)
setting_auto_ocr = namespace.add_setting(
    global_name='OCR_AUTO_OCR', default=True,
    help_text=_(
        'Set new document types to perform OCR automatically by default.'
    )
)
