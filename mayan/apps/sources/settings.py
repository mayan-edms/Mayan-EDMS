from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_SOURCES_BACKEND_ARGUMENTS,
    DEFAULT_SOURCES_CACHE_STORAGE_BACKEND,
    DEFAULT_SOURCES_CACHE_STORAGE_BACKEND_ARGUMENTS
)
from .setting_migrations import SourcesSettingMigration

namespace = SettingNamespace(
    label=_('Sources'), migration_class=SourcesSettingMigration,
    name='sources', version='0003'
)

setting_backend_arguments = namespace.add_setting(
    default=DEFAULT_SOURCES_BACKEND_ARGUMENTS,
    global_name='SOURCES_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to use when creating source backends.'
    )
)
setting_source_cache_storage_backend = namespace.add_setting(
    global_name='SOURCES_CACHE_STORAGE_BACKEND',
    default=DEFAULT_SOURCES_CACHE_STORAGE_BACKEND, help_text=_(
        'Path to the Storage subclass used to store cached '
        'source image files.'
    )
)
setting_source_cache_storage_backend_arguments = namespace.add_setting(
    global_name='SOURCES_CACHE_STORAGE_BACKEND_ARGUMENTS',
    default=DEFAULT_SOURCES_CACHE_STORAGE_BACKEND_ARGUMENTS,
    help_text=_(
        'Arguments to pass to the SOURCES_SOURCE_CACHE_STORAGE_BACKEND.'
    )
)
