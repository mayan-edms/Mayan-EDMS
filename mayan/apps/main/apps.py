from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_main, menu_setup, menu_tools


from .links import (
    link_admin_site, link_maintenance_menu, link_tools, link_setup, link_tools
)


class MainApp(apps.AppConfig):
    name = 'main'
    verbose_name = _('Main')

    def ready(self):
        menu_main.bind_links(links=[link_setup], position=-2)
        menu_main.bind_links(links=[link_tools], position=-3)
        menu_setup.bind_links(links=[link_admin_site])
        menu_tools.bind_links(links=[link_maintenance_menu])
