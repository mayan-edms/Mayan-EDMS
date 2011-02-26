import datetime
import hashlib
import uuid
import tempfile

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from converter.api import get_page_count

from documents.storage import DocumentStorage

default_available_functions = {
    'current_date':datetime.datetime.now().date,
}

default_available_models = {
    'User':User
}

available_transformations = {
    'rotate': {'label':_(u'Rotate [degrees]'), 'arguments':[{'name':'degrees'}]}
}


# Definition
AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
AVAILABLE_MODELS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_MODELS', default_available_models)

# Upload
USE_STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_USE_STAGING_DIRECTORY', False)
STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_STAGING_DIRECTORY', u'/tmp/mayan/staging')
DELETE_STAGING_FILE_AFTER_UPLOAD = getattr(settings, 'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', False)
STAGING_FILES_PREVIEW_SIZE = getattr(settings, 'DOCUMENTS_STAGING_FILES_PREVIEW_SIZE', '640x480')
AUTOMATIC_OCR = getattr(settings, 'DOCUMENTS_AUTOMATIC_OCR', False)
ENABLE_SINGLE_DOCUMENT_UPLOAD = getattr(settings, 'DOCUMENTS_ENABLE_SINGLE_DOCUMENT_UPLOAD', True)
UNCOMPRESS_COMPRESSED_LOCAL_FILES = getattr(settings, 'DOCUMENTS_UNCOMPRESS_COMPRESSED_LOCAL_FILES', True)
UNCOMPRESS_COMPRESSED_STAGING_FILES = getattr(settings, 'DOCUMENTS_UNCOMPRESS_COMPRESSED_STAGING_FILES', True)

# Saving
CHECKSUM_FUNCTION = getattr(settings, 'DOCUMENTS_CHECKSUM_FUNCTION', lambda x: hashlib.sha256(x).hexdigest())
UUID_FUNCTION = getattr(settings, 'DOCUMENTS_UUID_FUNCTION', lambda:unicode(uuid.uuid4()))
PAGE_COUNT_FUNCTION = getattr(settings, 'DOCUMENTS_PAGE_COUNT_FUNCTION', lambda x: get_page_count(x.save_to_file(tempfile.mkstemp()[1])))

# Storage
STORAGE_BACKEND = getattr(settings, 'DOCUMENTS_STORAGE_BACKEND', DocumentStorage)
STORAGE_DIRECTORY_NAME = getattr(settings, 'DOCUMENTS_STORAGE_DIRECTORY_NAME', 'documents')

# Usage
PREVIEW_SIZE = getattr(settings, 'DOCUMENTS_PREVIEW_SIZE', '640x480')
MULTIPAGE_PREVIEW_SIZE = getattr(settings, 'DOCUMENTS_MULTIPAGE_PREVIEW_SIZE', '160x120')
THUMBNAIL_SIZE = getattr(settings, 'DOCUMENTS_THUMBNAIL_SIZE', '50x50')
DISPLAY_SIZE = getattr(settings, 'DOCUMENTS_DISPLAY_SIZE', '1200')

# Transformations
AVAILABLE_TRANSFORMATIONS = getattr(settings, 'DOCUMENTS_AVAILABLE_TRANSFORMATIONS', available_transformations)
DEFAULT_TRANSFORMATIONS = getattr(settings, 'DOCUMENTS_DEFAULT_TRANSFORMATIONS', [])

#Groups
GROUP_MAX_RESULTS = getattr(settings, 'DOCUMENTS_GROUP_MAX_RESULTS', 20)
GROUP_SHOW_EMPTY = getattr(settings, 'DOCUMENTS_GROUP_SHOW_EMPTY', True)
