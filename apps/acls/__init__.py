from __future__ import absolute_import

from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup

from .classes import (AccessHolder, AccessObjectClass, ClassAccessHolder,
    AccessObject)
from .links import (acl_detail, acl_grant, acl_revoke, acl_holder_new,
    acl_setup_valid_classes, acl_class_list, acl_class_acl_list,
    acl_class_acl_detail, acl_class_new_holder_for, acl_class_grant,
    acl_class_revoke)

register_links(AccessHolder, [acl_detail])
register_multi_item_links(['acl_detail'], [acl_grant, acl_revoke])

register_links([AccessObject], [acl_holder_new], menu_name='sidebar')

register_setup(acl_setup_valid_classes)
register_links(['acl_setup_valid_classes', 'acl_class_acl_list', 'acl_class_new_holder_for', 'acl_class_acl_detail', 'acl_class_multiple_grant', 'acl_class_multiple_revoke'], [acl_class_list], menu_name='secondary_menu')

register_links(ClassAccessHolder, [acl_class_acl_detail])

register_links(AccessObjectClass, [acl_class_acl_list, acl_class_new_holder_for])
register_multi_item_links(['acl_class_acl_detail'], [acl_class_grant, acl_class_revoke])
