from __future__ import absolute_import

from .cleanup import cleanup

bootstrap_models = [
    {
        'name': 'defaultaccessentry',
    },
]
cleanup_functions = [cleanup]
