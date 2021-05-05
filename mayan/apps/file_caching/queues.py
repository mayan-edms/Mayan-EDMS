from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_b

queue_file_caching = CeleryQueue(
    name='file_caching', label=_('File caching'), worker=worker_b
)

queue_file_caching.add_task_type(
    dotted_path='mayan.apps.file_caching.tasks.task_cache_partition_purge',
    label=_('Purge a file cache partition')
)

queue_tools.add_task_type(
    dotted_path='mayan.apps.file_caching.tasks.task_cache_purge',
    label=_('Purge a file cache')
)
