from django.conf import settings

from common.utils import proper_name

available_indexing_functions = {
    'proper_name':proper_name
}


# Serving
FILESERVING_ENABLE = getattr(settings, 'FILESYSTEM_FILESERVING_ENABLE', True)
FILESERVING_PATH = getattr(settings, 'FILESYSTEM_FILESERVING_PATH', u'/tmp/mayan/documents')
SLUGIFY_PATHS = getattr(settings, 'FILESYSTEM_SLUGIFY_PATHS', False)
MAX_RENAME_COUNT = getattr(settings, 'FILESYSTEM_MAX_RENAME_COUNT', 200)
AVAILABLE_INDEXING_FUNCTIONS = getattr(settings, 'FILESYSTEM_INDEXING_AVAILABLE_FUNCTIONS', available_indexing_functions)
