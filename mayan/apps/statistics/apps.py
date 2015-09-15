from __future__ import unicode_literals

from celery.schedules import crontab
from kombu import Exchange, Queue

from django.utils.translation import ugettext_lazy as _

from mayan.celery import app
from common import MayanAppConfig, menu_object, menu_secondary, menu_tools

from navigation import SourceColumn

from .classes import Statistic, StatisticNamespace
from .links import (
    link_execute, link_namespace_details, link_namespace_list,
    link_statistics, link_view
)
from .tasks import task_execute_statistic  # NOQA - Force registration of task


class StatisticsApp(MayanAppConfig):
    name = 'statistics'
    verbose_name = _('Statistics')

    def ready(self):
        super(StatisticsApp, self).ready()

        SourceColumn(
            source=Statistic,
            label=_('Schedule'),
            attribute='schedule',
        )

        app.conf.CELERY_QUEUES.extend(
            (
                Queue(
                    'statistics', Exchange('statistics'),
                    routing_key='statistics', delivery_mode=1
                ),
            )
        )

        menu_object.bind_links(links=(link_execute, link_view), sources=(Statistic,))
        menu_object.bind_links(
            links=(link_namespace_details,), sources=(StatisticNamespace,)
        )
        menu_secondary.bind_links(
            links=(link_namespace_list,),
            sources=(StatisticNamespace, 'statistics:namespace_list')
        )
        menu_tools.bind_links(links=(link_statistics,))
