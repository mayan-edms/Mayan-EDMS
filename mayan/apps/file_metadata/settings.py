from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_FILE_METADATA_AUTO_PROCESS,
    DEFAULT_FILE_METADATA_DRIVERS_ARGUMENTS
)
from .setting_migrations import FileMetadataSettingMigration

namespace = SettingNamespace(
    label=_('File metadata'), migration_class=FileMetadataSettingMigration,
    name='file_metadata', version='0002'
)
setting_auto_process = namespace.add_setting(
    default=DEFAULT_FILE_METADATA_AUTO_PROCESS,
    global_name='FILE_METADATA_AUTO_PROCESS', help_text=_(
        'Set new document types to perform file metadata processing '
        'automatically by default.'
    )
)
setting_drivers_arguments = namespace.add_setting(
    default=DEFAULT_FILE_METADATA_DRIVERS_ARGUMENTS,
    global_name='FILE_METADATA_DRIVERS_ARGUMENTS', help_text=_(
        'Arguments to pass to the drivers.'
    )
)
