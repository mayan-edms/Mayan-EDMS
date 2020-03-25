from . import *  # NOQA

CELERY_TASK_ALWAYS_EAGER = False

TEMPLATES[0]['OPTIONS']['loaders'] = (  # NOQA: F405
    (
        'django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    ),
)
