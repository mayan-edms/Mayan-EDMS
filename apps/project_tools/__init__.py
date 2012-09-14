from __future__ import absolute_import

from navigation.api import register_top_menu

from .links import link_tools

tool_menu = register_top_menu('tools', link=link_tools, position=-3)
