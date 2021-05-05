from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_MAXIMUM_FAILED_PRUNE_ATTEMPTS,
    DEFAULT_MAXIMUM_NORMAL_PRUNE_ATTEMPTS
)

namespace = SettingNamespace(label=_('File caching'), name='file_caching')

setting_maximum_failed_prune_attempts = namespace.add_setting(
    default=DEFAULT_MAXIMUM_FAILED_PRUNE_ATTEMPTS,
    global_name='FILE_CACHING_MAXIMUM_FAILED_PRUNE_ATTEMPTS', help_text=_(
        'Number of times a cache will retry failed attempts to prune '
        'files to free up space for new a file being requested, before '
        'giving up.'
    )
)
setting_maximum_normal_prune_attempts = namespace.add_setting(
    default=DEFAULT_MAXIMUM_NORMAL_PRUNE_ATTEMPTS,
    global_name='FILE_CACHING_MAXIMUM_NORMAL_PRUNE_ATTEMPTS', help_text=_(
        'Number of times a cache will attempt to prune files to free up '
        'space for new a file being requested, before giving up.'
    )
)
