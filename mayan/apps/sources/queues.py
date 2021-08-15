from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_a, worker_b, worker_c

queue_sources = CeleryQueue(
    label=_('Sources'), name='sources', worker=worker_b
)
queue_sources_periodic = CeleryQueue(
    label=_('Sources periodic'), name='sources_periodic', transient=True,
    worker=worker_c
)
queue_sources_fast = CeleryQueue(
    label=_('Sources fast'), name='sources_fast', transient=True,
    worker=worker_a
)

queue_sources_periodic.add_task_type(
    label=_('Check interval source'),
    dotted_path='mayan.apps.sources.tasks.task_source_process_document'
)

queue_sources.add_task_type(
    label=_('Handle upload'),
    dotted_path='mayan.apps.sources.tasks.task_process_document_upload'
)
