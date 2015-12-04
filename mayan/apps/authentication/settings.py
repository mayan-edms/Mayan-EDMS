from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='authentication', label=_('Authentication'))
setting_login_method = namespace.add_setting(
    global_name='AUTHENTICATION_LOGIN_METHOD', default='username',
    help_text=_(
        'Controls the mechanism used to authenticated user. Options are: '
        'username, email'
    )
)
