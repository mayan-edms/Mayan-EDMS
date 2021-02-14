import os
import tempfile

from django.conf import settings

DEFAULT_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
DEFAULT_STORAGE_DOWNLOAD_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
DEFAULT_STORAGE_DOWNLOAD_FILE_STORAGE_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'download_files')
}
DEFAULT_STORAGE_SHARED_STORAGE = 'django.core.files.storage.FileSystemStorage'
DEFAULT_STORAGE_SHARED_STORAGE_ARGUMENTS = {
    'location': os.path.join(settings.MEDIA_ROOT, 'shared_files')
}
DEFAULT_STORAGE_TEMPORARY_DIRECTORY = tempfile.gettempdir()
DELETE_STALE_UPLOADS_INTERVAL = 60 * 10  # 10 minutes
INTERVAL_DOWNLOAD_FILE_EXPIRATION = 60 * 24 * 2  # 2 days
INTERVAL_SHARED_UPLOAD_STALE = 60 * 60 * 24 * 7  # 7 days
MSG_MIME_TYPES = (
    'application/vnd.ms-outlook', 'application/vnd.ms-office'
)
STORAGE_NAME_DOWNLOAD_FILE = 'storage__downloadfile'
STORAGE_NAME_SHARED_UPLOADED_FILE = 'storage__shareduploadedfile'
TASK_SHARED_UPLOADS_STALE_INTERVAL = 60 * 10  # 10 minutes
TASK_DOWNLOAD_FILE_STALE_INTERVAL = 60 * 10  # 10 minutes
