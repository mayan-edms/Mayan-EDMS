import logging
import sys
import traceback
import warnings

from django import apps
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.db.utils import OperationalError
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.logging.mixins import LoggingAppConfigMixin
from mayan.apps.templating.classes import AJAXTemplate

from .handlers import handler_pre_initial_setup, handler_pre_upgrade
from .links import (
    link_about, link_book, link_license, link_setup, link_store,
    link_support, link_tools
)
from .literals import MESSAGE_SQLITE_WARNING
from .menus import menu_about, menu_secondary, menu_topbar, menu_user
from .patches import patchDjangoTranslation
from .settings import (
    setting_auto_logging, setting_production_error_log_path,
    setting_production_error_logging, setting_url_base_path
)
from .signals import (
    signal_database_ready, signal_pre_initial_setup, signal_pre_upgrade
)
from .tasks import task_delete_stale_uploads  # NOQA - Force task registration
from .utils import check_for_sqlite
from .warnings import DatabaseWarning

logger = logging.getLogger(name=__name__)


class MayanAppConfig(apps.AppConfig):
    app_namespace = None
    app_url = None

    @staticmethod
    def _get_mayan_apps():
        return [
            app for app in apps.apps.get_app_configs() if isinstance(app, MayanAppConfig)
        ]

    @staticmethod
    def _are_apps_ready():
        return all(
            [
                getattr(
                    app, 'app_ready', False
                ) for app in MayanAppConfig._get_mayan_apps()
            ]
        )

    def ready(self):
        logger.debug('Initializing app: %s', self.name)
        from mayan.urls import urlpatterns as mayan_urlpatterns

        installation_base_url = setting_url_base_path.value
        if installation_base_url:
            installation_base_url = '{}/'.format(installation_base_url)
        else:
            installation_base_url = ''

        if self.app_url:
            top_url = '{installation_base_url}{app_urls}/'.format(
                installation_base_url=installation_base_url,
                app_urls=self.app_url
            )
        elif self.app_url is not None:
            # When using app_url as '' to register a top of URL view.
            top_url = installation_base_url
        else:
            # If app_url is None, use the app's name for the URL base.
            top_url = '{installation_base_url}{app_name}/'.format(
                installation_base_url=installation_base_url,
                app_name=self.name
            )

        try:
            app_urlpatterns = import_string(
                dotted_path='{}.urls.urlpatterns'.format(self.name)
            )
        except ImportError as exception:
            non_critical_error_list = (
                'No module named urls',
                'No module named \'{}.urls\''.format(self.name),
                'Module "{}.urls" does not define a "urlpatterns" attribute/class'.format(self.name),
            )
            if force_text(s=exception) not in non_critical_error_list:
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
        self.app_ready = True

        if MayanAppConfig._are_apps_ready():
            SharedUploadedFile = apps.apps.get_model(
                app_label='contenttypes', model_name='ContentType'
            )
            try:
                SharedUploadedFile.objects.first()
            except OperationalError:
                """Expected when the database is not yet ready"""
            #else:
            #    signal_database_ready.send(sender=self)

        try:
            passthru_urlpatterns = import_string(
                dotted_path='{}.urls.passthru_urlpatterns'.format(self.name)
            )
        except ImportError as exception:
            non_critical_error_list = (
                'No module named urls',
                'No module named \'{}.urls\''.format(self.name),
                'Module "{}.urls" does not define a "passthru_urlpatterns" attribute/class'.format(self.name),
            )
            if force_text(s=exception) not in non_critical_error_list:
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
                        (passthru_urlpatterns)
                    )
                ),
            )


class CommonApp(LoggingAppConfigMixin, MayanAppConfig):
    app_namespace = 'common'
    app_url = ''
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.common'
    static_media_ignore_patterns = (
        'mptt/*',
    )
    verbose_name = _('Common')

    def ready(self):
        super().ready()

        admin.autodiscover()

        if check_for_sqlite():
            warnings.warn(
                category=DatabaseWarning,
                message=force_text(s=MESSAGE_SQLITE_WARNING)
            )

        AJAXTemplate(
            name='menu_main', template_name='appearance/menu_main.html'
        )
        AJAXTemplate(
            name='menu_topbar', template_name='appearance/menu_topbar.html'
        )

        menu_about.bind_links(
            links=(
                link_tools, link_setup, link_about, link_book, link_store,
                link_support, link_license,
            )
        )

        menu_topbar.bind_links(links=(menu_about, menu_user,), position=99)

        signal_pre_initial_setup.connect(
            dispatch_uid='common_handler_pre_initial_setup',
            receiver=handler_pre_initial_setup
        )
        signal_pre_upgrade.connect(
            dispatch_uid='common_handler_pre_upgrade',
            receiver=handler_pre_upgrade
        )
