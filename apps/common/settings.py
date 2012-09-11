"""
Configuration options for the common app
"""
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from smart_settings import SettingsNamespace, LocalScope

from .literals import DEFAULT_PAGE_SIZE, DEFAULT_PAGE_ORIENTATION

namespace = SettingsNamespace(name='common', label=_(u'common'), module='common.settings')

namespace.add_setting(
    name='TEMPORARY_DIRECTORY',
    default=u'/tmp',
    description=_(u'Temporary directory used site wide to store thumbnails, previews and temporary files.  If none is specified, one will be created using tempfile.mkdtemp().'),
    exists=True,
    scopes=[LocalScope()]
)

namespace.add_setting(
    name=u'DEFAULT_PAPER_SIZE',
    default=DEFAULT_PAGE_SIZE,
    scopes=[LocalScope()]
)

namespace.add_setting(
    name=u'DEFAULT_PAGE_ORIENTATION',
    default=DEFAULT_PAGE_ORIENTATION,
    scopes=[LocalScope()]
)

namespace.add_setting(
    name=u'AUTO_CREATE_ADMIN',
    default=True,
    scopes=[LocalScope()]
)

namespace.add_setting(
    name=u'AUTO_ADMIN_USERNAME',
    default=u'admin',
    scopes=[LocalScope()]
)

namespace.add_setting(
    name=u'AUTO_ADMIN_PASSWORD',
    default=User.objects.make_random_password(),
    scopes=[LocalScope()]
)

namespace.add_setting(
    name=u'LOGIN_METHOD',
    default=u'username',
    description=_(u'Controls the mechanism used to authenticated user.  Options are: username, email'),
    scopes=[LocalScope()]
)

namespace.add_setting(
    name=u'ALLOW_ANONYMOUS_ACCESS',
    default=False,
    description=_(u'Allow non authenticated users, access to all views'),
    scopes=[LocalScope()]
)
