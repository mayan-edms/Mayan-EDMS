from __future__ import absolute_import

from project_tools.api import register_tool
from navigation.api import bind_links

from .links import backup_tool_link, restore_tool_link

register_tool(backup_tool_link)
register_tool(restore_tool_link)
