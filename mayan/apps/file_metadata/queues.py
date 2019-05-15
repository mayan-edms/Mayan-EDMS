from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

queue = CeleryQueue(
    label=_('File metadata'), name='file_metadata', worker=worker_medium
)
queue.add_task_type(
    label=_('Process document version'),
    dotted_path='mayan.apps.file_metadata.tasks.task_process_document_version'
)
