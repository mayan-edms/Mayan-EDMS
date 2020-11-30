from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.documents.queues import queue_documents, queue_uploads

queue_documents.add_task_type(
    dotted_path='mayan.apps.duplicates.tasks.task_duplicates_clean_empty_lists',
    label=_('Clean empty duplicate lists')
)

queue_tools.add_task_type(
    dotted_path='mayan.apps.duplicates.tasks.task_duplicates_scan_all',
    label=_('Duplicated document scan')
)

queue_uploads.add_task_type(
    dotted_path='mayan.apps.duplicates.tasks.task_duplicates_scan_for',
    label=_('Scan document duplicates')
)
