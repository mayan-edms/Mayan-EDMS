import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import LOGGING_HANDLER_OPTIONS

namespace = SettingNamespace(label=_('Logging'), name='logging')

setting_logging_enable = namespace.add_setting(
    global_name='LOGGING_ENABLE', default=True, help_text=_(
        'Automatically enable logging to all apps.'
    )
)
setting_logging_handlers = namespace.add_setting(
    global_name='LOGGING_HANDLERS', default=('console',),
    help_text=_(
        'List of handlers to which logging messages will be sent. '
        'Options are: {}'.format(', '.join(LOGGING_HANDLER_OPTIONS))
    )
)
setting_logging_level = namespace.add_setting(
    global_name='LOGGING_LEVEL', default='ERROR', help_text=_(
        'Level for the logging system.'
    )
)
setting_logging_log_file_path = namespace.add_setting(
    global_name='LOGGING_LOG_FILE_PATH',
    default=os.path.join(settings.MEDIA_ROOT, 'error.log'), help_text=_(
        'Path to the logfile that will track errors during production.'
    ),
    is_path=True
)
