"""Configuration options for the common app"""

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from smart_settings.api import register_setting

from common.literals import PAGE_SIZE_LETTER, PAGE_ORIENTATION_PORTRAIT

TEMPORARY_DIRECTORY = register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'TEMPORARY_DIRECTORY',
    global_name=u'COMMON_TEMPORARY_DIRECTORY',
    default=u'/tmp',
    description=_(u'Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp()'),
    exists=True
)

DEFAULT_PAPER_SIZE = register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'DEFAULT_PAPER_SIZE',
    global_name=u'COMMON_DEFAULT_PAPER_SIZE',
    default=PAGE_SIZE_LETTER,
)

DEFAULT_PAGE_ORIENTATION = register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'DEFAULT_PAGE_ORIENTATION',
    global_name=u'COMMON_DEFAULT_PAGE_ORIENTATION',
    default=PAGE_ORIENTATION_PORTRAIT,
)

register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'AUTO_CREATE_ADMIN',
    global_name=u'COMMON_AUTO_CREATE_ADMIN',
    default=True,
)

register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'AUTO_ADMIN_USERNAME',
    global_name=u'COMMON_AUTO_ADMIN_USERNAME',
    default=u'admin',
)

register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'AUTO_ADMIN_PASSWORD',
    global_name=u'COMMON_AUTO_ADMIN_PASSWORD',
    default=User.objects.make_random_password(),
)

register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'LOGIN_METHOD',
    global_name=u'COMMON_LOGIN_METHOD',
    default=u'username',
    description=_(u'Controls the mechanism used to authenticated user.  Options are: username, email'),
)

register_setting(
    namespace=u'common',
    module=u'common.conf.settings',
    name=u'ALLOW_ANONYMOUS_ACCESS',
    global_name=u'COMMON_ALLOW_ANONYMOUS_ACCESS',
    default=False,
    description=_(u'Allow non authenticated users, access to all views'),
)
