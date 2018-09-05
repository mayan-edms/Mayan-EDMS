from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link, get_cascade_condition

from .icons import icon_message_create, icon_message_list
from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)


link_message_create = Link(
    icon_class=icon_message_create, permissions=(permission_message_create,),
    text=_('Create message'), view='motd:message_create'
)
link_message_delete = Link(
    args='object.pk', permissions=(permission_message_delete,),
    tags='dangerous', text=_('Delete'), view='motd:message_delete'
)
link_message_edit = Link(
    args='object.pk', permissions=(permission_message_edit,), text=_('Edit'),
    view='motd:message_edit'
)
link_message_list = Link(
    condition=get_cascade_condition(
        app_label='motd', model_name='Message',
        object_permission=permission_message_view,
        view_permission=permission_message_create,
    ), icon_class=icon_message_list, text=_('Message of the day'),
    view='motd:message_list'
)
