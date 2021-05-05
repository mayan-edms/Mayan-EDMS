from datetime import timedelta

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_d

from .literals import (
    TASK_DOWNLOAD_FILE_STALE_INTERVAL, TASK_SHARED_UPLOADS_STALE_INTERVAL
)

queue_storage_periodic = CeleryQueue(
    label=_('Storage periodic'), name='storage_periodic', transient=True,
    worker=worker_d
)

queue_storage_periodic.add_task_type(
    dotted_path='mayan.apps.storage.tasks.task_shared_upload_stale_delete',
    label=_('Delete stale uploads'), name='task_shared_upload_stale_delete',
    schedule=timedelta(
        seconds=TASK_SHARED_UPLOADS_STALE_INTERVAL
    )
)
queue_storage_periodic.add_task_type(
    dotted_path='mayan.apps.storage.tasks.task_download_files_stale_delete',
    label=_('Delete stale download files'),
    name='task_download_files_stale_delete',
    schedule=timedelta(
        seconds=TASK_DOWNLOAD_FILE_STALE_INTERVAL
    )
)
