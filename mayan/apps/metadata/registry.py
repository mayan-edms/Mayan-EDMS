from __future__ import absolute_import

from .cleanup import cleanup


bootstrap_models = [
    {
        'name': 'metadatatype',
    },
    {
        'name': 'metadataset',
        'dependencies': ['metadata.metadatatype']
    },
    {
        'name': 'metadatasetitem',
        'dependencies': ['metadata.metadataset']
    },
    {
        'name': 'documenttypedefaults',
        'dependencies': ['documents.documenttype']
    },
]
cleanup_functions = [cleanup]
