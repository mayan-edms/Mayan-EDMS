from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_MIME_TYPE_BACKEND, DEFAULT_MIME_TYPE_BACKEND_ARGUMENTS
)

namespace = SettingNamespace(label=_('MIME types'), name='mime_types')

setting_backend = namespace.add_setting(
    default=DEFAULT_MIME_TYPE_BACKEND, global_name='MIME_TYPE_BACKEND',
    help_text=_(
        'Path to the class to use when to detect file MIME types.'
    )
)
setting_backend_arguments = namespace.add_setting(
    default=DEFAULT_MIME_TYPE_BACKEND_ARGUMENTS,
    global_name='MIME_TYPE_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to pass to the MIME_TYPE_BACKEND.'
    )
)
