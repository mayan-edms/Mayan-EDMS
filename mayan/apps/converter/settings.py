from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND,
    DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND_ARGUMENTS,
    DEFAULT_CONVERTER_GRAPHICS_BACKEND,
    DEFAULT_CONVERTER_GRAPHICS_BACKEND_ARGUMENTS
)
from .setting_migrations import ConvertSettingMigration

namespace = SettingNamespace(
    label=_('Converter'), migration_class=ConvertSettingMigration,
    name='converter', version='0002'
)

setting_graphics_backend = namespace.add_setting(
    default=DEFAULT_CONVERTER_GRAPHICS_BACKEND,
    global_name='CONVERTER_GRAPHICS_BACKEND', help_text=_(
        'Graphics conversion backend to use.'
    )
)
setting_graphics_backend_arguments = namespace.add_setting(
    default=DEFAULT_CONVERTER_GRAPHICS_BACKEND_ARGUMENTS,
    global_name='CONVERTER_GRAPHICS_BACKEND_ARGUMENTS', help_text=_(
        'Configuration options for the graphics conversion backend.'
    )
)
setting_storage_backend = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND,
    global_name='CONVERTER_ASSET_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing assets.'
    )
)
setting_storage_backend_arguments = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND_ARGUMENTS,
    global_name='CONVERTER_ASSET_STORAGE_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to pass to the CONVERTER_ASSET_STORAGE_BACKEND.'
    )
)
