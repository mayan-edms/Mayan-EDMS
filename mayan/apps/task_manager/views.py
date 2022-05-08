from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import SingleObjectListView

from .classes import CeleryQueue
from .icons import icon_queue_list
from .permissions import permission_task_view


class QueueListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('Background task queues'),
    }
    view_icon = icon_queue_list
    view_permission = permission_task_view

    def get_source_queryset(self):
        return CeleryQueue.all()
