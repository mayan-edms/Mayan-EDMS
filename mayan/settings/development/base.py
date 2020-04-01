from __future__ import absolute_import, unicode_literals

from .. import *  # NOQA

ALLOWED_HOSTS = ['*']

DEBUG = True

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = CELERY_TASK_ALWAYS_EAGER  # NOQA: F405
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if 'rosetta' not in INSTALLED_APPS:   # NOQA: F405
    try:
        import rosetta  # NOQA: F401
    except ImportError:
        pass
    else:
        INSTALLED_APPS += (  # NOQA: F405
            'rosetta',
        )

if 'django_extensions' not in INSTALLED_APPS:
    try:
        import django_extensions  # NOQA: F401
    except ImportError:
        pass
    else:
        INSTALLED_APPS += (
            'django_extensions',
        )

ROOT_URLCONF = 'mayan.urls.development'

TEMPLATES[0]['OPTIONS']['loaders'] = (  # NOQA: F405
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

WSGI_AUTO_RELOAD = True
