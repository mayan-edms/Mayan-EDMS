
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_SOURCES_SCANIMAGE_PATH,
    DEFAULT_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND,
    DEFAULT_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS
)
from .setting_migrations import SourcesSettingMigration

namespace = SettingNamespace(
    label=_('Sources'), migration_class=SourcesSettingMigration,
    name='sources', version='0002'
)

setting_scanimage_path = namespace.add_setting(
    default=DEFAULT_SOURCES_SCANIMAGE_PATH,
    global_name='SOURCES_SCANIMAGE_PATH', help_text=_(
        'File path to the scanimage program used to control image scanners.'
    ), is_path=True
)
setting_staging_file_image_cache_storage = namespace.add_setting(
    global_name='SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND',
    default=DEFAULT_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND, help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'staging_file image files.'
    )
)
setting_staging_file_image_cache_storage_arguments = namespace.add_setting(
    global_name='SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS',
    default=DEFAULT_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS,
    help_text=_(
        'Arguments to pass to the SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND.'
    )
)
