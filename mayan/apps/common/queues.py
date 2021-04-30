from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_d

queue_tools = CeleryQueue(label=_('Tools'), name='tools', worker=worker_d)
