from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from common import menu_object, menu_secondary, menu_tools

from .classes import Statistic, StatisticNamespace
from .links import (
    link_execute, link_namespace_details, link_namespace_list,
    link_statistics
)


class StatisticsApp(apps.AppConfig):
    name = 'statistics'
    verbose_name = _('Statistics')

    def ready(self):
        menu_object.bind_links(links=[link_execute], sources=[Statistic])
        menu_object.bind_links(links=[link_namespace_details], sources=[StatisticNamespace])
        menu_secondary.bind_links(links=[link_namespace_list], sources=[StatisticNamespace, 'statistics:namespace_list', 'statistics:execute'])
        menu_tools.bind_links(links=[link_statistics])
