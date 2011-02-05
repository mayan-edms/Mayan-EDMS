import datetime
import hashlib

from django.conf import settings

default_available_functions = {
    'current_date':datetime.datetime.now().date,
}

AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_STAGING_DIRECTORY', u'/tmp')
FILESERVING_PATH = getattr(settings, 'DOCUMENTS_FILESERVING_PATH', u'/tmp')
DELETE_LOCAL_ORIGINAL = getattr(settings, 'DOCUMENTS_DELETE_LOCAL_ORIGINAL', False)
SLUGIFY_PATH = getattr(settings, 'DOCUMENTS_SLUGIFY_PATH', False)
CHECKSUM_FUNCTION = getattr(settings, 'DOCUMENTS_CHECKSUM_FUNCTION', lambda x: hashlib.sha256(x).hexdigest())
DELETE_STAGING_FILE_AFTER_UPLOAD = getattr(settings, 'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', False)
