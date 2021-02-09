from django.utils.translation import ugettext_lazy as _

from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_slow

queue_search = CeleryQueue(
    label=_('Search'), name='search', worker=worker_slow
)
queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_deindex_instance',
    label=_('Remove a model instance from the search engine.'),
    name='task_index_instance',
)
queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_index_instance',
    label=_('Index a model instance to the search engine.'),
    name='task_deindex_instance',
)
