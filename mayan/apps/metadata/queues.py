from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_b

queue_metadata = CeleryQueue(
    label=_('Metadata'), name='metadata', worker=worker_b
)

queue_metadata.add_task_type(
    label=_('Remove metadata type'),
    dotted_path='mayan.apps.metadata.tasks.task_remove_metadata_type'
)
queue_metadata.add_task_type(
    label=_('Add required metadata type'),
    dotted_path='mayan.apps.metadata.tasks.task_add_required_metadata_type'
)
