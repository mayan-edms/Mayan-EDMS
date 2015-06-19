from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_setting

TEMPORARY_DIRECTORY = register_setting(
    namespace='common',
    module='common.settings',
    name='TEMPORARY_DIRECTORY',
    global_name='COMMON_TEMPORARY_DIRECTORY',
    default='/tmp',
    description=_('Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp()'),
    exists=True
)

register_setting(
    namespace='common',
    module='common.settings',
    name='SHARED_STORAGE',
    global_name='COMMON_SHARED_STORAGE',
    default='storage.backends.filebasedstorage.FileBasedStorage',
    description=_('A storage backend that all workers can use to share files.'),
)
