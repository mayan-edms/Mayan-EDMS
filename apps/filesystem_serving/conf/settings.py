from django.conf import settings

# Serving
FILESERVING_ENABLE = getattr(settings, 'FILESYSTEM_FILESERVING_ENABLE', True)
FILESERVING_PATH = getattr(settings, 'FILESYSTEM_FILESERVING_PATH', u'/tmp/mayan/documents')
SLUGIFY_PATHS = getattr(settings, 'FILESYSTEM_SLUGIFY_PATHS', False)
MAX_RENAME_COUNT = getattr(settings, 'FILESYSTEM_MAX_RENAME_COUNT', 200)
