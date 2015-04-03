from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common.menus import menu_main

from .links import link_setup


class ProjectSetupApp(apps.AppConfig):
    name = 'project_setup'
    verbose_name = _('Project setup')

    def ready(self):
        menu_main.bind_links(links=[link_setup], position=-2)
