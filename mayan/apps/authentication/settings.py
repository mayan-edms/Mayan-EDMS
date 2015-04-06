from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_setting

register_setting(
    namespace='authentication',
    module='authentication.settings',
    name='LOGIN_METHOD',
    global_name='COMMON_LOGIN_METHOD',
    default='username',
    description=_('Controls the mechanism used to authenticated user. Options are: username, email'),
)

register_setting(
    namespace='authentication',
    module='authentication.settings',
    name='ALLOW_ANONYMOUS_ACCESS',
    global_name='COMMON_ALLOW_ANONYMOUS_ACCESS',
    default=False,
    description=_('Allow non authenticated users, access to all views'),
)
