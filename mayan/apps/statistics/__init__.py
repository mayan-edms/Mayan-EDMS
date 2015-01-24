from __future__ import unicode_literals

from navigation.api import register_links

from project_tools.api import register_tool

from .classes import Statistic, StatisticNamespace
from .links import (
    link_execute, link_namespace_details, link_namespace_list,
    link_statistics
)

register_links(StatisticNamespace, [link_namespace_details])
register_links([StatisticNamespace, 'statistics:namespace_list', 'statistics:execute'], [link_namespace_list], menu_name='secondary_menu')
register_links(Statistic, [link_execute])
register_tool(link_statistics)
