from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='converter', label=_('Converter'))
setting_graphics_backend = namespace.add_setting(global_name='CONVERTER_GRAPHICS_BACKEND', default='converter.backends.python.Python', help_text=_('Graphics conversion backend to use.'))
setting_libreoffice_path = namespace.add_setting(global_name='CONVERTER_LIBREOFFICE_PATH', default='/usr/bin/libreoffice', help_text=_('Path to the libreoffice program.'), is_path=True)
setting_pdftoppm_path = namespace.add_setting(global_name='CONVERTER_PDFTOPPM_PATH', default='/usr/bin/pdftoppm', help_text=_('Path to the Popple program pdftoppm.'), is_path=True)

# TODO: remove unconverted backends from repository
#register_settings(
#    namespace='converter',
#    module='converter.settings',
#    settings=[
#        {'name': 'IM_CONVERT_PATH', 'global_name': 'CONVERTER_IM_CONVERT_PATH', 'default': '/usr/bin/convert', 'description': _('File path to imagemagick\'s convert program.'), 'exists': True},
#        {'name': 'IM_IDENTIFY_PATH', 'global_name': 'CONVERTER_IM_IDENTIFY_PATH', 'default': '/usr/bin/identify', 'description': _('File path to imagemagick\'s identify program.'), 'exists': True},
#        {'name': 'GM_PATH', 'global_name': 'CONVERTER_GM_PATH', 'default': '/usr/bin/gm', 'description': _('File path to graphicsmagick\'s program.'), 'exists': True},
#        {'name': 'GM_SETTINGS', 'global_name': 'CONVERTER_GM_SETTINGS', 'default': ''},
#    ]
#)
