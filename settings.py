# Django settings for mayan project.
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))

sys.path.append(os.path.join(PROJECT_ROOT, 'modules'))
sys.path.append(os.path.join(PROJECT_ROOT, 'customization_apps'))
sys.path.append(os.path.join(PROJECT_ROOT, 'apps'))
sys.path.append(os.path.join(PROJECT_ROOT, 'shared_apps'))
sys.path.append(os.path.join(PROJECT_ROOT, '3rd_party_apps'))

PROJECT_TITLE = 'Mayan'
PROJECT_NAME = 'mayan'

DEBUG = False
DEVELOPMENT = False
TEMPLATE_DEBUG = True

ADMINS = ()
SENTRY_ADMINS = ('root@localhost',)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, '%s.sqlite' % PROJECT_NAME),     # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Puerto_Rico'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en'

ugettext = lambda s: s

LANGUAGES = (
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/%s-site_media/' % PROJECT_NAME

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'grappelli/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'om^a(i8^6&h+umbd2%pt91cj!qu_@oztw117rgxmn(n2lp^*c!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.login_required_middleware.LoginRequiredMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'web_theme',
    'main',
    'common',
    'documents',
    'pagination',
    'dynamic_search',
    'filetransfers',
    'converter',
    'ocr',
    'permissions',
    'djcelery',
    'indexer',
    'paging',
    'sentry',
    'sentry.client',
    'sentry.client.celery',
    'filesystem_serving',
    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'grappelli.context_processors.admin_template_path',
#    'django.contrib.messages.context_processors.messages',
)

#===== Configuration options ===============
#--------- Grappelli ----------------
#GRAPPELLI_ADMIN_TITLE = PROJECT_TITLE
#--------- Django -------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
#-------- LoginRequiredMiddleware ----------
LOGIN_EXEMPT_URLS = (
    r'^favicon\.ico$',
    r'^about\.html$',
    r'^legal/', # allow the entire /legal/* subsection
    r'^%s-site_media/' % PROJECT_NAME,

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
#--------- Pagination ------------------
#PAGINATION_DEFAULT_PAGINATION = 10
#--------- Web theme app ---------------
#WEB_THEME = 'default'
#---------- Documents ------------------
# Definition
#DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS = {}
#DOCUMENTS_METADATA_AVAILABLE_MODELS = {}

# Upload
#DOCUMENTS_USE_STAGING_DIRECTORY = False
#DOCUMENTS_STAGING_DIRECTORY = u'/tmp/mayan/staging'
#DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD = False
#DOCUMENTS_STAGING_FILES_PREVIEW_SIZE = '640x480'
#DOCUMENTS_AUTOMATIC_OCR = False
#DOCUMENTS_ENABLE_SINGLE_DOCUMENT_UPLOAD = True
#DOCUMENTS_UNCOMPRESS_COMPRESSED_LOCAL_FILES = True
#DOCUMENTS_UNCOMPRESS_COMPRESSED_STAGING_FILES = True

# Saving
#DOCUMENTS_CHECKSUM_FUNCTION = lambda x: hashlib.sha256(x).hexdigest())
#DOCUMENTS_UUID_FUNCTION = lambda:unicode(uuid.uuid4())
#DOCUMENTS_DEFAULT_TRANSFORMATIONS = []

# Storage
#DOCUMENTS_STORAGE_DIRECTORY_NAME = 'documents'
#DOCUMENTS_STORAGE_BACKEND = DocumentStorage

# Usage
#DOCUMENTS_PREVIEW_SIZE = '640x480'
#DOCUMENTS_THUMBNAIL_SIZE = '50x50'
#DOCUMENTS_DISPLAY_SIZE = '1200'
#DOCUMENTS_MULTIPAGE_PREVIEW_SIZE = '160x120'
#DOCUMENTS_AVAILABLE_TRANSFORMATIONS = {}
#example: DOCUMENTS_DEFAULT_TRANSFORMATIONS = [{'name':'rotate', 'arguments':"{'degrees':270}"}]

# Groups
#DOCUMENTS_GROUP_MAX_RESULTS = 20
#DOCUMENTS_GROUP_SHOW_EMPTY = True

# Serving
#FILESYSTEM_FILESERVING_ENABLE = True
#FILESYSTEM_FILESERVING_PATH = u'/tmp/mayan/documents'
#FILESYSTEM_SLUGIFY_PATHS = False
#FILESYSTEM_MAX_RENAME_COUNT = 200

# Misc
#COMMON_TEMPORARY_DIRECTORY = u'/tmp'

# Converter
#CONVERTER_DEFAULT_OPTIONS = u''
#CONVERTER_LOW_QUALITY_OPTIONS = u''
#CONVERTER_HIGH_QUALITY_OPTIONS =  u'-density 400'
#CONVERTER_CONVERT_PATH = u'/usr/bin/convert'
#CONVERTER_OCR_OPTIONS = u'-colorspace Gray -depth 8 -resample 200x200'
#CONVERTER_IDENTIFY_PATH = u'/usr/bin/identify'
#CONVERTER_UNPAPER_PATH = u'/usr/bin/unpaper'

# OCR
#OCR_TESSERACT_PATH = u'/usr/bin/tesseract'
#OCR_MAX_CONCURRENT_EXECUTION = 2
#OCR_TESSERACT_LANGUAGE = None


# Permissions
#ROLES_DEFAULT_ROLES = []

# Override
SEARCH_SHOW_OBJECT_TYPE = False
#----------- django-celery --------------
import djcelery
djcelery.setup_loader()
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"
CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'
#======== End of configuration options =======

try:
    from settings_local import *
except ImportError:
    pass


if DEVELOPMENT:
    INTERNAL_IPS = ('127.0.0.1',)

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
    try:
        import rosetta
        INSTALLED_APPS += ('rosetta',)
    except ImportError:
        #print 'rosetta is not installed'
        pass

    try:
        import django_extensions
        INSTALLED_APPS +=('django_extensions',)
    except ImportError:
        #print 'django_extensions is not installed'
        pass

    try:
        import debug_toolbar
        #INSTALLED_APPS.append('debug_toolbar')
    except ImportError:
        #print 'debug_toolbar is not installed'
        pass

    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)

    WSGI_AUTO_RELOAD = True
    if 'debug_toolbar' in INSTALLED_APPS:
        MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
        DEBUG_TOOLBAR_CONFIG={
            'INTERCEPT_REDIRECTS' : False,
        }
