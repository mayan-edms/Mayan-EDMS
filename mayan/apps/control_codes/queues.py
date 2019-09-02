from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_fast, worker_medium

queue = CeleryQueue(
    label=_('Control codes'), name='control_codes', worker=worker_medium
)
queue.add_task_type(
    label=_('Process document version'),
    dotted_path='mayan.apps.control_codes.tasks.task_process_document_version'
)

queue = CeleryQueue(
    label=_('Control codes fast'), name='control_codes_fast',
    worker=worker_fast
)
queue.add_task_type(
    label=_('Generate control sheet code image'),
    dotted_path='mayan.apps.control_codes.tasks.task_generate_control_sheet_code_image'
)
