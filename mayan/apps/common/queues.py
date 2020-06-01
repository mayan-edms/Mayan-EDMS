from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium, worker_slow

queue_default = CeleryQueue(
    default_queue=True, label=_('Default'), name='default', worker=worker_medium
)
queue_tools = CeleryQueue(label=_('Tools'), name='tools', worker=worker_slow)
