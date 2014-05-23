from __future__ import absolute_import

from . import tool_link

tool_items = []


def register_tool(link):
    tool_items.append(link)

    # Append the link's children_view_regex to the tool main menu children view regex
    tool_link.setdefault('children_view_regex', [])
    tool_link['children_view_regex'].extend(link.get('children_view_regex', []))
