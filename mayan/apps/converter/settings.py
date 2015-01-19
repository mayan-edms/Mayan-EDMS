from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace='converter',
    module='converter.settings',
    settings=[
        {'name': 'IM_CONVERT_PATH', 'global_name': 'CONVERTER_IM_CONVERT_PATH', 'default': '/usr/bin/convert', 'description': _('File path to imagemagick\'s convert program.'), 'exists': True},
        {'name': 'IM_IDENTIFY_PATH', 'global_name': 'CONVERTER_IM_IDENTIFY_PATH', 'default': '/usr/bin/identify', 'description': _('File path to imagemagick\'s identify program.'), 'exists': True},
        {'name': 'GM_PATH', 'global_name': 'CONVERTER_GM_PATH', 'default': '/usr/bin/gm', 'description': _('File path to graphicsmagick\'s program.'), 'exists': True},
        {'name': 'GM_SETTINGS', 'global_name': 'CONVERTER_GM_SETTINGS', 'default': ''},
        {'name': 'GRAPHICS_BACKEND', 'global_name': 'CONVERTER_GRAPHICS_BACKEND', 'default': 'converter.backends.python.Python', 'description': _('Graphics conversion backend to use.  Options are: converter.backends.imagemagick.ImageMagick, converter.backends.graphicsmagick.GraphicsMagick and converter.backends.python.Python')},
        {'name': 'LIBREOFFICE_PATH', 'global_name': 'CONVERTER_LIBREOFFICE_PATH', 'default': '/usr/bin/libreoffice', 'exists': True, 'description': _('Path to the libreoffice program.')},
        {'name': 'PDFTOPPM_PATH', 'global_name': 'CONVERTER_PDFTOPPM_PATH', 'default': '/usr/bin/pdftoppm', 'exists': True, 'description': _('Path to the Popple program pdftoppm.')},
    ]
)
