from __future__ import absolute_import, unicode_literals

from . import *  # NOQA

CELERY_TASK_ALWAYS_EAGER = False

TEMPLATES[0]['OPTIONS']['loaders'] = (
    (
        'django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    ),
)
