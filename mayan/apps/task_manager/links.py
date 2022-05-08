from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_queue_list
from .permissions import permission_task_view

link_queue_list = Link(
    icon=icon_queue_list, permissions=(permission_task_view,),
    text=_('Task manager'), view='task_manager:queue_list'
)
