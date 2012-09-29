from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (ACLS_EDIT_ACL, ACLS_VIEW_ACL,
    ACLS_CLASS_EDIT_ACL, ACLS_CLASS_VIEW_ACL)
from .icons import (icon_acls, icon_acl_detail, icon_acl_grant, icon_acl_revoke,
    icon_acl_holder_new, icon_acl_class_list, icon_acl_class_acl_list,
    icon_acl_class_acl_list, icon_acl_class_acl_detail, icon_acl_class_new_holder_for,
    icon_acl_class_grant, icon_acl_class_revoke)

acl_list = Link(text=_(u'ACLs'), view='acl_list', icon=icon_acls, permissions=[ACLS_VIEW_ACL])
acl_detail = Link(text=_(u'details'), view='acl_detail', args=['access_object.gid', 'object.gid'], icon=icon_acl_detail, permissions=[ACLS_VIEW_ACL])
acl_grant = Link(text=_(u'grant'), view='acl_multiple_grant', icon=icon_acl_grant, permissions=[ACLS_EDIT_ACL])
acl_revoke = Link(text=_(u'revoke'), view='acl_multiple_revoke', icon=icon_acl_revoke, permissions=[ACLS_EDIT_ACL])
acl_holder_new = Link(text=_(u'New holder'), view='acl_holder_new', args='access_object.gid', icon=icon_acl_holder_new, permissions=[ACLS_EDIT_ACL])

acl_setup_valid_classes = Link(text=_(u'Default ACLs'), view='acl_setup_valid_classes', icon=icon_acl_class_list, permissions=[ACLS_CLASS_VIEW_ACL])  # 'children_view_regex=[r'^acl_class', r'^acl_setup']}
acl_class_list = Link(text=_(u'List of classes'), view='acl_setup_valid_classes', icon=icon_acl_class_list, permissions=[ACLS_CLASS_VIEW_ACL])
acl_class_acl_list = Link(text=_(u'ACLs for class'), view='acl_class_acl_list', args='object.gid', icon=icon_acl_class_acl_list, permissions=[ACLS_CLASS_VIEW_ACL])
acl_class_acl_detail = Link(text=_(u'details'), view='acl_class_acl_detail', args=['access_object_class.gid', 'object.gid'], icon=icon_acl_class_acl_detail, permissions=[ACLS_CLASS_VIEW_ACL])
acl_class_new_holder_for = Link(text=_(u'New holder'), view='acl_class_new_holder_for', args='object.gid', icon=icon_acl_class_new_holder_for, permissions=[ACLS_CLASS_EDIT_ACL])
acl_class_grant = Link(text=_(u'grant'), view='acl_class_multiple_grant', icon=icon_acl_class_grant, permissions=[ACLS_CLASS_EDIT_ACL])
acl_class_revoke = Link(text=_(u'revoke'), view='acl_class_multiple_revoke', icon=icon_acl_class_revoke, permissions=[ACLS_CLASS_EDIT_ACL])
