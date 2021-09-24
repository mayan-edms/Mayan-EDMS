from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_AUTHENTICATION_BACKEND, DEFAULT_AUTHENTICATION_BACKEND_ARGUMENTS,
    DEFAULT_AUTHENTICATION_DISABLE_PASSWORD_RESET
)

namespace = SettingNamespace(label=_('Authentication'), name='authentication')

setting_disable_password_reset = namespace.add_setting(
    default=DEFAULT_AUTHENTICATION_DISABLE_PASSWORD_RESET,
    global_name='AUTHENTICATION_DISABLE_PASSWORD_RESET', help_text=_(
        'Remove the "Forgot your password?" link on the login form used to '
        'trigger the password reset.'
    )
)
setting_authentication_backend = namespace.add_setting(
    default=DEFAULT_AUTHENTICATION_BACKEND,
    global_name='AUTHENTICATION_BACKEND',
    help_text=_(
        'Dotted path to the backend used to process user authentication.'
    )
)
setting_authentication_backend_arguments = namespace.add_setting(
    default=DEFAULT_AUTHENTICATION_BACKEND_ARGUMENTS,
    global_name='AUTHENTICATION_BACKEND_ARGUMENTS',
    help_text=_('Arguments for the AUTHENTICATION_BACKEND.')
)
