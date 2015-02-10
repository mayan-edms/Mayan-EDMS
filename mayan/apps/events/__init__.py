from __future__ import unicode_literals

from project_tools.api import register_tool

from .classes import Event  # NOQA
from .links import events_list

register_tool(events_list)
