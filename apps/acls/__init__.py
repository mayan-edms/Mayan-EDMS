from django.utils.translation import ugettext_lazy as _

from permissions.api import register_permission, set_namespace_title


ACLS_EDIT_ACL = {'namespace': 'acls', 'name': 'acl_edit', 'label': _(u'Edit ACLs')}
ACLS_VIEW_ACL = {'namespace': 'acls', 'name': 'acl_view', 'label': _(u'View ACLs')}

set_namespace_title('acls', _(u'Access control lists'))
register_permission(ACLS_EDIT_ACL)
register_permission(ACLS_VIEW_ACL)

acl_list = {'text': _(u'ACLs'), 'view': 'acl_list', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
