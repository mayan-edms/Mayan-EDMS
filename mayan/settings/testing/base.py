from __future__ import absolute_import, unicode_literals

from .. import *  # NOQA

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
BROKER_BACKEND = 'memory'

COMMON_PRODUCTION_ERROR_LOG_PATH = '/tmp/mayan-errors.log'

DOCUMENT_PARSING_AUTO_PARSING = False

FILE_METADATA_AUTO_PROCESS = False

INSTALLED_APPS += ('test_without_migrations',)  # NOQA: F405

INSTALLED_APPS = [
    cls for cls in INSTALLED_APPS if cls != 'whitenoise.runserver_nostatic'
]

# Remove whitenoise from middlewares. Causes out of memory errors during test
# suit
MIDDLEWARE = [
    cls for cls in MIDDLEWARE if cls != 'whitenoise.middleware.WhiteNoiseMiddleware'  # NOQA: F405
]

# Remove middlewares not used for tests
MIDDLEWARE = [
    cls for cls in MIDDLEWARE if cls not in [
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

OCR_AUTO_OCR = False

# User a simpler password hasher
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

STATICFILES_STORAGE = None

# Cache templates in memory
TEMPLATES[0]['OPTIONS']['loaders'] = (  # NOQA: F405
    (
        'django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
    ),
)
