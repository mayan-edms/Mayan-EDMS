"""Configuration options for the converter app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'converter',
    module=u'converter.settings',
    settings=[
        {'name': u'IM_CONVERT_PATH', 'global_name': u'CONVERTER_IM_CONVERT_PATH', 'default': u'/usr/bin/convert', 'description': _(u'File path to imagemagick\'s convert program.'), 'exists': True},
        {'name': u'IM_IDENTIFY_PATH', 'global_name': u'CONVERTER_IM_IDENTIFY_PATH', 'default': u'/usr/bin/identify', 'description': _(u'File path to imagemagick\'s identify program.'), 'exists': True},
        {'name': u'GM_PATH', 'global_name': u'CONVERTER_GM_PATH', 'default': u'/usr/bin/gm', 'description': _(u'File path to graphicsmagick\'s program.'), 'exists': True},
        {'name': u'GM_SETTINGS', 'global_name': u'CONVERTER_GM_SETTINGS', 'default': u''},
        {'name': u'GRAPHICS_BACKEND', 'global_name': u'CONVERTER_GRAPHICS_BACKEND', 'default': u'converter.backends.python.Python', 'description': _(u'Graphics conversion backend to use.  Options are: converter.backends.imagemagick.ImageMagick, converter.backends.graphicsmagick.GraphicsMagick and converter.backends.python.Python')},
        {'name': u'LIBREOFFICE_PATH', 'global_name': u'CONVERTER_LIBREOFFICE_PATH', 'default': u'/usr/bin/libreoffice', 'exists': True, 'description': _(u'Path to the libreoffice program.')},
        {'name': u'PDFTOPPM_PATH', 'global_name': u'CONVERTER_PDFTOPPM_PATH', 'default': u'/usr/bin/pdftoppm', 'exists': True, 'description': _(u'Path to the Popple program pdftoppm.')},
    ]
)
