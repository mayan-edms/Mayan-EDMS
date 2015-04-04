from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_setup

from .links import link_check_settings


class SmartSettingsApp(apps.AppConfig):
    name = 'smart_settings'
    verbose_name = _('Smart settings')

    def ready(self):
        menu_setup.bind_links(links=[link_check_settings])
