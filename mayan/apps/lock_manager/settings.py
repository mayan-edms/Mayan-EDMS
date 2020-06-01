from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import DEFAULT_BACKEND, DEFAULT_LOCK_TIMEOUT_VALUE

namespace = SettingNamespace(label=_('Lock manager'), name='lock_manager')

setting_backend = namespace.add_setting(
    default=DEFAULT_BACKEND,
    global_name='LOCK_MANAGER_BACKEND', help_text=_(
        'Path to the class to use when to request and release '
        'resource locks.'
    )
)
setting_backend_arguments = namespace.add_setting(
    global_name='LOCK_MANAGER_BACKEND_ARGUMENTS',
    default={}, help_text=_('Arguments to pass to the LOCK_MANAGER_BACKEND.')
)

setting_default_lock_timeout = namespace.add_setting(
    default=DEFAULT_LOCK_TIMEOUT_VALUE,
    global_name='LOCK_MANAGER_DEFAULT_LOCK_TIMEOUT', help_text=_(
        'Default amount of time in seconds after which a resource '
        'lock will be automatically released.'
    )
)
