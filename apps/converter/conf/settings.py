from django.conf import settings

CONVERT_PATH = getattr(settings, 'CONVERTER_CONVERT_PATH', u'/usr/bin/convert')
OCR_OPTIONS = getattr(settings, 'CONVERTER_OCR_OPTIONS', u'-colorspace Gray -depth 8 -resample 200x200')
DEFAULT_OPTIONS = getattr(settings, 'CONVERTER_DEFAULT_OPTIONS', u'')
LOW_QUALITY_OPTIONS = getattr(settings, 'CONVERTER_LOW_QUALITY_OPTIONS', u'')
HIGH_QUALITY_OPTIONS = getattr(settings, 'CONVERTER_HIGH_QUALITY_OPTIONS', u'-density 400')
