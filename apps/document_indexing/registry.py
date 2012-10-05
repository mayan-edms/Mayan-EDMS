from __future__ import absolute_import

from .cleanup import cleanup

bootstrap_models = [
    {
        'name': 'index',
    },
    {
        'name': 'indextemplatenode',
        'sanitize': False,
    }
]
cleanup_functions = [cleanup]
