from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common import MayanAppConfig, menu_user
from mayan.apps.navigation.classes import Separator

from .links import link_logout, link_password_change

logger = logging.getLogger(__name__)


class AuthenticationApp(MayanAppConfig):
    app_namespace = 'authentication'
    app_url = 'authentication'
    has_tests = True
    name = 'mayan.apps.authentication'
    verbose_name = _('Authentication')

    def ready(self):
        super(AuthenticationApp, self).ready()

        menu_user.bind_links(
            links=(
                Separator(), link_password_change, link_logout
            ), position=99
        )
