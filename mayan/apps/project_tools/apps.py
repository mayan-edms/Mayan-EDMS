from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu

from .links import link_tools


class ProjectToolsApp(apps.AppConfig):
    name = 'project_tools'
    verbose_name = _('Project tools')

    def ready(self):
        tool_link = register_top_menu('tools', link=link_tools, position=-3)

