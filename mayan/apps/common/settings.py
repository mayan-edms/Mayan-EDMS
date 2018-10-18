from __future__ import unicode_literals

import os
import tempfile

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import mayan
from smart_settings import Namespace

namespace = Namespace(name='common', label=_('Common'))

setting_auto_logging = namespace.add_setting(
    global_name='COMMON_AUTO_LOGGING',
    default=True,
    help_text=_('Automatically enable logging to all apps.')
)
settings_db_sync_task_delay = namespace.add_setting(
    global_name='COMMON_DB_SYNC_TASK_DELAY',
    default=2,
    help_text=_(
        'Time to delay background tasks that depend on a database commit to '
        'propagate.'
    )
)
setting_paginate_by = namespace.add_setting(
    global_name='COMMON_PAGINATE_BY',
    default=40,
    help_text=_(
        'An integer specifying how many objects should be displayed per page.'
    )
)
setting_production_error_logging = namespace.add_setting(
    global_name='COMMON_PRODUCTION_ERROR_LOGGING',
    default=False,
    help_text=_(
        'Enable error logging outside of the system error logging '
        'capabilities.'
    )
)
setting_production_error_log_path = namespace.add_setting(
    global_name='COMMON_PRODUCTION_ERROR_LOG_PATH',
    default=os.path.join(settings.MEDIA_ROOT, 'error.log'), help_text=_(
        'Path to the logfile that will track errors during production.'
    ),
    is_path=True
)
setting_project_title = namespace.add_setting(
    global_name='COMMON_PROJECT_TITLE',
    default=mayan.__title__, help_text=_(
        'Name to be displayed in the main menu.'
    ),
)
setting_project_url = namespace.add_setting(
    global_name='COMMON_PROJECT_URL',
    default=mayan.__website__, help_text=_(
        'URL of the installation or homepage of the project.'
    ),
)
setting_shared_storage = namespace.add_setting(
    global_name='COMMON_SHARED_STORAGE',
    default='django.core.files.storage.FileSystemStorage',
    help_text=_('A storage backend that all workers can use to share files.')
)
setting_shared_storage_arguments = namespace.add_setting(
    global_name='COMMON_SHARED_STORAGE_ARGUMENTS',
    default='{{location: {}}}'.format(
        os.path.join(settings.MEDIA_ROOT, 'shared_files')
    ), quoted=True
)
setting_temporary_directory = namespace.add_setting(
    global_name='COMMON_TEMPORARY_DIRECTORY', default=tempfile.gettempdir(),
    help_text=_(
        'Temporary directory used site wide to store thumbnails, previews '
        'and temporary files.'
    ),
    is_path=True
)

namespace = Namespace(name='django', label=_('Django'))

