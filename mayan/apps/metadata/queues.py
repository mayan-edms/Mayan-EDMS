from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue

queue_metadata = CeleryQueue(
    label=_('Metadata'), name='metadata'
)
queue_metadata.add_task_type(
    label=_('Remove metadata type'),
    name='mayan.apps.metadata.tasks.task_remove_metadata_type'
)
queue_metadata.add_task_type(
    label=_('Add required metadata type'),
    name='mayan.apps.metadata.tasks.task_add_required_metadata_type'
)
