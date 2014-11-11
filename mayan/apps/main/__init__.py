from __future__ import absolute_import

from project_setup.api import register_setup
from project_tools.api import register_tool

from .links import admin_site, maintenance_menu

register_setup(admin_site)
register_tool(maintenance_menu)
