from __future__ import absolute_import, unicode_literals

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
    link_current_user_locale_profile_details,
    link_current_user_locale_profile_edit, link_license, link_setup, link_tools
)
from .menus import menu_facet, menu_main, menu_secondary

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

        urlpatterns += url(
            r'^{}'.format(top_url),
            include(
                '{}.urls'.format(self.name),
                namespace=self.app_namespace or self.name
            )
        ),


class CommonApp(MayanAppConfig):
    app_url = ''
    name = 'common'
    verbose_name = _('Common')

    def ready(self):
        super(CommonApp, self).ready()

        app.conf.CELERY_QUEUES.extend(
            (
                Queue('default', Exchange('default'), routing_key='default'),
                Queue('tools', Exchange('tools'), routing_key='tools'),
            )
        )

        app.conf.CELERY_DEFAULT_QUEUE = 'default'

        menu_facet.bind_links(
            links=(
                link_current_user_details,
                link_current_user_locale_profile_details, link_tools,
                link_setup
            ), sources=(
                'common:current_user_details', 'common:current_user_edit',
                'common:current_user_locale_profile_details',
                'common:current_user_locale_profile_edit',
                'authentication:password_change_view', 'common:setup_list',
                'common:tools_list'
            )
        )
        menu_main.bind_links(links=[link_about], position=-1)
        menu_secondary.bind_links(
            links=(link_about, link_license),
            sources=('common:about_view', 'common:license_view')
        )
        menu_secondary.bind_links(
            links=(
                link_current_user_edit, link_current_user_locale_profile_edit
            ),
            sources=(
                'common:current_user_details', 'common:current_user_edit',
                'common:current_user_locale_profile_details',
                'common:current_user_locale_profile_edit',
                'authentication:password_change_view', 'common:setup_list',
                'common:tools_list'
            )
        )
        user_logged_in.connect(
            user_locale_profile_session_config,
            dispatch_uid='user_locale_profile_session_config'
        )
        post_save.connect(
            user_locale_profile_create,
            dispatch_uid='user_locale_profile_create',
            sender=settings.AUTH_USER_MODEL
        )
