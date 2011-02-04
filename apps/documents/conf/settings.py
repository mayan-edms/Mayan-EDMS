import datetime

from django.conf import settings

default_available_functions = {
    'current_date':datetime.datetime.now().date,
}

AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_STAGIN_DIRECTORY', '/tmp')
FILESERVING_PATH = getattr(settings, 'DOCUMENTS_FILESERVING_PATH', '/tmp')
