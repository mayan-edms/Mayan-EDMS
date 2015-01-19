from __future__ import unicode_literals

from django.contrib.auth.models import User
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
    name='AUTO_CREATE_ADMIN',
    global_name='COMMON_AUTO_CREATE_ADMIN',
    default=True,
)

register_setting(
    namespace='common',
    module='common.settings',
    name='AUTO_ADMIN_USERNAME',
    global_name='COMMON_AUTO_ADMIN_USERNAME',
    default='admin',
)

register_setting(
    namespace='common',
    module='common.settings',
    name='AUTO_ADMIN_PASSWORD',
    global_name='COMMON_AUTO_ADMIN_PASSWORD',
    default=User.objects.make_random_password(),
)

register_setting(
    namespace='common',
    module='common.settings',
    name='LOGIN_METHOD',
    global_name='COMMON_LOGIN_METHOD',
    default='username',
    description=_('Controls the mechanism used to authenticated user.  Options are: username, email'),
)

register_setting(
    namespace='common',
    module='common.settings',
    name='ALLOW_ANONYMOUS_ACCESS',
    global_name='COMMON_ALLOW_ANONYMOUS_ACCESS',
    default=False,
    description=_('Allow non authenticated users, access to all views'),
)

register_setting(
    namespace='common',
    module='common.settings',
    name='SHARED_STORAGE',
    global_name='COMMON_SHARED_STORAGE',
    default='storage.backends.filebasedstorage.FileBasedStorage',
    description=_('A storage backend that all workers can use to share files.'),
)
