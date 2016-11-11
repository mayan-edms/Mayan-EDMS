from __future__ import absolute_import, unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_user

from .links import link_logout, link_password_change

logger = logging.getLogger(__name__)


class AuthenticationApp(MayanAppConfig):
    name = 'authentication'
    test = True
    verbose_name = _('Authentication')

    def ready(self):
        super(AuthenticationApp, self).ready()

        menu_user.bind_links(
            links=(
                link_password_change, link_logout
            ), position=99
        )
