from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_b

queue_parsing = CeleryQueue(
    name='parsing', label=_('Parsing'), worker=worker_b
)

queue_parsing.add_task_type(
    dotted_path='mayan.apps.document_parsing.tasks.task_parse_document_file',
    label=_('Document file parsing')
)
