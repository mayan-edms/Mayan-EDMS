from __future__ import absolute_import, unicode_literals

from .. import *  # NOQA

INSTALLED_APPS += ('test_without_migrations',)

INSTALLED_APPS = [
    cls for cls in INSTALLED_APPS if cls != 'whitenoise.runserver_nostatic'
]

COMMON_PRODUCTION_ERROR_LOG_PATH = '/tmp/mayan-errors.log'

# Remove whitenoise from middlewares. Causes out of memory errors during test
# suit
MIDDLEWARE_CLASSES = [
    cls for cls in MIDDLEWARE_CLASSES if cls != 'whitenoise.middleware.WhiteNoiseMiddleware'
]

# User a simpler password hasher
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

STATICFILES_STORAGE = None

# Cache templates in memory
TEMPLATES[0]['OPTIONS']['loaders'] = (
    (
        'django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    ),
)

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = 'memory'

# Remove middlewares not used for tests
MIDDLEWARE_CLASSES = [
    cls for cls in MIDDLEWARE_CLASSES if cls not in [
        'common.middleware.error_logging.ErrorLoggingMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'common.middleware.timezone.TimezoneMiddleware',
        'common.middleware.ajax_redirect.AjaxRedirect',
    ]
]
