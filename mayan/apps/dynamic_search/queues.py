from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_b

queue_search = CeleryQueue(
    label=_('Search'), name='search', worker=worker_b
)

queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_deindex_instance',
    label=_('Remove a model instance from the search engine.'),
    name='task_deindex_instance',
)
queue_search.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_index_instance',
    label=_('Index a model instance to the search engine.'),
    name='task_index_instance',
)

queue_tools.add_task_type(
    dotted_path='mayan.apps.dynamic_search.tasks.task_index_search_model',
    label=_('Index all instances of a search model to the search engine.'),
    name='task_index_search_model',
)
