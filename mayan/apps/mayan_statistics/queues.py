from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue

queue_statistics = CeleryQueue(
    label=_('Statistics'), name='statistics', transient=True
)

queue_statistics.add_task_type(
    label=_('Execute statistic'),
    name='mayan.apps.mayan_statistics.tasks.task_execute_statistic'
)
