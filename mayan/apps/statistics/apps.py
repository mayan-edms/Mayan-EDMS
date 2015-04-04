from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_tools

from .classes import Statistic, StatisticNamespace
from .links import (
    link_execute, link_namespace_details, link_namespace_list,
    link_statistics
)


class StatisticsApp(apps.AppConfig):
    name = 'statistics'
    verbose_name = _('Statistics')

    def ready(self):
        #register_links(StatisticNamespace, [link_namespace_details])
        #register_links([StatisticNamespace, 'statistics:namespace_list', 'statistics:execute'], [link_namespace_list], menu_name='secondary_menu')
        #register_links(Statistic, [link_execute])
        menu_tools.bind_links(links=[link_statistics])
