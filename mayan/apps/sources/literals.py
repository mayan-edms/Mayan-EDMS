import os

from django.conf import settings

DEFAULT_BINARY_SCANIMAGE_PATH = '/usr/bin/scanimage'
DEFAULT_SOURCES_BACKEND_ARGUMENTS = {
    'mayan.apps.sources.source_backends.SourceBackendSANEScanner': {
        'scanimage_path': DEFAULT_BINARY_SCANIMAGE_PATH
    }
}
DEFAULT_SOURCES_CACHE_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_SOURCES_CACHE_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'source_cache')
}

DEFAULT_SOURCES_LOCK_EXPIRE = 600

STORAGE_NAME_SOURCE_CACHE_FOLDER = 'sources__source_cache'
