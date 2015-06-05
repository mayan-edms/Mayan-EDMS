from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    PERMISSION_GROUP_CREATE, PERMISSION_GROUP_DELETE, PERMISSION_GROUP_EDIT,
    PERMISSION_GROUP_VIEW, PERMISSION_USER_CREATE, PERMISSION_USER_DELETE,
    PERMISSION_USER_EDIT, PERMISSION_USER_VIEW
)

link_group_add = Link(permissions=[PERMISSION_GROUP_CREATE], text=_('Create new group'), view='user_management:group_add')
link_group_delete = Link(permissions=[PERMISSION_GROUP_DELETE], tags='dangerous', text=_('Delete'), view='user_management:group_delete', args='object.id')
link_group_edit = Link(permissions=[PERMISSION_GROUP_EDIT], text=_('Edit'), view='user_management:group_edit', args='object.id')
link_group_list = Link(permissions=[PERMISSION_GROUP_VIEW], text=_('Groups'), view='user_management:group_list')
link_group_members = Link(permissions=[PERMISSION_GROUP_EDIT], text=_('Members'), view='user_management:group_members', args='object.id')
link_group_multiple_delete = Link(permissions=[PERMISSION_GROUP_DELETE], text=_('Delete'), view='user_management:group_multiple_delete')
link_group_setup = Link(icon='fa fa-group', permissions=[PERMISSION_GROUP_VIEW], text=_('Groups'), view='user_management:group_list')
link_user_add = Link(permissions=[PERMISSION_USER_CREATE], text=_('Create new user'), view='user_management:user_add')
link_user_delete = Link(permissions=[PERMISSION_USER_DELETE], tags='dangerous', text=_('Delete'), view='user_management:user_delete', args='object.id')
link_user_edit = Link(permissions=[PERMISSION_USER_EDIT], text=_('Edit'), view='user_management:user_edit', args='object.id')
link_user_groups = Link(permissions=[PERMISSION_USER_EDIT], text=_('Groups'), view='user_management:user_groups', args='object.id')
link_user_list = Link(permissions=[PERMISSION_USER_VIEW], text=_('Users'), view='user_management:user_list')
link_user_multiple_delete = Link(permissions=[PERMISSION_USER_DELETE], tags='dangerous', text=_('Delete'), view='user_management:user_multiple_delete')
link_user_multiple_set_password = Link(permissions=[PERMISSION_USER_EDIT], text=_('Reset password'), view='user_management:user_multiple_set_password')
link_user_set_password = Link(permissions=[PERMISSION_USER_EDIT], text=_('Reset password'), view='user_management:user_set_password', args='object.id')
link_user_setup = Link(icon='fa fa-user', permissions=[PERMISSION_USER_VIEW], text=_('Users'), view='user_management:user_list')
