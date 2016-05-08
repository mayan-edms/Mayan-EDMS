from __future__ import unicode_literals

from kombu import Exchange, Queue

from django.utils.translation import ugettext_lazy as _

from mayan.celery import app
from common import MayanAppConfig, menu_object, menu_secondary, menu_tools
from common.classes import Package

from navigation import SourceColumn

from .classes import Statistic, StatisticNamespace
from .links import (
    link_execute, link_namespace_details, link_namespace_list,
    link_statistics, link_view
)
from .tasks import task_execute_statistic  # NOQA - Force registration of task


class StatisticsApp(MayanAppConfig):
    name = 'statistics'
    test = True
    verbose_name = _('Statistics')

    def ready(self):
        super(StatisticsApp, self).ready()

        Package(label='Chart.js', license_text='''
Copyright (c) 2013-2015 Nick Downie

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        ''')

        SourceColumn(
            source=Statistic,
            # Translators: Schedule here is a verb, the 'schedule' at which the
            # statistic will be updated
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

        app.conf.CELERY_ROUTES.update(
            {
                'statistics.tasks.task_execute_statistic': {
                    'queue': 'statistics'
                },
            }
        )

        menu_object.bind_links(
            links=(link_execute, link_view), sources=(Statistic,)
        )
        menu_object.bind_links(
            links=(link_namespace_details,), sources=(StatisticNamespace,)
        )
        menu_secondary.bind_links(
            links=(link_namespace_list,),
            sources=(StatisticNamespace, 'statistics:namespace_list')
        )
        menu_tools.bind_links(links=(link_statistics,))
