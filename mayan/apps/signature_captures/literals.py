import os

from django.conf import settings

STORAGE_NAME_SIGNATURE_CAPTURES_CACHE = 'signature_captures__signaturecaptures_cache'

DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_MAXIMUM_SIZE = 10 * 2 ** 20  # 10 Megabytes
DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_SIGNATURE_CAPTURES_SIGNATURE_CAPTURE_CACHE_STORAGE_BACKEND_ARGUMENTS = {
    'location': os.path.join(
        settings.MEDIA_ROOT, 'signature_captures_signature_capture_cache'
    )
}
