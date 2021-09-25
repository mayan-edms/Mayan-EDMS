from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_PLATFORM_CLIENT_BACKEND_ARGUMENTS,
    DEFAULT_PLATFORM_CLIENT_BACKEND_ENABLED
)


namespace = SettingNamespace(label=_('Platform'), name='platform')

setting_client_backend_enabled = namespace.add_setting(
    default=DEFAULT_PLATFORM_CLIENT_BACKEND_ENABLED,
    global_name='PLATFORM_CLIENT_BACKEND_ENABLED', help_text=_(
        'List of client backends to launch after startup. Use full dotted '
        'path to the client backend classes.'
    )
)
setting_client_backend_arguments = namespace.add_setting(
    default=DEFAULT_PLATFORM_CLIENT_BACKEND_ARGUMENTS,
    global_name='PLATFORM_CLIENT_BACKEND_ARGUMENTS', help_text=_(
        'Arguments for the client backends. Use the client backend dotted '
        'path as the dictionary key for the arguments in dictionary format.'
    )
)
