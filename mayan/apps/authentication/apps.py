from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_multi_item, menu_object, menu_user
from mayan.apps.navigation.classes import Separator

from .links import (
    link_logout, link_password_change, link_user_multiple_set_password,
    link_user_set_password
)

logger = logging.getLogger(__name__)


class AuthenticationApp(MayanAppConfig):
    app_namespace = 'authentication'
    app_url = 'authentication'
    has_tests = True
    name = 'mayan.apps.authentication'
    verbose_name = _('Authentication')

    def ready(self):
        super(AuthenticationApp, self).ready()

        User = get_user_model()

        menu_multi_item.bind_links(
            links=(link_user_multiple_set_password,),
            sources=('user_management:user_list',)
        )

        menu_object.bind_links(
            links=(link_user_set_password,), sources=(User,)
        )

        menu_user.bind_links(
            links=(
                Separator(), link_password_change, link_logout
            ), position=99
        )
