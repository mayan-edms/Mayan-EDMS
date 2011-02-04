import datetime

from django.conf import settings

default_available_functions = {
    'current_date':datetime.datetime.now().date,
}

AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
