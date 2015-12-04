from __future__ import unicode_literals

import tempfile

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='common', label=_('Common'))
setting_temporary_directory = namespace.add_setting(
    global_name='COMMON_TEMPORARY_DIRECTORY', default=tempfile.gettempdir(),
    help_text=_(
        'Temporary directory used site wide to store thumbnails, previews '
        'and temporary files.  If none is specified, one will be created '
        'using tempfile.mkdtemp().'
    ),
    is_path=True
)
setting_shared_storage = namespace.add_setting(
    global_name='COMMON_SHARED_STORAGE',
    default='storage.backends.filebasedstorage.FileBasedStorage',
    help_text=_('A storage backend that all workers can use to share files.')
)
setting_paginate_by = namespace.add_setting(
    global_name='COMMON_PAGINATE_BY',
    default=40,
    help_text=_(
        'An integer specifying how many objects should be displayed per page.'
    )
)
setting_auto_logging = namespace.add_setting(
    global_name='COMMON_AUTO_LOGGING',
    default=True,
    help_text=_('Automatically enable logging to all apps.')
)
settings_db_sync_task_delay = namespace.add_setting(
    global_name='COMMON_DB_SYNC_TASK_DELAY',
    default=2,
    help_text=_(
        'Time to delay background tasks that depend on a database commit to '
        'propagate.'
    )
)
