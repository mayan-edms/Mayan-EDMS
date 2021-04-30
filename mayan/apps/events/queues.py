from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_c

queue_events = CeleryQueue(
    label=_('Events'), name='events', transient=True,
    worker=worker_c
)

queue_events.add_task_type(
    dotted_path='mayan.apps.events.tasks.task_event_queryset_export',
    label=_('Export event querysets'), name='task_event_queryset_export',
)
