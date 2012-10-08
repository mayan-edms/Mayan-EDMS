from __future__ import absolute_import

from .cleanup import cleanup

bootstrap_models = [
    {
        'name': 'index',
        'dependencies': ['documents.documenttype']
    },
    {
        'name': 'indextemplatenode',
        'sanitize': False,
        'dependencies': ['document_indexing.index']
    }
]
cleanup_functions = [cleanup]
