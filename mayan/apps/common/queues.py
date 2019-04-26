from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue

queue_default = CeleryQueue(
    is_default_queue=True, label=_('Default'), name='default'
)
queue_tools = CeleryQueue(label=_('Tools'), name='tools')
queue_common_periodic = CeleryQueue(
    label=_('Common periodic'), name='common_periodic', transient=True
)
queue_common_periodic.add_task_type(
    label=_('Delete stale uploads'),
    name='mayan.apps.common.tasks.task_delete_stale_uploads'
)
