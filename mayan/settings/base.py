"""
Django settings for Mayan EDMS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from __future__ import unicode_literals

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from django.utils.translation import ugettext_lazy as _

_file_path = os.path.abspath(os.path.dirname(__file__)).split('/')

BASE_DIR = '/'.join(_file_path[0:-2])

MEDIA_ROOT = os.path.join(BASE_DIR, 'mayan', 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_key_missing'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    # Placed at the top so it can override any template
    'appearance',
    # 3rd party
    'suit',
    # Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # 3rd party
    'actstream',
    'autoadmin',
    'colorful',
    'compressor',
    'corsheaders',
    'djcelery',
    'filetransfers',
    'mptt',
    'pure_pagination',
    'rest_framework',
    'rest_framework.authtoken',
    'solo',
    'widget_tweaks',
    # Base generic
    'acls',
    'authentication',
    'common',
    'converter',
    'django_gpg',
    'dynamic_search',
    'lock_manager',
    'mimetype',
    'navigation',
    'permissions',
    'smart_settings',
    'user_management',
    # Mayan EDMS
    'checkouts',
    'document_comments',
    'document_indexing',
    'document_signatures',
    'document_states',
    'documents',
    'events',
    'folders',
    'installation',
    'linking',
    'mailer',
    'metadata',
    'mirroring',
    'ocr',
    'rest_api',
    'sources',
    'statistics',
    'storage',
    'tags',
    # Placed after rest_api to allow template overriding
    'rest_framework_swagger',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'common.middleware.timezone.TimezoneMiddleware',
    'common.middleware.strip_spaces_widdleware.SpacelessMiddleware',
    'authentication.middleware.login_required_middleware.LoginRequiredMiddleware',
    'common.middleware.ajax_redirect.AjaxRedirect',
)

ROOT_URLCONF = 'mayan.urls'

WSGI_APPLICATION = 'mayan.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MEDIA_ROOT, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'


# ------------ Custom settings section ----------

TEMPLATE_DEBUG = True
PROJECT_TITLE = 'Mayan EDMS'
PROJECT_NAME = 'mayan'
PROJECT_WEBSITE = 'http://www.mayan-edms.com'

LANGUAGES = (
    ('ar', _('Arabic')),
    ('bg', _('Bulgarian')),
    ('bs', _('Bosnian (Bosnia and Herzegovina)')),
    ('da', _('Danish')),
    ('de', _('German (Germany)')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fa', _('Persian')),
    ('fr', _('French')),
    ('hu', _('Hungarian')),
    ('hr', _('Croatian')),
    ('id', _('Indonesian')),
    ('it', _('Italian')),
    ('nl', _('Dutch (Nethherlands)')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('pt-br', _('Portuguese (Brazil)')),
    ('ro', _('Romanian (Romania)')),
    ('ru', _('Russian')),
    ('sl', _('Slovenian')),
    ('tr', _('Turkish')),
    ('vi', _('Vietnamese (Viet Nam)')),
    ('zh-cn', _('Chinese (China)')),
)

SITE_ID = 1

sys.path.append(os.path.join(BASE_DIR, 'mayan', 'apps'))

STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# --------- Django compressor -------------
COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
)
COMPRESS_ENABLED = False
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
# --------- Django -------------------
LOGIN_URL = 'authentication:login_view'
LOGIN_REDIRECT_URL = 'common:home'
INTERNAL_IPS = ('127.0.0.1',)
# -------- LoginRequiredMiddleware ----------
LOGIN_EXEMPT_URLS = (
    r'^favicon\.ico$',
    r'^about\.html$',
    r'^legal/',  # allow the entire /legal/* subsection
    r'^%s-static/' % PROJECT_NAME,

    r'^accounts/register/$',
    r'^accounts/register/complete/$',
    r'^accounts/register/closed/$',

    r'^accounts/activate/complete/',
    r'^accounts/activate/(?P<activation_key>\w+)/$',

    r'^authentication/password/reset/$',
    r'^authentication/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^authentication/password/reset/complete/$',
    r'^authentication/password/reset/done/$',

    r'^api/',
    r'^docs/',
)
# ---------- Django REST framework -----------
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
# --------- Pagination --------
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 8,
    'MARGIN_PAGES_DISPLAYED': 2,
}
# ----------- Celery ----------
CELERY_ACCEPT_CONTENT = ('json',)
CELERY_ALWAYS_EAGER = True
CELERY_CREATE_MISSING_QUEUES = False
CELERY_DISABLE_RATE_LIMITS = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ENABLE_UTC = True
CELERY_QUEUES = []
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ROUTES = {}
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
# ------------ CORS ------------
CORS_ORIGIN_ALLOW_ALL = True
# ------ Django REST Swagger -----
SWAGGER_SETTINGS = {
    'api_version': '1',
    'info': {
          'title': _('Mayan EDMS API Documentation'),
          'description': _('Free Open Source Document Management System.'),
          'contact': 'roberto.rosario@mayan-edms.com',
          'license': 'Apache 2.0',
          'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html'
    }

}
# ------ Timezone --------
TIMEZONE_COOKIE_NAME = 'django_timezone'
TIMEZONE_SESSION_KEY = 'django_timezone'
