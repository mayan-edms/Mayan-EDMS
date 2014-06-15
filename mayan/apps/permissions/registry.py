from __future__ import absolute_import

from .cleanup import cleanup


bootstrap_models = [
    {
        'name': 'role',
    },
]
cleanup_functions = [cleanup]
