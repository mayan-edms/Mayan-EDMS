from django.utils.translation import ugettext_lazy as _

from permissions.api import register_permission, set_namespace_title
from navigation.api import register_links, register_multi_item_links

from acls.models import AccessHolder


ACLS_EDIT_ACL = {'namespace': 'acls', 'name': 'acl_edit', 'label': _(u'Edit ACLs')}
ACLS_VIEW_ACL = {'namespace': 'acls', 'name': 'acl_view', 'label': _(u'View ACLs')}

set_namespace_title('acls', _(u'Access control lists'))
register_permission(ACLS_EDIT_ACL)
register_permission(ACLS_VIEW_ACL)

acl_list = {'text': _(u'ACLs'), 'view': 'acl_list', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
acl_detail = {'text': _(u'edit'), 'view': 'acl_detail', 'args': ['access_object.gid', 'object.gid'], 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
acl_grant = {'text': _(u'grant'), 'view': 'acl_multiple_grant', 'famfam': 'key_add', 'permissions': [ACLS_EDIT_ACL]}

register_links(AccessHolder, [acl_detail])
register_multi_item_links(['acl_detail'], [acl_grant])#, permission_revoke])
