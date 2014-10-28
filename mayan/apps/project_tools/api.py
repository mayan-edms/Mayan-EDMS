from __future__ import absolute_import

from . import tool_link

tool_items = []


def register_tool(link):
    tool_items.append(link)
