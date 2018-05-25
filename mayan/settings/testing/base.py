from __future__ import absolute_import, unicode_literals

from .. import *  # NOQA

INSTALLED_APPS += ('test_without_migrations',)

INSTALLED_APPS = [
    cls for cls in INSTALLED_APPS if cls != 'whitenoise.runserver_nostatic'
]

COMMON_PRODUCTION_ERROR_LOG_PATH = '/tmp/mayan-errors.log'

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Remove whitenoise from middlewares. Causes out of memory errors during test
# suit
MIDDLEWARE_CLASSES = [
    cls for cls in MIDDLEWARE_CLASSES if cls != 'whitenoise.middleware.WhiteNoiseMiddleware'
]

STATICFILES_STORAGE = None
