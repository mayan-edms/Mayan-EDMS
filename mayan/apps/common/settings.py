from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='common', label=_('Common'))
setting_temporary_directory = namespace.add_setting(
    global_name='COMMON_TEMPORARY_DIRECTORY', default='/tmp',
    help_text=_('Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp()'),
    is_path=True
)  # TODO: get os default temp directory
setting_shared_storage = namespace.add_setting(
    global_name='COMMON_SHARED_STORAGE',
    default='storage.backends.filebasedstorage.FileBasedStorage',
    help_text=_('A storage backend that all workers can use to share files.')
)
