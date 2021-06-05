from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_d

queue_file_metadata = CeleryQueue(
    label=_('File metadata'), name='file_metadata', worker=worker_d
)

queue_file_metadata.add_task_type(
    label=_('Process document file'),
    dotted_path='mayan.apps.file_metadata.tasks.task_process_document_file'
)
