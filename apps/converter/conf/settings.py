from django.conf import settings
from django.utils.translation import ugettext_lazy as _


IM_CONVERT_PATH = getattr(settings, 'CONVERTER_IM_ONVERT_PATH', u'/usr/bin/convert')
IM_IDENTIFY_PATH = getattr(settings, 'CONVERTER_IM_IDENTIFY_PATH', u'/usr/bin/identify')
UNPAPER_PATH = getattr(settings, 'CONVERTER_UNPAPER_PATH', u'/usr/bin/unpaper')
GM_PATH = getattr(settings, 'CONVERTER_GM_PATH', u'/usr/bin/gm')
GRAPHICS_BACKEND = getattr(settings, 'CONVERTER_GRAPHICS_BACKEND', u'converter.backends.imagemagick')

OCR_OPTIONS = getattr(settings, 'CONVERTER_OCR_OPTIONS', u'-colorspace Gray -depth 8 -resample 200x200')
DEFAULT_OPTIONS = getattr(settings, 'CONVERTER_DEFAULT_OPTIONS', u'')
LOW_QUALITY_OPTIONS = getattr(settings, 'CONVERTER_LOW_QUALITY_OPTIONS', u'')
HIGH_QUALITY_OPTIONS = getattr(settings, 'CONVERTER_HIGH_QUALITY_OPTIONS', u'-density 400')


setting_description = {
    'CONVERTER_IM_CONVERT_PATH': _(u'File path to imagemagick\'s convert program.'),
    'CONVERTER_IM_IDENTIFY_PATH': _(u'File path to imagemagick\'s identify program.'),
    'CONVERTER_GM_PATH': _(u'File path to graphicsmagick\'s program.'),
    'CONVERTER_UNPAPER_PATH': _(u'File path to unpaper program.'),
    'CONVERTER_GRAPHICS_BACKEND': _(u'Graphics conversion backend to use.  Options are: converter.backends.imagemagick and converter.backends.graphicsmagick.'),
}
