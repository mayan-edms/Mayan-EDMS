import os
import sys

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.utils import SettingNamespaceSingleton

from .literals import DEFAULT_SECRET_KEY, SECRET_KEY_FILENAME, SYSTEM_DIR

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

setting_namespace = SettingNamespaceSingleton(global_symbol_table=globals())
if 'revertsettings' in sys.argv:
    setting_namespace.update_globals(only_critical=True)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(MEDIA_ROOT, 'db.sqlite3')  # NOQA: F821
        }
    }
else:
    setting_namespace.update_globals()

# SECURITY WARNING: keep the secret key used in production secret!
environment_secret_key = os.environ.get('MAYAN_SECRET_KEY')
if environment_secret_key:
    SECRET_KEY = environment_secret_key
else:
    SECRET_KEY_PATH = os.path.join(MEDIA_ROOT, SYSTEM_DIR, SECRET_KEY_FILENAME)
    try:
        with open(file=SECRET_KEY_PATH) as file_object:  # NOQA: F821
            SECRET_KEY = file_object.read().strip()
    except IOError:
        SECRET_KEY = DEFAULT_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!

# Application definition

INSTALLED_APPS = (
    # Placed at the top so it can override any template
    'mayan.apps.appearance',
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.forms',
    # Allow using WhiteNoise in development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # 3rd party
    'actstream',
    'colorful',
    'corsheaders',
    'django_celery_beat',
    'formtools',
    'mathfilters',
    'mptt',
    'pure_pagination',
    'rest_framework',
    'rest_framework.authtoken',
    'solo',
    'stronghold',
    'widget_tweaks',
    # Base apps
    # Moved to the top to ensure Mayan app logging is initialized and
    # available as soon as possible.
    'mayan.apps.logging',
    # Task manager goes to the top to ensure all queues are created before any
    # other app tries to use them.
    'mayan.apps.task_manager',
    'mayan.apps.acls',
    'mayan.apps.authentication',
    'mayan.apps.autoadmin',
    'mayan.apps.common',
    'mayan.apps.converter',
    'mayan.apps.dashboards',
    'mayan.apps.dependencies',
    'mayan.apps.django_gpg',
    'mayan.apps.dynamic_search',
    'mayan.apps.events',
    'mayan.apps.file_caching',
    'mayan.apps.locales',
    'mayan.apps.lock_manager',
    'mayan.apps.messaging',
    'mayan.apps.mimetype',
    'mayan.apps.navigation',
    'mayan.apps.organizations',
    'mayan.apps.permissions',
    'mayan.apps.platform',
    'mayan.apps.quotas',
    'mayan.apps.rest_api',
    'mayan.apps.smart_settings',
    'mayan.apps.storage',
    'mayan.apps.templating',
    'mayan.apps.testing',
    'mayan.apps.user_management',
    'mayan.apps.views',
    # Project apps
    'mayan.apps.announcements',
    'mayan.apps.motd',
    # Document apps
    'mayan.apps.cabinets',
    'mayan.apps.checkouts',
    'mayan.apps.document_comments',
    'mayan.apps.document_indexing',
    'mayan.apps.document_parsing',
    'mayan.apps.document_signatures',
    'mayan.apps.document_states',
    'mayan.apps.documents',
    'mayan.apps.duplicates',
    'mayan.apps.file_metadata',
    'mayan.apps.linking',
    'mayan.apps.mailer',
    'mayan.apps.mayan_statistics',
    'mayan.apps.metadata',
    'mayan.apps.mirroring',
    'mayan.apps.ocr',
    'mayan.apps.redactions',
    'mayan.apps.sources',
    'mayan.apps.tags',
    'mayan.apps.web_links',
    # Placed after rest_api to allow template overriding
    'drf_yasg'
)

MIDDLEWARE = (
    'mayan.apps.logging.middleware.error_logging.ErrorLoggingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mayan.apps.authentication.middleware.impersonate.ImpersonateMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'mayan.apps.locales.middleware.timezone.TimezoneMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
    'mayan.apps.common.middleware.ajax_redirect.AjaxRedirect'
)

