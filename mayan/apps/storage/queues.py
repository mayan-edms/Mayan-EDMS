from datetime import timedelta

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_slow

from .literals import DELETE_STALE_UPLOADS_INTERVAL

queue_storage_periodic = CeleryQueue(
    label=_('Storage periodic'), name='storage_periodic', transient=True,
    worker=worker_slow
)
queue_storage_periodic.add_task_type(
    dotted_path='mayan.apps.storage.tasks.task_delete_stale_uploads',
    label=_('Delete stale uploads'), name='task_delete_stale_uploads',
    schedule=timedelta(
        seconds=DELETE_STALE_UPLOADS_INTERVAL
    )
)
