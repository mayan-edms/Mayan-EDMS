from __future__ import absolute_import

from .cleanup import cleanup

bootstrap_models = [
    {
        'name': 'documenttype',
    },
    {
        'name': 'documenttypefilename',
    }
]
cleanup_functions = [cleanup]
