from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common.menus import menu_main

from .links import link_tools


class ProjectToolsApp(apps.AppConfig):
    name = 'project_tools'
    verbose_name = _('Project tools')

    def ready(self):
        menu_main.bind_links(links=[link_tools], position=-3)
