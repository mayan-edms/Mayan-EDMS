from datetime import timedelta

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

from .literals import CHECK_EXPIRED_CHECK_OUTS_INTERVAL

queue_checkouts_periodic = CeleryQueue(
    label=_('Checkouts periodic'), name='checkouts_periodic', transient=True,
    worker=worker_medium
)
queue_checkouts_periodic.add_task_type(
    label=_('Check expired checkouts'),
    name='task_check_expired_check_outs',
    dotted_path='mayan.apps.checkouts.tasks.task_check_expired_check_outs',
    schedule=timedelta(
        seconds=CHECK_EXPIRED_CHECK_OUTS_INTERVAL
    ),
)
