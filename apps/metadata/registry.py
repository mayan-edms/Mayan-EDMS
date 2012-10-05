from __future__ import absolute_import

from .cleanup import cleanup


bootstrap_models = [
    {
        'name': 'metadatatype',
    },
    {
        'name': 'metadataset',
    },
    {
        'name': 'metadatasetitem',
    },
    {
        'name': 'documenttypedefaults',
    },
]
cleanup_functions = [cleanup]
