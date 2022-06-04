from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_MAXIMUM_SIZE,
    DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND,
    DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND_ARGUMENTS
)
from .setting_callbacks import callback_update_signature_capture_cache_size

namespace = SettingNamespace(
    label=_('Signature captures'), name='signature_captures',
)


setting_signature_capture_cache_maximum_size = namespace.add_setting(
    default=DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_MAXIMUM_SIZE,
    global_name='SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_MAXIMUM_SIZE',
    help_text=_(
        'The threshold at which the SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND '
        'will start deleting the oldest signature capture cache files. '
        'Specify the size in bytes.'
    ), post_edit_function=callback_update_signature_capture_cache_size
)
setting_signature_capture_cache_storage_backend = namespace.add_setting(
    default=DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND,
    global_name='SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'signature capture files.'
    )
)
setting_signature_capture_cache_storage_backend_arguments = namespace.add_setting(
    default=DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND_ARGUMENTS,
    global_name='SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND_ARGUMENTS',
    help_text=_(
        'Arguments to pass to the SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND.'
    )
)
