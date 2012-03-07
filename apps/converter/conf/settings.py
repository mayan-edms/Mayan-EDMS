"""Configuration options for the converter app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('converter', _(u'Converter'), module='converter.conf.settings')

Setting(
    namespace=namespace,
    name='IM_CONVERT_PATH',
    global_name='CONVERTER_IM_CONVERT_PATH',
    default=u'/usr/bin/convert',
    description=_(u'File path to imagemagick\'s convert program.'),
    exists=True,
)

Setting(
    namespace=namespace,
    name='IM_CONVERT_PATH',
    global_name='CONVERTER_IM_CONVERT_PATH',
    default=u'/usr/bin/convert',
    description=_(u'File path to imagemagick\'s convert program.'),
    exists=True,
)

Setting(
    namespace=namespace,
    name='IM_IDENTIFY_PATH',
    global_name='CONVERTER_IM_IDENTIFY_PATH',
    default=u'/usr/bin/identify',
    description=_(u'File path to imagemagick\'s identify program.'),
    exists=True,
)

Setting(
    namespace=namespace,
    name='GM_PATH',
    global_name='CONVERTER_GM_PATH',
    default=u'/usr/bin/gm',
    description=_(u'File path to graphicsmagick\'s program.'),
    exists=True,
)

Setting(
    namespace=namespace,
    name='GM_SETTINGS',
    global_name='CONVERTER_GM_SETTINGS',
    default=u'',
    description=_(u'Set of configuration options to pass to the GraphicsMagick executable to fine tune it\'s functionality as explained in the GraphicsMagick documentation.'),
)

Setting(
    namespace=namespace,
    name='GRAPHICS_BACKEND',
    global_name='CONVERTER_GRAPHICS_BACKEND',
    default=u'converter.backends.python',
    description=_(u'Graphics conversion backend to use.  Options are: converter.backends.imagemagick, converter.backends.graphicsmagick and converter.backends.python.'),
)

Setting(
    namespace=namespace,
    name='UNOCONV_PATH',
    global_name='CONVERTER_UNOCONV_PATH',
    default=u'/usr/bin/unoconv',
    description=_(u'Path to the unoconv program.'),
    exists=True
)

Setting(
    namespace=namespace,
    name='UNOCONV_USE_PIPE',
    global_name='CONVERTER_UNOCONV_USE_PIPE',
    default=True,
    description=_(u'Use alternate method of connection to LibreOffice using a pipe, it is slower but less prone to segmentation faults.'),
)

#{'name': u'OCR_OPTIONS', 'global_name': u'CONVERTER_OCR_OPTIONS', 'default': u'-colorspace Gray -depth 8 -resample 200x200'},
#{'name': u'HIGH_QUALITY_OPTIONS', 'global_name': u'CONVERTER_HIGH_QUALITY_OPTIONS', 'default': u'-density 400'},
#{'name': u'PRINT_QUALITY_OPTIONS', 'global_name': u'CONVERTER_PRINT_QUALITY_OPTIONS', 'default': u'-density 500'},
