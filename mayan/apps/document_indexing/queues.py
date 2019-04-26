from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue

queue_indexing = CeleryQueue(label=_('Indexing'), name='indexing')

queue_indexing.add_task_type(
    label=_('Delete empty index nodes'),
    name='mayan.apps.document_indexing.tasks.task_delete_empty'
)
queue_indexing.add_task_type(
    label=_('Remove document'),
    name='mayan.apps.document_indexing.tasks.task_remove_document'
)
queue_indexing.add_task_type(
    label=_('Index document'),
    name='mayan.apps.document_indexing.tasks.task_index_document'
)
queue_tools.add_task_type(
    label=_('Rebuild index'),
    name='mayan.apps.document_indexing.tasks.task_rebuild_index'
)
