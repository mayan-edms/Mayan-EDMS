from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_LOCK_MANAGER_BACKEND, DEFAULT_LOCK_MANAGER_BACKEND_ARGUMENTS,
    DEFAULT_LOCK_MANAGER_DEFAULT_LOCK_TIMEOUT
)

namespace = SettingNamespace(label=_('Lock manager'), name='lock_manager')

setting_backend = namespace.add_setting(
    default=DEFAULT_LOCK_MANAGER_BACKEND, global_name='LOCK_MANAGER_BACKEND',
    help_text=_(
        'Path to the class to use when to request and release '
        'resource locks.'
    )
)
setting_backend_arguments = namespace.add_setting(
    default=DEFAULT_LOCK_MANAGER_BACKEND_ARGUMENTS,
    global_name='LOCK_MANAGER_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to pass to the LOCK_MANAGER_BACKEND.'
    )
)
setting_default_lock_timeout = namespace.add_setting(
    default=DEFAULT_LOCK_MANAGER_DEFAULT_LOCK_TIMEOUT,
    global_name='LOCK_MANAGER_DEFAULT_LOCK_TIMEOUT', help_text=_(
        'Default amount of time in seconds after which a resource '
        'lock will be automatically released.'
    )
)
