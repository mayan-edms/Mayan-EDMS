from __future__ import absolute_import, unicode_literals

from datetime import timedelta
import logging

from kombu import Exchange, Queue

from django import apps
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.celery import app

from .handlers import (
    user_locale_profile_session_config, user_locale_profile_create
)
from .links import (
    link_about, link_current_user_details, link_current_user_edit,
    link_current_user_locale_profile_edit, link_filters, link_license,
    link_packages_licenses, link_setup, link_tools
)
from .literals import DELETE_STALE_UPLOADS_INTERVAL
from .menus import menu_facet, menu_main, menu_tools, menu_user
from .licenses import *  # NOQA
from .settings import setting_auto_logging
from .tasks import task_delete_stale_uploads  # NOQA - Force task registration

logger = logging.getLogger(__name__)


class MayanAppConfig(apps.AppConfig):
    app_url = None
    app_namespace = None

    def ready(self):
        from mayan.urls import urlpatterns

        if self.app_url:
            top_url = '{}/'.format(self.app_url)
        elif self.app_url is not None:
            top_url = ''
        else:
            top_url = '{}/'.format(self.name)

        try:
            urlpatterns += url(
                r'^{}'.format(top_url),
                include(
                    '{}.urls'.format(self.name),
                    namespace=self.app_namespace or self.name
                )
            ),
        except ImportError as exception:
            logger.debug(
                'App %s doesn\'t have URLs defined. Exception: %s', self.name,
                exception
            )
            if 'No module named urls' not in unicode(exception):
                logger.error(
                    'Import time error when running AppConfig.ready(). Check '
                    'apps.py, urls.py, views.py, etc.'
                )
                raise exception


class CommonApp(MayanAppConfig):
    app_url = ''
    name = 'common'
    test = True
    verbose_name = _('Common')

    def ready(self):
        super(CommonApp, self).ready()

        app.conf.CELERYBEAT_SCHEDULE.update(
            {
                'task_delete_stale_uploads': {
                    'task': 'common.tasks.task_delete_stale_uploads',
                    'schedule': timedelta(
                        seconds=DELETE_STALE_UPLOADS_INTERVAL
                    ),
                },
            }
        )

        app.conf.CELERY_QUEUES.extend(
            (
                Queue('default', Exchange('default'), routing_key='default'),
                Queue('tools', Exchange('tools'), routing_key='tools'),
                Queue(
                    'common_periodic', Exchange('common_periodic'),
                    routing_key='common_periodic', delivery_mode=1
                ),
            )
        )

        app.conf.CELERY_DEFAULT_QUEUE = 'default'

        app.conf.CELERY_ROUTES.update(
            {
                'common.tasks.task_delete_stale_uploads': {
                    'queue': 'common_periodic'
                },
            }
        )
        from navigation.classes import Separator
        menu_user.bind_links(
            links=(
                link_current_user_details, link_current_user_edit,
                link_current_user_locale_profile_edit, link_tools, link_setup,
                Separator()
            )
        )

        menu_facet.bind_links(
            links=(link_about, link_license, link_packages_licenses),
            sources=(
                'common:about_view', 'common:license_view',
                'common:packages_licenses_view'
            )
        )
        menu_main.bind_links(links=(link_about,), position=99)

        menu_tools.bind_links(
            links=(link_filters,)
        )

        post_save.connect(
            user_locale_profile_create,
            dispatch_uid='user_locale_profile_create',
            sender=settings.AUTH_USER_MODEL
        )
        user_logged_in.connect(
            user_locale_profile_session_config,
            dispatch_uid='user_locale_profile_session_config'
        )
        self.setup_auto_logging()

    def setup_auto_logging(self):
        if setting_auto_logging.value:
            if settings.DEBUG:
                level = 'DEBUG'
            else:
                level = 'INFO'

            loggers = {}
            for project_app in apps.apps.get_app_configs():
                loggers[project_app.name] = {
                    'handlers': ['console'],
                    'propagate': True,
                    'level': level,
                }

            logging.config.dictConfig(
                {
                    'version': 1,
                    'disable_existing_loggers': True,
                    'formatters': {
                        'intermediate': {
                            'format': '%(name)s <%(process)d> [%(levelname)s] "%(funcName)s() %(message)s"'
                        },
                    },
                    'handlers': {
                        'console': {
                            'level': 'DEBUG',
                            'class': 'logging.StreamHandler',
                            'formatter': 'intermediate'
                        }
                    },
                    'loggers': loggers
                }
            )
