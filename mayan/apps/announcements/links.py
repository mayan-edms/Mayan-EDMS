from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
    icon_announcement_create, icon_announcement_delete, icon_announcement_edit,
    icon_announcement_list
)
from .permissions import (
    permission_announcement_create, permission_announcement_delete,
    permission_announcement_edit, permission_announcement_view
)

link_announcement_create = Link(
    icon=icon_announcement_create, permissions=(permission_announcement_create,),
    text=_('Create announcement'), view='announcements:announcement_create'
)
link_announcement_multiple_delete = Link(
    icon=icon_announcement_delete, tags='dangerous', text=_('Delete'),
    view='announcements:announcement_multiple_delete'
)
link_announcement_single_delete = Link(
    args='object.pk', icon=icon_announcement_delete,
    permissions=(permission_announcement_delete,),
    tags='dangerous', text=_('Delete'),
    view='announcements:announcement_single_delete'
)
link_announcement_edit = Link(
    args='object.pk', icon=icon_announcement_edit,
    permissions=(permission_announcement_edit,), text=_('Edit'),
    view='announcements:announcement_edit'
)
link_announcement_list = Link(
    condition=get_cascade_condition(
        app_label='announcements', model_name='Announcement',
        object_permission=permission_announcement_view,
        view_permission=permission_announcement_create,
    ), icon=icon_announcement_list,
    text=_('Announcements'),
    view='announcements:announcement_list'
)
