from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)

link_message_create = Link(
    icon_class_path='mayan.apps.motd.icons.icon_message_create',
    permissions=(permission_message_create,),
    text=_('Create message'), view='motd:message_create'
)
link_message_multiple_delete = Link(
    icon_class_path='mayan.apps.motd.icons.icon_message_delete',
    tags='dangerous', text=_('Delete'), view='motd:message_multiple_delete'
)
link_message_single_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.motd.icons.icon_message_delete',
    permissions=(permission_message_delete,),
    tags='dangerous', text=_('Delete'), view='motd:message_single_delete'
)
link_message_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.motd.icons.icon_message_edit',
    permissions=(permission_message_edit,), text=_('Edit'),
    view='motd:message_edit'
)
link_message_list = Link(
    condition=get_cascade_condition(
        app_label='motd', model_name='Message',
        object_permission=permission_message_view,
        view_permission=permission_message_create,
    ), icon_class_path='mayan.apps.motd.icons.icon_message_list',
    text=_('Message of the day'),
    view='motd:message_list'
)
