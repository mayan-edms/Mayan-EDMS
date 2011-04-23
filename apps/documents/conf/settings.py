import datetime
import hashlib
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from common.utils import proper_name

from storage.backends.filebasedstorage import FileBasedStorage


def default_checksum(x):
    """hashlib.sha256(x).hexdigest()"""
    return hashlib.sha256(x).hexdigest()


def default_uuid():
    """unicode(uuid.uuid4())"""
    return unicode(uuid.uuid4())

default_available_functions = {
    'current_date': datetime.datetime.now().date,
}

default_available_models = {
    'User': User
}

available_transformations = {
    'rotate': {'label': _(u'Rotate [degrees]'), 'arguments': [{'name': 'degrees'}]}
}

available_indexing_functions = {
    'proper_name': proper_name
}

# Definition
AVAILABLE_FUNCTIONS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', default_available_functions)
AVAILABLE_MODELS = getattr(settings, 'DOCUMENTS_METADATA_AVAILABLE_MODELS', default_available_models)
AVAILABLE_INDEXING_FUNCTIONS = getattr(settings, 'DOCUMENTS_INDEXING_AVAILABLE_FUNCTIONS', available_indexing_functions)

# Upload
USE_STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_USE_STAGING_DIRECTORY', False)
STAGING_DIRECTORY = getattr(settings, 'DOCUMENTS_STAGING_DIRECTORY', u'/tmp/mayan/staging')
DELETE_STAGING_FILE_AFTER_UPLOAD = getattr(settings, 'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', False)
STAGING_FILES_PREVIEW_SIZE = getattr(settings, 'DOCUMENTS_STAGING_FILES_PREVIEW_SIZE', '640x480')
ENABLE_SINGLE_DOCUMENT_UPLOAD = getattr(settings, 'DOCUMENTS_ENABLE_SINGLE_DOCUMENT_UPLOAD', True)
UNCOMPRESS_COMPRESSED_LOCAL_FILES = getattr(settings, 'DOCUMENTS_UNCOMPRESS_COMPRESSED_LOCAL_FILES', True)
UNCOMPRESS_COMPRESSED_STAGING_FILES = getattr(settings, 'DOCUMENTS_UNCOMPRESS_COMPRESSED_STAGING_FILES', True)

# Saving
CHECKSUM_FUNCTION = getattr(settings, 'DOCUMENTS_CHECKSUM_FUNCTION', default_checksum)
UUID_FUNCTION = getattr(settings, 'DOCUMENTS_UUID_FUNCTION', default_uuid)

# Storage
STORAGE_BACKEND = getattr(settings, 'DOCUMENTS_STORAGE_BACKEND', FileBasedStorage)

# Usage
PREVIEW_SIZE = getattr(settings, 'DOCUMENTS_PREVIEW_SIZE', '640x480')
MULTIPAGE_PREVIEW_SIZE = getattr(settings, 'DOCUMENTS_MULTIPAGE_PREVIEW_SIZE', '160x120')
THUMBNAIL_SIZE = getattr(settings, 'DOCUMENTS_THUMBNAIL_SIZE', '50x50')
DISPLAY_SIZE = getattr(settings, 'DOCUMENTS_DISPLAY_SIZE', '1200')
RECENT_COUNT = getattr(settings, 'DOCUMENTS_RECENT_COUNT', 20)
ZOOM_PERCENT_STEP = getattr(settings, 'DOCUMENTS_ZOOM_PERCENT_STEP', 50)
ZOOM_MAX_LEVEL = getattr(settings, 'DOCUMENTS_ZOOM_MAX_LEVEL', 200)
ZOOM_MIN_LEVEL = getattr(settings, 'DOCUMENTS_ZOOM_MIN_LEVEL', 50)
ROTATION_STEP = getattr(settings, 'DOCUMENTS_ROTATION_STEP', 90)

# Transformations
AVAILABLE_TRANSFORMATIONS = getattr(settings, 'DOCUMENTS_AVAILABLE_TRANSFORMATIONS', available_transformations)
DEFAULT_TRANSFORMATIONS = getattr(settings, 'DOCUMENTS_DEFAULT_TRANSFORMATIONS', [])

#Groups
GROUP_MAX_RESULTS = getattr(settings, 'DOCUMENTS_GROUP_MAX_RESULTS', 20)
GROUP_SHOW_EMPTY = getattr(settings, 'DOCUMENTS_GROUP_SHOW_EMPTY', True)

setting_description = {
}
