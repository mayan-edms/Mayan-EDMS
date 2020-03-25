from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

from .literals import DEFAULT_GPG_PATH

namespace = Namespace(label=_('Signatures'), name='django_gpg')


setting_gpg_backend = namespace.add_setting(
    global_name='SIGNATURES_BACKEND',
    default='mayan.apps.django_gpg.backends.python_gnupg.PythonGNUPGBackend',
    help_text=_(
        'Full path to the backend to be used to handle keys and signatures.'
    )
)
setting_gpg_backend_arguments = namespace.add_setting(
    global_name='SIGNATURES_BACKEND_ARGUMENTS',
    default={
        'gpg_path': DEFAULT_GPG_PATH,
    }
)
setting_keyserver = namespace.add_setting(
    global_name='SIGNATURES_KEYSERVER', default='pool.sks-keyservers.net',
    help_text=_('Keyserver used to query for keys.')
)
