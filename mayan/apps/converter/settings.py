from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='converter', label=_('Converter'))
setting_graphics_backend = namespace.add_setting(
    default='converter.backends.python.Python',
    help_text=_('Graphics conversion backend to use.'),
    global_name='CONVERTER_GRAPHICS_BACKEND',
)
setting_libreoffice_path = namespace.add_setting(
    default='/usr/bin/libreoffice',
    global_name='CONVERTER_LIBREOFFICE_PATH',
    help_text=_('Path to the libreoffice program.'), is_path=True
)
setting_pdftoppm_path = namespace.add_setting(
    default='/usr/bin/pdftoppm', global_name='CONVERTER_PDFTOPPM_PATH',
    help_text=_('Path to the Popple program pdftoppm.'), is_path=True
)
