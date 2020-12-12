import os

from django.conf import settings

DEFAULT_ERROR_LOG_PARTITION_ENTRY_LIMIT = 3
DEFAULT_LOGGING_ENABLE = True
DEFAULT_LOGGING_HANDLERS = ('console',)
DEFAULT_LOGGING_LEVEL = 'ERROR'
DEFAULT_LOGGING_LOG_FILE_PATH = os.path.join(settings.MEDIA_ROOT, 'error.log')

LOGGING_HANDLER_OPTIONS = ('console', 'logfile')
