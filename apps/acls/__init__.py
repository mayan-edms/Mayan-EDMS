from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from permissions.models import PermissionNamespace, Permission
from project_setup.api import register_setup

from acls.models import AccessHolder, AccessObjectClass

acls_namespace = PermissionNamespace('acls', _(u'Access control lists'))

ACLS_EDIT_ACL = Permission.objects.register(acls_namespace, 'acl_edit', _(u'Edit ACLs'))
ACLS_VIEW_ACL = Permission.objects.register(acls_namespace, 'acl_view', _(u'View ACLs'))

acl_list = {'text': _(u'ACLs'), 'view': 'acl_list', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
acl_detail = {'text': _(u'edit'), 'view': 'acl_detail', 'args': ['access_object.gid', 'object.gid'], 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
acl_grant = {'text': _(u'grant'), 'view': 'acl_multiple_grant', 'famfam': 'key_add', 'permissions': [ACLS_EDIT_ACL]}
acl_revoke = {'text': _(u'revoke'), 'view': 'acl_multiple_revoke', 'famfam': 'key_delete', 'permissions': [ACLS_EDIT_ACL]}

acl_setup_valid_classes = {'text': _(u'Default ACLs'), 'view': 'acl_setup_valid_classes', 'icon': 'lock.png'}#, 'permissions': [ACLS_EDIT_ACL]}
acl_class_acl_list = {'text': _(u'ACLs for class'), 'view': 'acl_class_acl_list', 'args': 'object.gid', 'famfam': 'lock'}#, 'permissions': [ACLS_VIEW_ACL]}

register_links(AccessHolder, [acl_detail])
register_multi_item_links(['acl_detail'], [acl_grant, acl_revoke])

register_setup(acl_setup_valid_classes)
register_links(['acl_setup_valid_classes', 'acl_class_acl_list',], [acl_setup_valid_classes], menu_name='sidebar')

register_links(AccessObjectClass, [acl_class_acl_list])
