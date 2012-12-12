from __future__ import absolute_import

from .cleanup import cleanup


bootstrap_models = [
    {
        'name': 'smartlink',
    },
    {
        'name': 'smartlinkcondition',
    }
]

cleanup_functions = [cleanup]
