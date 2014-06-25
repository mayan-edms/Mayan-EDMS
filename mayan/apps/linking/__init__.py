from __future__ import absolute_import

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from documents.models import Document
from navigation.api import register_links, register_sidebar_template
from project_setup.api import register_setup

from .links import (smart_link_instances_for_document,
    smart_link_setup, smart_link_list, smart_link_create, smart_link_edit,
    smart_link_delete, smart_link_condition_list, smart_link_condition_create,
    smart_link_condition_edit, smart_link_condition_delete, smart_link_acl_list)
from .models import SmartLink, SmartLinkCondition
from .permissions import (PERMISSION_SMART_LINK_VIEW,
    PERMISSION_SMART_LINK_DELETE, PERMISSION_SMART_LINK_EDIT)

register_links(Document, [smart_link_instances_for_document], menu_name='form_header')

register_links(SmartLink, [smart_link_edit, smart_link_delete, smart_link_condition_list, smart_link_acl_list])
register_links([SmartLink, 'smart_link_list', 'smart_link_create'], [smart_link_list, smart_link_create], menu_name='secondary_menu')

register_links(SmartLinkCondition, [smart_link_condition_edit, smart_link_condition_delete])
register_links(['smart_link_condition_list', 'smart_link_condition_create', 'smart_link_condition_edit', 'smart_link_condition_delete'], [smart_link_condition_create], menu_name='sidebar')

register_setup(smart_link_setup)
register_sidebar_template(['smart_link_list'], 'smart_links_help.html')

class_permissions(SmartLink, [
    PERMISSION_SMART_LINK_VIEW,
    PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT,
    ACLS_EDIT_ACL,
    ACLS_VIEW_ACL
])
