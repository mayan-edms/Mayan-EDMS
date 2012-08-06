from __future__ import absolute_import

from project_tools.api import register_tool
from navigation.api import bind_links

from .links import maintenance_menu, maintenance_execute
from .api import MaintenanceTool

register_tool(maintenance_menu)
bind_links(['maintenance_menu'], maintenance_menu, menu_name='secondary_menu')
bind_links([MaintenanceTool], maintenance_execute)
