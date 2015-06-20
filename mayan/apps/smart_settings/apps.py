from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_setup

from .links import link_check_settings


class SmartSettingsApp(MayanAppConfig):
    app_namespace = 'settings'
    app_url = 'settings'
    name = 'smart_settings'
    verbose_name = _('Smart settings')

    def ready(self):
        super(SmartSettingsApp, self).ready()

        menu_setup.bind_links(links=[link_check_settings])
