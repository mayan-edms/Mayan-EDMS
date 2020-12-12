from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_LOGGING_ENABLE, DEFAULT_LOGGING_HANDLERS, DEFAULT_LOGGING_LEVEL,
    DEFAULT_LOGGING_LOG_FILE_PATH, LOGGING_HANDLER_OPTIONS
)

namespace = SettingNamespace(label=_('Logging'), name='logging')

setting_logging_enable = namespace.add_setting(
    default=DEFAULT_LOGGING_ENABLE, global_name='LOGGING_ENABLE', help_text=_(
        'Automatically enable logging to all apps.'
    )
)
setting_logging_handlers = namespace.add_setting(
    default=DEFAULT_LOGGING_HANDLERS, global_name='LOGGING_HANDLERS', help_text=_(
        'List of handlers to which logging messages will be sent. '
        'Options are: {}'.format(', '.join(LOGGING_HANDLER_OPTIONS))
    )
)
setting_logging_level = namespace.add_setting(
    default=DEFAULT_LOGGING_LEVEL, global_name='LOGGING_LEVEL', help_text=_(
        'Level for the logging system.'
    )
)
setting_logging_log_file_path = namespace.add_setting(
    default=DEFAULT_LOGGING_LOG_FILE_PATH,
    global_name='LOGGING_LOG_FILE_PATH', help_text=_(
        'Path to the logfile that will track errors during production.'
    ), is_path=True
)
