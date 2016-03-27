from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig


class ServerApp(MayanAppConfig):
    name = 'server'
    verbose_name = _('Server')

    def ready(self):
        super(ServerApp, self).ready()
