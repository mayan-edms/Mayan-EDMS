import os
import tempfile

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

namespace = SettingNamespace(label=_('Storage'), name='storage')

setting_shared_storage = namespace.add_setting(
    global_name='STORAGE_SHARED_STORAGE',
    default='django.core.files.storage.FileSystemStorage',
    help_text=_('A storage backend that all workers can use to share files.')
)
setting_shared_storage_arguments = namespace.add_setting(
    global_name='STORAGE_SHARED_STORAGE_ARGUMENTS',
    default={'location': os.path.join(settings.MEDIA_ROOT, 'shared_files')}
)
setting_temporary_directory = namespace.add_setting(
    global_name='STORAGE_TEMPORARY_DIRECTORY', default=tempfile.gettempdir(),
    help_text=_(
        'Temporary directory used site wide to store thumbnails, previews '
        'and temporary files.'
    )
)
