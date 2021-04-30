from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_c

queue_statistics = CeleryQueue(
    label=_('Statistics'), name='statistics', transient=True,
    worker=worker_c
)

task_execute_statistic = queue_statistics.add_task_type(
    label=_('Execute statistic'),
    dotted_path='mayan.apps.mayan_statistics.tasks.task_execute_statistic'
)
