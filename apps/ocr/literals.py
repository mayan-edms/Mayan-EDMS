from django.utils.translation import ugettext_lazy as _


OCR_STATE_DISABLED = 'd'
OCR_STATE_ENABLED = 'e'

OCR_STATE_CHOICES = (
    (OCR_STATE_DISABLED, _(u'disabled')),
    (OCR_STATE_ENABLED, _(u'enabled')),
)

DEFAULT_OCR_FILE_FORMAT = u'tiff'
DEFAULT_OCR_FILE_EXTENSION = u'tif'
UNPAPER_FILE_FORMAT = u'ppm'

OCR_QUEUE_NAME = 'ocr'
