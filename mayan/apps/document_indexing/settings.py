from __future__ import unicode_literals

from smart_settings.api import register_settings

available_indexing_functions = {
}

register_settings(
    namespace='document_indexing',
    module='document_indexing.settings',
    settings=[
        # Definition
        {'name': 'AVAILABLE_INDEXING_FUNCTIONS', 'global_name': 'DOCUMENT_INDEXING_AVAILABLE_INDEXING_FUNCTIONS', 'default': available_indexing_functions},
    ]
)
