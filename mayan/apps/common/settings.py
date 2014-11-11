"""Configuration options for the common app"""

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from smart_settings.api import register_setting

TEMPORARY_DIRECTORY = register_setting(
    namespace=u'common',
    module=u'common.settings',
    name=u'TEMPORARY_DIRECTORY',
    global_name=u'COMMON_TEMPORARY_DIRECTORY',
    default=u'/tmp',
    description=_(u'Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp()'),
    exists=True
)

register_setting(
    namespace=u'common',
    module=u'common.settings',
    name=u'AUTO_CREATE_ADMIN',
    global_name=u'COMMON_AUTO_CREATE_ADMIN',
    default=True,
)

register_setting(
    namespace=u'common',
    module=u'common.settings',
    name=u'AUTO_ADMIN_USERNAME',
    global_name=u'COMMON_AUTO_ADMIN_USERNAME',
    default=u'admin',
)

register_setting(
    namespace=u'common',
    module=u'common.settings',
    name=u'AUTO_ADMIN_PASSWORD',
    global_name=u'COMMON_AUTO_ADMIN_PASSWORD',
    default=User.objects.make_random_password(),
)

register_setting(
    namespace=u'common',
    module=u'common.settings',
    name=u'LOGIN_METHOD',
    global_name=u'COMMON_LOGIN_METHOD',
    default=u'username',
    description=_(u'Controls the mechanism used to authenticated user.  Options are: username, email'),
)

register_setting(
    namespace=u'common',
    module=u'common.settings',
    name=u'ALLOW_ANONYMOUS_ACCESS',
    global_name=u'COMMON_ALLOW_ANONYMOUS_ACCESS',
    default=False,
    description=_(u'Allow non authenticated users, access to all views'),
)

register_setting(
    namespace=u'common',
    module=u'common.settings',
    name=u'SHARED_STORAGE',
    global_name=u'COMMON_SHARED_STORAGE',
    default='storage.backends.filebasedstorage.FileBasedStorage',
    description=_(u'A storage backend that all workers can use to share files.'),
)
