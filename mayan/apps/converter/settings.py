from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_CONVERTER_ASSET_CACHE_MAXIMUM_SIZE,
    DEFAULT_CONVERTER_ASSET_CACHE_TIME,
    DEFAULT_CONVERTER_ASSET_CACHE_STORAGE_BACKEND,
    DEFAULT_CONVERTER_ASSET_CACHE_STORAGE_BACKEND_ARGUMENTS,
    DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND,
    DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND_ARGUMENTS,
    DEFAULT_CONVERTER_GRAPHICS_BACKEND,
    DEFAULT_CONVERTER_GRAPHICS_BACKEND_ARGUMENTS
)
from .setting_callbacks import callback_update_asset_cache_size
from .setting_migrations import ConvertSettingMigration

namespace = SettingNamespace(
    label=_('Converter'), migration_class=ConvertSettingMigration,
    name='converter', version='0002'
)


setting_asset_cache_maximum_size = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_CACHE_MAXIMUM_SIZE,
    global_name='CONVERTER_ASSET_CACHE_MAXIMUM_SIZE',
    help_text=_(
        'The threshold at which the CONVERTER_ASSET_CACHE_STORAGE_BACKEND '
        'will start deleting the oldest asset cache files. '
        'Specify the size in bytes.'
    ), post_edit_function=callback_update_asset_cache_size
)
setting_asset_cache_time = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_CACHE_TIME,
    global_name='CONVERTER_ASSET_CACHE_TIME',
    help_text=_(
        'Time in seconds that the browser should cache the supplied asset. '
        'The default of 31559626 seconds correspond to 1 year.'
    )
)
setting_asset_cache_storage_backend = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_CACHE_STORAGE_BACKEND,
    global_name='CONVERTER_ASSET_CACHE_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'asset files.'
    )
)
setting_asset_cache_storage_backend_arguments = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_CACHE_STORAGE_BACKEND_ARGUMENTS,
    global_name='CONVERTER_ASSET_CACHE_STORAGE_BACKEND_ARGUMENTS',
    help_text=_(
        'Arguments to pass to the CONVERTER_ASSET_CACHE_STORAGE_BACKEND.'
    )
)
setting_asset_storage_backend = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND,
    global_name='CONVERTER_ASSET_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing assets.'
    )
)
setting_asset_storage_backend_arguments = namespace.add_setting(
    default=DEFAULT_CONVERTER_ASSET_STORAGE_BACKEND_ARGUMENTS,
    global_name='CONVERTER_ASSET_STORAGE_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to pass to the CONVERTER_ASSET_STORAGE_BACKEND.'
    )
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
