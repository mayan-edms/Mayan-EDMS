import datetime
import hashlib
import uuid

from django.conf import settings
from django.contrib.auth.models import User

from documents.storage import DocumentStorage

default_available_functions = {
    'current_date':datetime.datetime.now().date,
}

default_available_models = {
    'User':User
}

# Definition
AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
AVAILABLE_MODELS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_MODELS', default_available_models)
# Upload
USE_STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_USE_STAGING_DIRECTORY', False)
STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_STAGING_DIRECTORY', u'/tmp/mayan/staging')
DELETE_STAGING_FILE_AFTER_UPLOAD = getattr(settings, 'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', False)
STAGING_FILES_PREVIEW_SIZE = getattr(settings, 'DOCUMENTS_STAGING_FILES_PREVIEW_SIZE', '640x480')

DELETE_LOCAL_ORIGINAL = getattr(settings, 'DOCUMENTS_DELETE_LOCAL_ORIGINAL', False)
# Saving
CHECKSUM_FUNCTION = getattr(settings, 'DOCUMENTS_CHECKSUM_FUNCTION', lambda x: hashlib.sha256(x).hexdigest())
UUID_FUNCTION = getattr(settings, 'DOCUMENTS_UUID_FUNTION', lambda:unicode(uuid.uuid4()))
# Storage
STORAGE_BACKEND = getattr(settings, 'DOCUMENTS_STORAGE_BACKEND', DocumentStorage)
STORAGE_DIRECTORY_NAME = getattr(settings, 'DOCUMENTS_STORAGE_DIRECTORY_NAME', 'documents')
# Serving
FILESYSTEM_FILESERVING_ENABLE = getattr(settings, 'DOCUMENTS_FILESYSTEM_FILESERVING_ENABLE', True)
FILESYSTEM_FILESERVING_PATH = getattr(settings, 'DOCUMENTS_FILESERVING_PATH', u'/tmp/mayan/documents')
FILESYSTEM_SLUGIFY_PATHS = getattr(settings, 'DOCUMENTS_SLUGIFY_PATHS', False)
FILESYSTEM_MAX_RENAME_COUNT = getattr(settings, 'DOCUMENTS_FILESYSTEM_MAX_RENAME_COUNT', 200)
#misc
TEMPORARY_DIRECTORY = getattr(settings, 'DOCUMENTS_TEMPORARY_DIRECTORY', u'/tmp')