ROOT_URLCONF = 'mayan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        }
    }
]

WSGI_APPLICATION = 'mayan.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    }
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# ------------ Custom settings section ----------

LANGUAGES = (
    ('ar', _('Arabic')),
    ('bg', _('Bulgarian')),
    ('bs', _('Bosnian')),
    ('cs', _('Czech')),
    ('da', _('Danish')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fa', _('Persian')),
    ('fr', _('French')),
    ('hu', _('Hungarian')),
    ('id', _('Indonesian')),
    ('it', _('Italian')),
    ('lv', _('Latvian')),
    ('nl', _('Dutch')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('pt-br', _('Portuguese (Brazil)')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sl', _('Slovenian')),
    ('tr', _('Turkish')),
    ('vi', _('Vietnamese')),
    ('zh-hans', _('Chinese (Simplified)'))
)

SITE_ID = 1

STATIC_ROOT = os.environ.get(
    'MAYAN_STATIC_ROOT', os.path.join(MEDIA_ROOT, 'static')  # NOQA: F821
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'mayan.apps.views.finders.MayanAppDirectoriesFinder'
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEST_RUNNER = 'mayan.apps.testing.runner.MayanTestRunner'

# ---------- Django REST framework -----------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'mayan.apps.rest_api.pagination.MayanPageNumberPagination'
}

# --------- Pagination --------

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 5,
    'MARGIN_PAGES_DISPLAYED': 2
}

# ----------- Celery ----------

CELERY_ACCEPT_CONTENT = ('json',)
CELERY_BEAT_SCHEDULE = {}
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ENABLE_UTC = True
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_TASK_DEFAULT_QUEUE = 'celery'
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_QUEUES = []
CELERY_TASK_ROUTES = {}
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# ------------ CORS ------------

CORS_ORIGIN_ALLOW_ALL = True

# ------ Timezone --------

TIMEZONE_COOKIE_NAME = 'django_timezone'
TIMEZONE_SESSION_KEY = 'django_timezone'

# ----- Stronghold -------

STRONGHOLD_PUBLIC_URLS = (r'^/favicon\.ico$',)

# ----- Swagger --------

SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'rest_api.schemas.openapi_info',
    'DEFAULT_MODEL_DEPTH': 1,
    'DOC_EXPANSION': 'None'
}

# ----- AJAX REDIRECT -----

AJAX_REDIRECT_CODE = 278

# ------ End -----

BASE_INSTALLED_APPS = INSTALLED_APPS

for app in INSTALLED_APPS:
    if 'mayan.apps.{}'.format(app) in BASE_INSTALLED_APPS:
        raise ImproperlyConfigured(
            'Update the app references in the file config.yml as detailed '
            'in https://docs.mayan-edms.com/releases/3.2.html#backward-incompatible-changes'
        )

for APP in (COMMON_EXTRA_APPS or ()):  # NOQA: F821
    INSTALLED_APPS = INSTALLED_APPS + (APP,)


INSTALLED_APPS = [
    APP for APP in INSTALLED_APPS if APP not in (COMMON_DISABLED_APPS or ())  # NOQA: F821
]

if not DATABASES:
    if DATABASE_ENGINE:  # NOQA: F821
        DATABASES = {
            'default': {
                'ENGINE': DATABASE_ENGINE,  # NOQA: F821
                'NAME': DATABASE_NAME,  # NOQA: F821
                'USER': DATABASE_USER,  # NOQA: F821
                'PASSWORD': DATABASE_PASSWORD,  # NOQA: F821
                'HOST': DATABASE_HOST,  # NOQA: F821
                'PORT': DATABASE_PORT,  # NOQA: F821
                'CONN_MAX_AGE': DATABASE_CONN_MAX_AGE  # NOQA: F821
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(MEDIA_ROOT, 'db.sqlite3')  # NOQA: F821
            }
        }
