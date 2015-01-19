from __future__ import unicode_literals

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from documents.models import Document
from navigation.api import register_links
from project_setup.api import register_setup

from .classes import ResolvedSmartLink
from .links import (
    smart_link_acl_list, smart_link_create, smart_link_condition_create,
    smart_link_condition_delete, smart_link_condition_edit,
    smart_link_condition_list, smart_link_delete, smart_link_document_types,
    smart_link_edit, smart_link_instance_view,
    smart_link_instances_for_document, smart_link_list, smart_link_setup
)
from .models import SmartLink, SmartLinkCondition
from .permissions import (
    PERMISSION_SMART_LINK_DELETE, PERMISSION_SMART_LINK_EDIT,
    PERMISSION_SMART_LINK_VIEW
)

register_links(Document, [smart_link_instances_for_document], menu_name='form_header')
register_links(SmartLink, [smart_link_edit, smart_link_document_types, smart_link_condition_list, smart_link_acl_list, smart_link_delete])
register_links([SmartLink, 'linking:smart_link_list', 'linking:smart_link_create'], [smart_link_list, smart_link_create], menu_name='secondary_menu')
register_links(SmartLinkCondition, [smart_link_condition_edit, smart_link_condition_delete])
register_links(ResolvedSmartLink, [smart_link_instance_view])
register_links(['linking:smart_link_condition_list', 'linking:smart_link_condition_create', 'linking:smart_link_condition_edit', 'linking:smart_link_condition_delete'], [smart_link_condition_create], menu_name='sidebar')

register_setup(smart_link_setup)

class_permissions(SmartLink, [
    ACLS_EDIT_ACL, ACLS_VIEW_ACL, PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT, PERMISSION_SMART_LINK_VIEW
])
