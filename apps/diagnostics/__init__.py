from __future__ import absolute_import

from project_tools.api import register_tool
from navigation.api import bind_links

from .links import diagnostic_list, diagnostic_execute
from .api import DiagnosticTool

register_tool(diagnostic_list)
bind_links(['diagnostic_list'], diagnostic_list, menu_name='secondary_menu')
bind_links([DiagnosticTool], diagnostic_execute)
