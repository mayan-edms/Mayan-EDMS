import datetime
import hashlib
import uuid

from django.conf import settings

default_available_functions = {
    'current_date':datetime.datetime.now().date,
}

AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_STAGING_DIRECTORY', u'/tmp/mayan/staging')
FILESERVING_PATH = getattr(settings, 'DOCUMENTS_FILESERVING_PATH', u'/tmp/mayan/documents')
DELETE_LOCAL_ORIGINAL = getattr(settings, 'DOCUMENTS_DELETE_LOCAL_ORIGINAL', False)
SLUGIFY_PATH = getattr(settings, 'DOCUMENTS_SLUGIFY_PATH', False)
CHECKSUM_FUNCTION = getattr(settings, 'DOCUMENTS_CHECKSUM_FUNCTION', lambda x: hashlib.sha256(x).hexdigest())
DELETE_STAGING_FILE_AFTER_UPLOAD = getattr(settings, 'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', False)
UUID_FUNCTION = getattr(settings, 'DOCUMENTS_UUID_FUNTION', lambda:unicode(uuid.uuid4()))
STORAGE_DIRECTORY_NAME = getattr(settings, 'DOCUMENTS_STORAGE_DIRECTORY_NAME', 'documents')
