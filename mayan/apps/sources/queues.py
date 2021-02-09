from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_fast, worker_medium

queue_sources = CeleryQueue(
    label=_('Sources'), name='sources', worker=worker_medium
)
queue_sources_periodic = CeleryQueue(
    label=_('Sources periodic'), name='sources_periodic', transient=True,
    worker=worker_medium
)
queue_sources_fast = CeleryQueue(
    label=_('Sources fast'), name='sources_fast', transient=True,
    worker=worker_fast
)

queue_sources_fast.add_task_type(
    label=_('Generate staging file image'),
    dotted_path='mayan.apps.sources.tasks.task_generate_staging_file_image'
)
queue_sources_periodic.add_task_type(
    label=_('Check interval source'),
    dotted_path='mayan.apps.sources.tasks.task_check_interval_source'
)
queue_sources.add_task_type(
    label=_('Handle upload'),
    dotted_path='mayan.apps.sources.tasks.task_source_handle_upload'
)
queue_sources.add_task_type(
    label=_('Upload document'),
    dotted_path='mayan.apps.sources.tasks.task_upload_document'
)
