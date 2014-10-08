from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from navigation.api import register_top_menu
from project_setup.api import register_setup
from project_tools.api import register_tool

from .links import admin_site, diagnostics, maintenance_menu

if 'django.contrib.admin' in django_settings.INSTALLED_APPS:
    register_setup(admin_site)

register_tool(diagnostics)
register_tool(maintenance_menu)
