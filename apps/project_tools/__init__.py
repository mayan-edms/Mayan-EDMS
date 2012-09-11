from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, Link

from .icons import icon_tool

tool_menu = register_top_menu('tools', link=Link(text=_(u'tools'), view='tools_list', icon=icon_tool), position=-3)
