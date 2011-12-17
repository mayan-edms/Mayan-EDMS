from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from permissions.models import PermissionNamespace, Permission
from project_setup.api import register_setup

from acls.models import AccessHolder, AccessObjectClass

acls_namespace = PermissionNamespace('acls', _(u'Access control lists'))

ACLS_EDIT_ACL = Permission.objects.register(acls_namespace, 'acl_edit', _(u'Edit ACLs'))
ACLS_VIEW_ACL = Permission.objects.register(acls_namespace, 'acl_view', _(u'View ACLs'))

ACLS_CLASS_EDIT_ACL = Permission.objects.register(acls_namespace, 'acl_edit', _(u'Edit class default ACLs'))
ACLS_CLASS_VIEW_ACL = Permission.objects.register(acls_namespace, 'acl_view', _(u'View class default ACLs'))


acl_list = {'text': _(u'ACLs'), 'view': 'acl_list', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
acl_detail = {'text': _(u'edit'), 'view': 'acl_detail', 'args': ['access_object.gid', 'object.gid'], 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
acl_grant = {'text': _(u'grant'), 'view': 'acl_multiple_grant', 'famfam': 'key_add', 'permissions': [ACLS_EDIT_ACL]}
acl_revoke = {'text': _(u'revoke'), 'view': 'acl_multiple_revoke', 'famfam': 'key_delete', 'permissions': [ACLS_EDIT_ACL]}

acl_setup_valid_classes = {'text': _(u'Default ACLs'), 'view': 'acl_setup_valid_classes', 'icon': 'lock.png'}#, 'permissions': [ACLS_EDIT_ACL]}
acl_class_list = {'text': _(u'List of classes'), 'view': 'acl_setup_valid_classes', 'famfam': 'package'}#, 'permissions': [ACLS_EDIT_ACL]}
acl_class_acl_list = {'text': _(u'ACLs for class'), 'view': 'acl_class_acl_list', 'args': 'object.gid', 'famfam': 'lock'}#, 'permissions': [ACLS_VIEW_ACL]}
acl_class_new_holder_for = {'text': _(u'New holder'), 'view': 'acl_class_new_holder_for', 'args': 'object.gid', 'famfam': 'user'}#, 'permissions': [ACLS_VIEW_ACL]}
acl_class_grant = {'text': _(u'grant'), 'view': 'acl_class_multiple_grant', 'famfam': 'key_add', 'permissions': [ACLS_EDIT_ACL]}
acl_class_revoke = {'text': _(u'revoke'), 'view': 'acl_class_multiple_revoke', 'famfam': 'key_delete', 'permissions': [ACLS_EDIT_ACL]}

register_links(AccessHolder, [acl_detail])
register_multi_item_links(['acl_detail'], [acl_grant, acl_revoke])

register_setup(acl_setup_valid_classes)
register_links(['acl_setup_valid_classes', 'acl_class_acl_list', 'acl_class_new_holder_for', 'acls_class_acl_detail'], [acl_class_list], menu_name='sidebar')

register_links(AccessObjectClass, [acl_class_acl_list])
register_links(AccessObjectClass, [acl_class_new_holder_for])
register_multi_item_links(['acls_class_acl_detail'], [acl_class_grant, acl_class_revoke])
