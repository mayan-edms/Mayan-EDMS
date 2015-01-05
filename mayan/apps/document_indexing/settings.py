"""Configuration options for the document_indexing app"""

from smart_settings.api import register_settings

available_indexing_functions = {
}

register_settings(
    namespace=u'document_indexing',
    module=u'document_indexing.settings',
    settings=[
        # Definition
        {'name': u'AVAILABLE_INDEXING_FUNCTIONS', 'global_name': u'DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS', 'default': available_indexing_functions},
    ]
)
