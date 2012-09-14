from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (PERMISSION_GROUP_CREATE, PERMISSION_GROUP_EDIT,
    PERMISSION_GROUP_VIEW, PERMISSION_GROUP_DELETE, PERMISSION_GROUP_CREATE,
    PERMISSION_GROUP_EDIT, PERMISSION_GROUP_VIEW, PERMISSION_GROUP_DELETE)
from .icons import (icon_user, icon_user_add, icon_user_edit, icon_user_delete,
    icon_group, icon_group_add, icon_group_edit, icon_group_delete, icon_set_password,
    icon_group_members)

user_list = Link(text=_(u'user list'), view='user_list', icon=icon_user, permissions=[PERMISSION_GROUP_VIEW])
user_setup = Link(text=_(u'users'), view='user_list', icon=icon_user, permissions=[PERMISSION_GROUP_VIEW], children_view_regex=[r'^user_'])
user_add = Link(text=_(u'create new user'), view='user_add', icon=icon_user_add, permissions=[PERMISSION_GROUP_CREATE])
user_edit = Link(text=_(u'edit'), view='user_edit', args='object.id', icon=icon_user_edit, permissions=[PERMISSION_GROUP_EDIT])
user_delete = Link(text=_('delete'), view='user_delete', args='object.id', icon=icon_user_delete, permissions=[PERMISSION_GROUP_DELETE])
user_multiple_delete = Link(text=_('delete'), view='user_multiple_delete', icon=icon_user_delete, permissions=[PERMISSION_GROUP_DELETE])
user_set_password = Link(text=_('reset password'), view='user_set_password', args='object.id', icon=icon_set_password, permissions=[PERMISSION_GROUP_EDIT])
user_multiple_set_password = Link(text=_('reset password'), view='user_multiple_set_password', icon=icon_set_password, permissions=[PERMISSION_GROUP_EDIT])

group_list = Link(text=_(u'group list'), view='group_list', icon=icon_group, permissions=[PERMISSION_GROUP_VIEW])
group_setup = Link(text=_(u'groups'), view='group_list', icon=icon_group, permissions=[PERMISSION_GROUP_VIEW], children_view_regex=[r'^group_'])
group_add = Link(text=_(u'create new group'), view='group_add', icon=icon_group_add, permissions=[PERMISSION_GROUP_CREATE])
group_edit = Link(text=_(u'edit'), view='group_edit', args='object.id', icon=icon_group_edit, permissions=[PERMISSION_GROUP_EDIT])
group_delete = Link(text=_('delete'), view='group_delete', args='object.id', icon=icon_group_delete, permissions=[PERMISSION_GROUP_DELETE])
group_multiple_delete = Link(text=_('delete'), view='group_multiple_delete', icon=icon_group_delete, permissions=[PERMISSION_GROUP_DELETE])
group_members = Link(text=_(u'members'), view='group_members', args='object.id', icon=icon_group_members, permissions=[PERMISSION_GROUP_EDIT])
