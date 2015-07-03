from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='converter', label=_('Converter'))
setting_graphics_backend = namespace.add_setting(global_name='CONVERTER_GRAPHICS_BACKEND', default='converter.backends.python.Python', help_text=_('Graphics conversion backend to use.'))
setting_libreoffice_path = namespace.add_setting(global_name='CONVERTER_LIBREOFFICE_PATH', default='/usr/bin/libreoffice', help_text=_('Path to the libreoffice program.'), is_path=True)
setting_pdftoppm_path = namespace.add_setting(global_name='CONVERTER_PDFTOPPM_PATH', default='/usr/bin/pdftoppm', help_text=_('Path to the Popple program pdftoppm.'), is_path=True)