setting_django_allowed_hosts = namespace.add_setting(
    global_name='ALLOWED_HOSTS', default=settings.ALLOWED_HOSTS,
    help_text=_(
        'A list of strings representing the host/domain names that this site '
        'can serve. This is a security measure to prevent HTTP Host header '
        'attacks, which are possible even under many seemingly-safe web '
        'server configurations. Values in this list can be '
        'fully qualified names (e.g. \'www.example.com\'), in which case '
        'they will be matched against the request\'s Host header exactly '
        '(case-insensitive, not including port). A value beginning with a '
        'period can be used as a subdomain wildcard: \'.example.com\' will '
        'match example.com, www.example.com, and any other subdomain of '
        'example.com. A value of \'*\' will match anything; in this case you '
        'are responsible to provide your own validation of the Host header '
        '(perhaps in a middleware; if so this middleware must be listed '
        'first in MIDDLEWARE).'
    ),
)
setting_django_append_slash = namespace.add_setting(
    global_name='APPEND_SLASH', default=settings.APPEND_SLASH,
    help_text=_(
        'When set to True, if the request URL does not match any of the '
        'patterns in the URLconf and it doesn\'t end in a slash, an HTTP '
        'redirect is issued to the same URL with a slash appended. Note '
        'that the redirect may cause any data submitted in a POST request '
        'to be lost. The APPEND_SLASH setting is only used if '
        'CommonMiddleware is installed (see Middleware). See also '
        'PREPEND_WWW.'
    )
)
setting_django_databases = namespace.add_setting(
    global_name='DATABASES', default=settings.DATABASES,
    help_text=_(
        'A dictionary containing the settings for all databases to be used '
        'with Django. It is a nested dictionary whose contents map a '
        'database alias to a dictionary containing the options for an '
        'individual database. The DATABASES setting must configure a '
        'default database; any number of additional databases may also '
        'be specified.'
    ),
)
setting_django_data_upload_max_memory_size = namespace.add_setting(
    global_name='DATA_UPLOAD_MAX_MEMORY_SIZE',
    default=settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
    help_text=_(
        'Default: 2621440 (i.e. 2.5 MB). The maximum size in bytes that a '
        'request body may be before a SuspiciousOperation '
        '(RequestDataTooBig) is raised. The check is done when accessing '
        'request.body or request.POST and is calculated against the total '
        'request size excluding any file upload data. You can set this to '
        'None to disable the check. Applications that are expected to '
        'receive unusually large form posts should tune this setting. The '
        'amount of request data is correlated to the amount of memory '
        'needed to process the request and populate the GET and POST '
        'dictionaries. Large requests could be used as a '
        'denial-of-service attack vector if left unchecked. Since web '
        'servers don\'t typically perform deep request inspection, it\'s '
        'not possible to perform a similar check at that level. See also '
        'FILE_UPLOAD_MAX_MEMORY_SIZE.'
    ),
)
setting_django_disallowed_user_agents = namespace.add_setting(
    global_name='DISALLOWED_USER_AGENTS',
    default=settings.DISALLOWED_USER_AGENTS,
    help_text=_(
        'Default: [] (Empty list). List of compiled regular expression '
        'objects representing User-Agent strings that are not allowed to '
        'visit any page, systemwide. Use this for bad robots/crawlers. '
        'This is only used if CommonMiddleware is installed '
        '(see Middleware).'
    ),
)
setting_django_email_backend = namespace.add_setting(
    global_name='EMAIL_BACKEND',
    default=settings.EMAIL_BACKEND,
    help_text=_(
        'Default: \'django.core.mail.backends.smtp.EmailBackend\'. The '
        'backend to use for sending emails.'
    ),
)
setting_django_email_host = namespace.add_setting(
    global_name='EMAIL_HOST',
    default=settings.EMAIL_HOST,
    help_text=_(
        'Default: \'localhost\'. The host to use for sending email.'
    ),
)
setting_django_email_host_password = namespace.add_setting(
    global_name='EMAIL_HOST_PASSWORD',
    default=settings.EMAIL_HOST_PASSWORD,
    help_text=_(
        'Default: \'\' (Empty string). Password to use for the SMTP '
        'server defined in EMAIL_HOST. This setting is used in '
        'conjunction with EMAIL_HOST_USER when authenticating to the '
        'SMTP server. If either of these settings is empty, '
        'Django won\'t attempt authentication.'
    ),
)
setting_django_email_host_user = namespace.add_setting(
    global_name='EMAIL_HOST_USER',
    default=settings.EMAIL_HOST_USER,
    help_text=_(
        'Default: \'\' (Empty string). Username to use for the SMTP '
        'server defined in EMAIL_HOST. If empty, Django won\'t attempt '
        'authentication.'
    ),
)
setting_django_email_port = namespace.add_setting(
    global_name='EMAIL_PORT',
    default=settings.EMAIL_PORT,
    help_text=_(
        'Default: 25. Port to use for the SMTP server defined in EMAIL_HOST.'
    ),
)
setting_django_email_user_tls = namespace.add_setting(
    global_name='EMAIL_USE_TLS',
    default=settings.EMAIL_USE_TLS,
    help_text=_(
        'Default: False. Whether to use a TLS (secure) connection when '
        'talking to the SMTP server. This is used for explicit TLS '
        'connections, generally on port 587. If you are experiencing '
        'hanging connections, see the implicit TLS setting EMAIL_USE_SSL.'
    ),
)
setting_django_email_user_ssl = namespace.add_setting(
    global_name='EMAIL_USE_SSL',
    default=settings.EMAIL_USE_SSL,
    help_text=_(
        'Default: False. Whether to use an implicit TLS (secure) connection '
        'when talking to the SMTP server. In most email documentation this '
        'type of TLS connection is referred to as SSL. It is generally used '
        'on port 465. If you are experiencing problems, see the explicit '
        'TLS setting EMAIL_USE_TLS. Note that EMAIL_USE_TLS/EMAIL_USE_SSL '
        'are mutually exclusive, so only set one of those settings to True.'
    ),
)
setting_django_email_timeout = namespace.add_setting(
    global_name='EMAIL_TIMEOUT',
    default=settings.EMAIL_TIMEOUT,
    help_text=_(
        'Default: None. Specifies a timeout in seconds for blocking '
        'operations like the connection attempt.'
    ),
)
setting_django_file_upload_max_memory_size = namespace.add_setting(
    global_name='FILE_UPLOAD_MAX_MEMORY_SIZE',
    default=settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
    help_text=_(
        'Default: 2621440 (i.e. 2.5 MB). The maximum size (in bytes) '
        'that an upload will be before it gets streamed to the file '
        'system. See Managing files for details. See also '
        'DATA_UPLOAD_MAX_MEMORY_SIZE.'
    ),
)
# Not really a Django setting, but since it is flat and defined in setting.py
# We need to put it here.
setting_home_view = namespace.add_setting(
    global_name='HOME_VIEW',
    default=settings.HOME_VIEW, help_text=_(
        'Name of the view attached to the branch anchor in the main menu.'
    ),
)
setting_django_installed_apps = namespace.add_setting(
    global_name='INSTALLED_APPS',
    default=settings.INSTALLED_APPS,
    help_text=_(
        'A list of strings designating all applications that are enabled '
        'in this Django installation. Each string should be a dotted '
        'Python path to: an application configuration class (preferred), '
        'or a package containing an application.'
    ),
)
setting_django_login_url = namespace.add_setting(
    global_name='LOGIN_URL',
    default=settings.LOGIN_URL,
    help_text=_(
        'Default: \'/accounts/login/\' The URL where requests are '
        'redirected for login, especially when using the login_required() '
        'decorator. This setting also accepts named URL patterns which '
        'can be used to reduce configuration duplication since you '
        'don\'t have to define the URL in two places (settings '
        'and URLconf).'
    )
)
setting_django_login_redirect_url = namespace.add_setting(
    global_name='LOGIN_REDIRECT_URL',
    default=settings.LOGIN_REDIRECT_URL,
    help_text=_(
        'Default: \'/accounts/profile/\' The URL where requests are '
        'redirected after login when the contrib.auth.login view gets no '
        'next parameter. This is used by the login_required() decorator, '
        'for example. This setting also accepts named URL patterns which '
        'can be used to reduce configuration duplication since you don\'t '
        'have to define the URL in two places (settings and URLconf).'
    ),
)

namespace = Namespace(name='celery', label=_('Celery'))

setting_celery_broker_url = namespace.add_setting(
    global_name='BROKER_URL', default=settings.BROKER_URL,
    help_text=_(
        'Default: "amqp://". Default broker URL. This must be a URL in '
        'the form of: transport://userid:password@hostname:port/virtual_host '
        'Only the scheme part (transport://) is required, the rest is '
        'optional, and defaults to the specific transports default values.'
    ),
)
setting_celery_result_backend = namespace.add_setting(
    global_name='CELERY_RESULT_BACKEND',
    default=settings.CELERY_RESULT_BACKEND,
    help_text=_(
        'Default: No result backend enabled by default. The backend used '
        'to store task results (tombstones). Refer to '
        'http://docs.celeryproject.org/en/v4.1.0/userguide/configuration.'
        'html#result-backend'
    )
)
