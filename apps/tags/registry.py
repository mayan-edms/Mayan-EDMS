from __future__ import absolute_import

from .cleanup import cleanup


bootstrap_models = [
    {
        'name': 'taggit.tag',
        'sanitize': False,
    },
    {
        'name': 'tagproperties',
        'dependencies': ['taggit.tag']
    }
]
cleanup_functions = [cleanup]
