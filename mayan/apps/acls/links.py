from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import acls_edit_acl, acls_view_acl

link_acl_list = Link(permissions=[acls_view_acl], text=_('ACLs'), view='acls:acl_list')

link_acl_detail = Link(permissions=[acls_view_acl], text=_('Details'), view='acls:acl_detail', args=['access_object.gid', 'object.gid'])
link_acl_grant = Link(permissions=[acls_edit_acl], text=_('Grant'), view='acls:acl_multiple_grant')
link_acl_revoke = Link(permissions=[acls_edit_acl], text=_('Revoke'), view='acls:acl_multiple_revoke')
link_acl_holder_new = Link(permissions=[acls_edit_acl], text=_('New holder'), view='acls:acl_holder_new', args='access_object.gid')
