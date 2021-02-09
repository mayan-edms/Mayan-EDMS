from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_content_type_kwargs_factory

from .icons import (
    icon_acl_delete, icon_acl_list, icon_acl_new, icon_acl_permissions,
    icon_global_acl_list
)
from .permissions import permission_acl_view, permission_acl_edit


link_acl_create = Link(
    icon=icon_acl_new, kwargs=get_content_type_kwargs_factory(
        variable_name='resolved_object'
    ), permissions=(permission_acl_edit,), text=_('New ACL'),
    view='acls:acl_create'
)
link_acl_delete = Link(
    args='resolved_object.pk', icon=icon_acl_delete,
    permissions=(permission_acl_edit,), tags='dangerous', text=_('Delete'),
    view='acls:acl_delete'
)
link_acl_list = Link(
    icon=icon_acl_list, kwargs=get_content_type_kwargs_factory(
        variable_name='resolved_object'
    ), permissions=(permission_acl_view,), text=_('ACLs'), view='acls:acl_list'
)
link_acl_permissions = Link(
    args='resolved_object.pk', icon=icon_acl_permissions,
    permissions=(permission_acl_edit,),
    text=_('Permissions'), view='acls:acl_permissions'
)
link_global_acl_list = Link(
    icon=icon_global_acl_list, text=_('Global ACLs'),
    view='acls:global_acl_list'
)
