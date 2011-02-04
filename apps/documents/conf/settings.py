import datetime
import hashlib

from django.conf import settings

default_available_functions = {
    'current_date':datetime.datetime.now().date,
}

AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_STAGING_DIRECTORY', '/tmp')
FILESERVING_PATH = getattr(settings, 'DOCUMENTS_FILESERVING_PATH', '/tmp')
DELETE_ORIGINAL = getattr(settings, 'DOCUMENTS_DELETE_ORIGINAL', False)
SLUGIFY_PATH = getattr(settings, 'DOCUMENTS_SLUGIFY_PATH', False)
CHECKSUM_FUNCTION = getattr(settings, 'DOCUMENTS_CHECKSUM_FUNCTION', lambda x: hashlib.sha256(x).hexdigest())
