from datetime import timedelta

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium, worker_slow

from .literals import DELETE_STALE_UPLOADS_INTERVAL

queue_default = CeleryQueue(
    default_queue=True, label=_('Default'), name='default', worker=worker_medium
)
queue_tools = CeleryQueue(label=_('Tools'), name='tools', worker=worker_slow)
queue_common_periodic = CeleryQueue(
    label=_('Common periodic'), name='common_periodic', transient=True,
    worker=worker_slow
)
queue_common_periodic.add_task_type(
    dotted_path='mayan.apps.common.tasks.task_delete_stale_uploads',
    label=_('Delete stale uploads'), name='task_delete_stale_uploads',
    schedule=timedelta(
        seconds=DELETE_STALE_UPLOADS_INTERVAL
    )
)
