from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_SIGNATURES_BACKEND, DEFAULT_DEFAULT_GPG_PATH,
    DEFAULT_SIGNATURES_KEYSERVER
)

namespace = SettingNamespace(label=_('Signatures'), name='django_gpg')

setting_gpg_backend = namespace.add_setting(
    default=DEFAULT_SIGNATURES_BACKEND,
    global_name='SIGNATURES_BACKEND',
    help_text=_(
        'Full path to the backend to be used to handle keys and signatures.'
    )
)
setting_gpg_backend_arguments = namespace.add_setting(
    default=DEFAULT_DEFAULT_GPG_PATH,
    global_name='SIGNATURES_BACKEND_ARGUMENTS',
)
setting_keyserver = namespace.add_setting(
    default=DEFAULT_SIGNATURES_KEYSERVER, global_name='SIGNATURES_KEYSERVER',
    help_text=_('Keyserver used to query for keys.')
)
