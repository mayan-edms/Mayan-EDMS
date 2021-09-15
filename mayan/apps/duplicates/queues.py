from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_b


queue_duplicates = CeleryQueue(
    label=_('Duplicates'), name='duplicates', worker=worker_b
)

queue_duplicates.add_task_type(
    dotted_path='mayan.apps.duplicates.tasks.task_duplicates_clean_empty_lists',
    label=_('Clean empty duplicate lists')
)
queue_duplicates.add_task_type(
    dotted_path='mayan.apps.duplicates.tasks.task_duplicates_scan_for',
    label=_('Scan document duplicates')
)

queue_tools.add_task_type(
    dotted_path='mayan.apps.duplicates.tasks.task_duplicates_scan_all',
    label=_('Duplicated document scan')
)
