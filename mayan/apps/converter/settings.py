from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

from .literals import (
    DEFAULT_LIBREOFFICE_PATH, DEFAULT_PDFTOPPM_DPI, DEFAULT_PDFTOPPM_FORMAT,
    DEFAULT_PDFTOPPM_PATH, DEFAULT_PDFINFO_PATH, DEFAULT_PILLOW_FORMAT,
    DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS
)
from .setting_migrations import ConvertSettingMigration

namespace = Namespace(
    label=_('Converter'), migration_class=ConvertSettingMigration,
    name='converter', version='0002'
)

setting_graphics_backend = namespace.add_setting(
    default='mayan.apps.converter.backends.python.Python',
    help_text=_('Graphics conversion backend to use.'),
    global_name='CONVERTER_GRAPHICS_BACKEND',
)
setting_graphics_backend_arguments = namespace.add_setting(
    default={
        'libreoffice_path': DEFAULT_LIBREOFFICE_PATH,
        'pdftoppm_dpi': DEFAULT_PDFTOPPM_DPI,
        'pdftoppm_format': DEFAULT_PDFTOPPM_FORMAT,
        'pdftoppm_path': DEFAULT_PDFTOPPM_PATH,
        'pdfinfo_path': DEFAULT_PDFINFO_PATH,
        'pillow_format': DEFAULT_PILLOW_FORMAT,
        'pillow_maximum_image_pixels': DEFAULT_PILLOW_MAXIMUM_IMAGE_PIXELS,
    }, help_text=_(
        'Configuration options for the graphics conversion backend.'
    ), global_name='CONVERTER_GRAPHICS_BACKEND_ARGUMENTS'
)
