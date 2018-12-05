from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common import MayanAppConfig

from .licenses import *  # NOQA


class AppearanceApp(MayanAppConfig):
    name = 'mayan.apps.appearance'
    verbose_name = _('Appearance')

    def ready(self):
        super(AppearanceApp, self).ready()
