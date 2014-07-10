"""
For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


from django.core.exceptions import ImproperlyConfigured


ugettext = lambda s: s

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-3])  # up from mayan/settings/include
SITE_ROOT = BASE_DIR  # for compatibility

_apps_path = os.path.join(BASE_DIR, 'mayan/apps')
if _apps_path not in sys.path:
    sys.path.append(_apps_path)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected/')

try:
    from .secrets import *
except ImportError:
    raise ImproperlyConfigured('You need a secrets.py file - contact aaron.dennis@crossculturalconsult.com')

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Application definition

INSTALLED_APPS = (
    #Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    # 3rd party
    # South
    'south',
    # Others
    'filetransfers',
    'taggit',
    'mptt',
    'compressor',
    'rest_framework',
    # Base generic
    'permissions',
    'project_setup',
    'project_tools',
    'smart_settings',
    'navigation',
    'lock_manager',
    'web_theme',
    # pagination needs to go after web_theme so that the pagination template
    # if found
    'pagination',
    'common',
    'django_gpg',
    'dynamic_search',
    'acls',
    'converter',
    'user_management',
    'mimetype',
    'scheduler',
    'job_processor',
    'installation',
    # Mayan EDMS
    'storage',
    'app_registry',
    'folders',
    'tags',
    'document_comments',
    'metadata',
    'statistics',
    'documents',
    'linking',
    'document_indexing',
    'document_acls',
    'ocr',
    'sources',
    'history',
    'main',
    'rest_api',
    'document_signatures',
    'checkouts',
    'bootstrap',
    'registration',
    # Has to be last so the other apps can register it's signals
    'signaler')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'common.middleware.strip_spaces_widdleware.SpacelessMiddleware',
    'common.middleware.login_required_middleware.LoginRequiredMiddleware',
    'permissions.middleware.permission_denied_middleware.PermissionDeniedMiddleware',
    'pagination.middleware.PaginationMiddleware')

ROOT_URLCONF = 'mayan.urls'

WSGI_APPLICATION = 'mayan.wsgi.application'



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


from django.core.urlresolvers import reverse_lazy

PROJECT_TITLE = 'Mayan CCCS Review'

LANGUAGES = (
    ('ar', ugettext('Arabic')),
    ('bg', ugettext('Bulgarian')),
    ('bs', ugettext('Bosnian (Bosnia and Herzegovina)')),
    ('da', ugettext('Danish')),
    ('de', ugettext('German (Germany)')),
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
    ('fa', ugettext('Persian')),
    ('fr', ugettext('French')),
    ('hu', ugettext('Hungarian')),
    ('hr', ugettext('Croatian')),
    ('id', ugettext('Indonesian')),
    ('it', ugettext('Italian')),
    ('nl', ugettext('Dutch (Nethherlands)')),
    ('pl', ugettext('Polish')),
    ('pt', ugettext('Portuguese')),
    ('pt-br', ugettext('Portuguese (Brazil)')),
    ('ro', ugettext('Romanian (Romania)')),
    ('ru', ugettext('Russian')),
    ('sl', ugettext('Slovenian')),
    ('tr', ugettext('Turkish')),
    ('vi', ugettext('Vietnamese (Viet Nam)')),
)

SITE_ID = 1


ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(PROJECT_ROOT, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# --------- Django compressor -------------
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_ENABLED=False
# ---------- Django sendfile --------------
SENDFILE_BACKEND = 'sendfile.backends.simple'
# --------- Web theme ---------------
WEB_THEME_ENABLE_SCROLL_JS = False
# --------- Django -------------------
LOGIN_URL = reverse_lazy('login_view')
LOGIN_REDIRECT_URL = reverse_lazy('home')
# -------- LoginRequiredMiddleware ----------
LOGIN_EXEMPT_URLS = (
    r'^favicon\.ico$',
    r'^about\.html$',
    r'^legal/',  # allow the entire /legal/* subsection
    r'^static/',

    r'^accounts/register/$',
    r'^accounts/register/complete/$',
    r'^accounts/register/closed/$',

    r'^accounts/activate/complete/',
    r'^accounts/activate/(?P<activation_key>\w+)/$',

    r'^password/reset/$',
    r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^password/reset/complete/$',
    r'^password/reset/done/$',
)
# --------- Pagination ----------------
PAGINATION_INVALID_PAGE_RAISES_404 = True
# ---------- Search ------------------
SEARCH_SHOW_OBJECT_TYPE = False

SERIALIZATION_MODULES = {
    'better_yaml': 'common.serializers.better_yaml',
}
# --------- Taggit ------------
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}
# ---------- Django REST framework -----------
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
}
