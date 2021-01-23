import os

from django.conf import settings

DEFAULT_SIGNATURES_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_SIGNATURES_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'document_signatures')
}
RETRY_DELAY = 10
STORAGE_NAME_DOCUMENT_SIGNATURES_DETACHED_SIGNATURE = 'document_signatures__detachedsignature'
