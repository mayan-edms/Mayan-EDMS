from __future__ import absolute_import, unicode_literals

import logging
import os
import sys
import traceback
import warnings

from django import apps
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from .classes import Template
from .dependencies import *  # NOQA
from .handlers import (
    handler_pre_initial_setup, handler_pre_upgrade,
    handler_user_locale_profile_session_config, handler_user_locale_profile_create
)
from .links import (
    link_about, link_current_user_locale_profile_edit, link_license,
    link_object_error_list_clear, link_setup, link_tools
)

from .literals import MESSAGE_SQLITE_WARNING
from .menus import menu_about, menu_secondary, menu_topbar, menu_user
from .settings import (
    setting_auto_logging, setting_production_error_log_path,
    setting_production_error_logging
)
from .signals import pre_initial_setup, pre_upgrade
from .tasks import task_delete_stale_uploads  # NOQA - Force task registration
from .utils import check_for_sqlite
from .warnings import DatabaseWarning

logger = logging.getLogger(__name__)


class MayanAppConfig(apps.AppConfig):
    app_namespace = None
    app_url = None

    def ready(self):
        logger.debug('Initializing app: %s', self.name)
        from mayan.urls import urlpatterns as mayan_urlpatterns

        if self.app_url:
            top_url = '{}/'.format(self.app_url)
        elif self.app_url is not None:
            top_url = ''
        else:
            top_url = '{}/'.format(self.name)

        try:
            app_urlpatterns = import_string(
                dotted_path='{}.urls.urlpatterns'.format(self.name)
            )
        except ImportError as exception:
            if force_text(exception) not in ('No module named urls', 'No module named \'{}.urls\''.format(self.name)):
                logger.exception(
                    'Import time error when running AppConfig.ready() of app '
                    '"%s".', self.name
                )
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                raise exception
        else:
            mayan_urlpatterns += (
                url(
                    regex=r'^{}'.format(top_url), view=include(
                        (app_urlpatterns, self.app_namespace or self.name)
                    )
                ),
            )


class CommonApp(MayanAppConfig):
    app_namespace = 'common'
    app_url = ''
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.common'
    verbose_name = _('Common')

    def ready(self):
        super(CommonApp, self).ready()
        if check_for_sqlite():
            warnings.warn(
                category=DatabaseWarning,
                message=force_text(MESSAGE_SQLITE_WARNING)
            )

        Template(
            name='menu_main', template_name='appearance/menu_main.html'
        )
        Template(
            name='menu_topbar', template_name='appearance/menu_topbar.html'
        )

        menu_user.bind_links(
            links=(
                link_current_user_locale_profile_edit,
            ), position=50
        )

        menu_about.bind_links(
            links=(
                link_tools, link_setup, link_about, link_license,
            )
        )

        menu_topbar.bind_links(links=(menu_about, menu_user,), position=99)
        menu_secondary.bind_links(
            links=(link_object_error_list_clear,), sources=(
                'common:object_error_list',
            )
        )

        post_save.connect(
            dispatch_uid='common_handler_user_locale_profile_create',
            receiver=handler_user_locale_profile_create,
            sender=settings.AUTH_USER_MODEL
        )
        pre_initial_setup.connect(
            dispatch_uid='common_handler_pre_initial_setup',
            receiver=handler_pre_initial_setup
        )
        pre_upgrade.connect(
            dispatch_uid='common_handler_pre_upgrade',
            receiver=handler_pre_upgrade
        )

        user_logged_in.connect(
            dispatch_uid='common_handler_user_locale_profile_session_config',
            receiver=handler_user_locale_profile_session_config
        )
        self.setup_auto_logging()

    def setup_auto_logging(self):
        if setting_auto_logging.value:
            if settings.DEBUG:
                level = 'DEBUG'
                handlers = ['console']
            else:
                level = 'ERROR'
                handlers = ['console']

            if os.path.exists(settings.MEDIA_ROOT) and setting_production_error_logging.value:
                handlers.append('logfile')

            loggers = {}
            for project_app in apps.apps.get_app_configs():
                loggers[project_app.name] = {
                    'handlers': handlers,
                    'propagate': True,
                    'level': level,
                }

            logging_configuration = {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'intermediate': {
                        'format': '%(name)s <%(process)d> [%(levelname)s] "%(funcName)s() line %(lineno)d %(message)s"',
                    },
                    'logfile': {
                        'format': '%(asctime)s %(name)s <%(process)d> [%(levelname)s] "%(funcName)s() line %(lineno)d %(message)s"'
                    },
                },
                'handlers': {
                    'console': {
                        'class': 'logging.StreamHandler',
                        'formatter': 'intermediate',
                        'level': 'DEBUG',
                    },
                },
                'loggers': loggers
            }

            if os.path.exists(settings.MEDIA_ROOT) and setting_production_error_logging.value:
                logging_configuration['handlers']['logfile'] = {
                    'backupCount': 3,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': setting_production_error_log_path.value,
                    'formatter': 'logfile',
                    'maxBytes': 1024,
                }

            logging.config.dictConfig(logging_configuration)
