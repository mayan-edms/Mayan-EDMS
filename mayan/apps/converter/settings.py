from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='converter', label=_('Converter'))
setting_graphics_backend = namespace.add_setting(
    default='converter.backends.python.Python',
    help_text=_('Graphics conversion backend to use.'),
    global_name='CONVERTER_GRAPHICS_BACKEND',
)
setting_graphics_backend_config = namespace.add_setting(
    default='{libreoffice_path: /usr/bin/libreoffice, '
    'pdftoppm_path: /usr/bin/pdftoppm, pdfinfo_path: /usr/bin/pdfinfo}',
    help_text=_(
        'Configuration options for the graphics conversion backend.'
    ), global_name='CONVERTER_GRAPHICS_BACKEND_CONFIG',
)
