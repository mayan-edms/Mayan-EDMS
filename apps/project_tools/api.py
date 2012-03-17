from __future__ import absolute_import

from elementtree.ElementTree import Element, SubElement

from . import tool_menu


def register_tool(link):
    SubElement(tool_menu, 'tool_link', link=link)
