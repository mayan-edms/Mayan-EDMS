from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu

from .links import link_setup


class ProjectSetupApp(apps.AppConfig):
    name = 'project_setup'
    verbose_name = _('Project setup')

    def ready(self):
        register_top_menu('setup_menu', link=link_setup, position=-2)
