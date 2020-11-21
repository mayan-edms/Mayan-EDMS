from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_task_manager
from .permissions import permission_task_view

link_task_manager = Link(
    icon=icon_task_manager, permissions=(permission_task_view,),
    text=_('Task manager'), view='task_manager:queue_list'
)
