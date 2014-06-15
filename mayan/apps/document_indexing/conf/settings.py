"""Configuration options for the document_indexing app"""

from django.utils.translation import ugettext_lazy as _

from common.utils import proper_name
from smart_settings.api import register_settings

available_indexing_functions = {
    'proper_name': proper_name
}

register_settings(
    namespace=u'document_indexing',
    module=u'document_indexing.conf.settings',
    settings=[
        # Definition
        {'name': u'AVAILABLE_INDEXING_FUNCTIONS', 'global_name': u'DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS', 'default': available_indexing_functions},
        {'name': u'SUFFIX_SEPARATOR', 'global_name': u'DOCUMENT_INDEXING_SUFFIX_SEPARATOR', 'default': u'_'},
        # Filesystem serving
        {'name': u'SLUGIFY_PATHS', 'global_name': u'DOCUMENT_INDEXING_FILESYSTEM_SLUGIFY_PATHS', 'default': False},
        {'name': u'MAX_SUFFIX_COUNT', 'global_name': u'DOCUMENT_INDEXING_FILESYSTEM_MAX_SUFFIX_COUNT', 'default': 1000},
        {'name': u'FILESYSTEM_SERVING', 'global_name': u'DOCUMENT_INDEXING_FILESYSTEM_SERVING', 'default': {}, 'description': _(u'A dictionary that maps the index name and where on the filesystem that index will be mirrored.')}
    ]
)
