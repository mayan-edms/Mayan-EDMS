from .. import *  # NOQA

ALLOWED_HOSTS = ['*']

DEBUG = True

CELERY_BROKER_URL = 'memory://'
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

# Allow using WhiteNoise in development.
INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')

LOGGING_LEVEL = 'DEBUG'
ROOT_URLCONF = 'mayan.urls.development'

SEARCH_BACKEND = 'mayan.apps.dynamic_search.backends.django.DjangoSearchBackend'

TEMPLATES[0]['OPTIONS']['loaders'] = (  # NOQA: F405
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

WSGI_AUTO_RELOAD = True
