from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_slow

queue_document_states = CeleryQueue(
    name='document_states', label=_('Document states'), worker=worker_slow
)
queue_document_states.add_task_type(
    dotted_path='mayan.apps.document_states.tasks.task_launch_all_workflows',
    label=_('Launch all workflows')
)
