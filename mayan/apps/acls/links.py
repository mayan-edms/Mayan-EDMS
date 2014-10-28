from django.utils.translation import ugettext_lazy as _

from .permissions import (ACLS_CLASS_EDIT_ACL, ACLS_CLASS_VIEW_ACL,
                          ACLS_EDIT_ACL, ACLS_VIEW_ACL)

acl_list = {'text': _(u'ACLs'), 'view': 'acls:acl_list', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
acl_detail = {'text': _(u'Details'), 'view': 'acls:acl_detail', 'args': ['access_object.gid', 'object.gid'], 'famfam': 'key_go', 'permissions': [ACLS_VIEW_ACL]}
acl_grant = {'text': _(u'Grant'), 'view': 'acls:acl_multiple_grant', 'famfam': 'key_add', 'permissions': [ACLS_EDIT_ACL]}
acl_revoke = {'text': _(u'Revoke'), 'view': 'acls:acl_multiple_revoke', 'famfam': 'key_delete', 'permissions': [ACLS_EDIT_ACL]}
acl_holder_new = {'text': _(u'New holder'), 'view': 'acls:acl_holder_new', 'args': 'access_object.gid', 'famfam': 'user', 'permissions': [ACLS_EDIT_ACL]}

acl_setup_valid_classes = {'text': _(u'Default ACLs'), 'view': 'acls:acl_setup_valid_classes', 'icon': 'lock.png', 'permissions': [ACLS_CLASS_VIEW_ACL]}
acl_class_list = {'text': _(u'Classes'), 'view': 'acls:acl_setup_valid_classes', 'famfam': 'package', 'permissions': [ACLS_CLASS_VIEW_ACL]}
acl_class_acl_list = {'text': _(u'ACLs for class'), 'view': 'acls:acl_class_acl_list', 'args': 'object.gid', 'famfam': 'lock_go', 'permissions': [ACLS_CLASS_VIEW_ACL]}
acl_class_acl_detail = {'text': _(u'Details'), 'view': 'acls:acl_class_acl_detail', 'args': ['access_object_class.gid', 'object.gid'], 'famfam': 'key_go', 'permissions': [ACLS_CLASS_VIEW_ACL]}
acl_class_new_holder_for = {'text': _(u'New holder'), 'view': 'acls:acl_class_new_holder_for', 'args': 'object.gid', 'famfam': 'user', 'permissions': [ACLS_CLASS_EDIT_ACL]}
acl_class_grant = {'text': _(u'Grant'), 'view': 'acls:acl_class_multiple_grant', 'famfam': 'key_add', 'permissions': [ACLS_CLASS_EDIT_ACL]}
acl_class_revoke = {'text': _(u'Revoke'), 'view': 'acls:acl_class_multiple_revoke', 'famfam': 'key_delete', 'permissions': [ACLS_CLASS_EDIT_ACL]}
