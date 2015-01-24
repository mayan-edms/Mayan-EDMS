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
SECRET_KEY = 'om^a(i8^6&h+umbd2%pt91cj!qu_@oztw117rgxmn(n2lp^*c!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
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
    'compressor',
    'corsheaders',
    'djcelery',
    'filetransfers',
    'mptt',
    'rest_framework',
    'rest_framework.authtoken',
    'solo',
    'south',
    # Base generic
    'acls',
    'common',
    'converter',
    'django_gpg',
    'dynamic_search',
    'lock_manager',
    'mimetype',
    'navigation',
    'permissions',
    'project_setup',
    'project_tools',
    'smart_settings',
    'user_management',
    # Mayan EDMS
    'checkouts',
    'document_acls',
    'document_comments',
    'document_indexing',
    'document_signatures',
    'document_states',
    'documents',
    'events',
    'folders',
    'history',
    'installation',
    'linking',
    'mailer',
    'main',
    'metadata',
    'ocr',
    'registration',
    'rest_api',
    'sources',
    'statistics',
    'storage',
    'tags',
    # Placed after rest_api to allow template overriding
    'rest_framework_swagger',
    # Must be last on Django < 1.7 as per documentation
    # https://django-activity-stream.readthedocs.org/en/latest/installation.html
    'actstream',
    # Pagination app must go after the main app so that the main app can
    # override the default pagination template
    'pagination',
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
    'common.middleware.login_required_middleware.LoginRequiredMiddleware',
    'permissions.middleware.permission_denied_middleware.PermissionDeniedMiddleware',
    'pagination.middleware.PaginationMiddleware',
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

# Custom settings section

PROJECT_TITLE = 'Mayan EDMS'
PROJECT_NAME = 'mayan'

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

STATIC_URL = '/static/'

# Custom settings section

sys.path.append(os.path.join(BASE_DIR, 'mayan', 'apps'))

STATIC_ROOT = os.path.join(BASE_DIR, 'mayan', 'media', 'static')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
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
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',
                        'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_ENABLED = False
# ---------- Django sendfile --------------
SENDFILE_BACKEND = 'sendfile.backends.simple'
# --------- Web theme ---------------
WEB_THEME_ENABLE_SCROLL_JS = False
# --------- Django -------------------
LOGIN_URL = 'common:login_view'
LOGIN_REDIRECT_URL = 'main:home'
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

    r'^password/reset/$',
    r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^password/reset/complete/$',
    r'^password/reset/done/$',

    r'^api/',
)
# --------- Pagination ----------------
PAGINATION_INVALID_PAGE_RAISES_404 = True
# ---------- Search ------------------
SEARCH_SHOW_OBJECT_TYPE = False
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
# ----------- Celery ----------
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
# ------------ CORS ------------
CORS_ORIGIN_ALLOW_ALL = True
# ------ Django REST Swagger -----
SWAGGER_SETTINGS = {
    'api_version': '0',  # Specify your API's version
}
