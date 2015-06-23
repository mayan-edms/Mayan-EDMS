from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='authentication', label=_('Authentication'))
setting_login_method = namespace.add_setting(global_name='AUTHENTICATION_LOGIN_METHOD', default='username', help_text=_('Controls the mechanism used to authenticated user. Options are: username, email'))
setting_allow_anonymous_access = namespace.add_setting(global_name='AUTHENTICATION_ALLOW_ANONYMOUS_ACCESS', default=False, help_text=_('Allow non authenticated users, access to all views'))
