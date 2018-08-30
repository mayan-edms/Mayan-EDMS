from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import (
    icon_group_create, icon_group_setup, icon_user_create, icon_user_setup
)
from .permissions import (
    permission_group_create, permission_group_delete, permission_group_edit,
    permission_group_view, permission_user_create, permission_user_delete,
    permission_user_edit, permission_user_view
)

link_group_create = Link(
    icon_class=icon_group_create, permissions=(permission_group_create,),
    text=_('Create new group'), view='user_management:group_create'
)
link_group_delete = Link(
    args='object.id', permissions=(permission_group_delete,), tags='dangerous',
    text=_('Delete'), view='user_management:group_delete',
)
link_group_edit = Link(
    args='object.id', permissions=(permission_group_edit,), text=_('Edit'),
    view='user_management:group_edit',
)
link_group_list = Link(
    permissions=(permission_group_view,), text=_('Groups'),
    view='user_management:group_list'
)
link_group_members = Link(
    args='object.id', permissions=(permission_group_edit,), text=_('Users'),
    view='user_management:group_members',
)
link_group_setup = Link(
    icon_class=icon_group_setup, permissions=(permission_group_view,),
    text=_('Groups'), view='user_management:group_list'
)
link_user_create = Link(
    icon_class=icon_user_create, permissions=(permission_user_create,),
    text=_('Create new user'), view='user_management:user_create'
)
link_user_delete = Link(
    args='object.id', permissions=(permission_user_delete,), tags='dangerous',
    text=_('Delete'), view='user_management:user_delete',
)
link_user_edit = Link(
    args='object.id', permissions=(permission_user_edit,), text=_('Edit'),
    view='user_management:user_edit',
)
link_user_groups = Link(
    args='object.id', permissions=(permission_user_edit,), text=_('Groups'),
    view='user_management:user_groups',
)
link_user_list = Link(
    permissions=(permission_user_view,), text=_('Users'),
    view='user_management:user_list'
)
link_user_multiple_delete = Link(
    permissions=(permission_user_delete,), tags='dangerous', text=_('Delete'),
    view='user_management:user_multiple_delete'
)
link_user_multiple_set_password = Link(
    permissions=(permission_user_edit,), text=_('Set password'),
    view='user_management:user_multiple_set_password'
)
link_user_set_options = Link(
    args='object.id', permissions=(permission_user_edit,),
    text=_('User options'), view='user_management:user_options',
)
link_user_set_password = Link(
    args='object.id', permissions=(permission_user_edit,),
    text=_('Set password'), view='user_management:user_set_password',
)
link_user_setup = Link(
    icon_class=icon_user_setup, permissions=(permission_user_view,),
    text=_('Users'), view='user_management:user_list'
)
