from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from documents.models import Document
from navigation.api import bind_links, register_sidebar_template

from .links import (smart_link_instances_for_document,
    smart_link_list, smart_link_create, smart_link_edit,
    smart_link_delete, smart_link_condition_list, smart_link_condition_create,
    smart_link_condition_edit, smart_link_condition_delete, smart_link_acl_list)
from .models import SmartLink, SmartLinkCondition
from .permissions import (PERMISSION_SMART_LINK_VIEW,
    PERMISSION_SMART_LINK_DELETE, PERMISSION_SMART_LINK_EDIT)

bind_links([Document], [smart_link_instances_for_document], menu_name='form_header')
bind_links([SmartLink], [smart_link_edit, smart_link_delete, smart_link_condition_list, smart_link_acl_list])
bind_links([SmartLink, 'smart_link_list', 'smart_link_create'], [smart_link_list, smart_link_create], menu_name='secondary_menu')

bind_links([SmartLinkCondition], [smart_link_condition_edit, smart_link_condition_delete])
bind_links(['smart_link_condition_list', 'smart_link_condition_create', 'smart_link_condition_edit', 'smart_link_condition_delete'], [smart_link_condition_create], menu_name='sidebar')

register_sidebar_template(['smart_link_list'], 'smart_links_help.html')

class_permissions(SmartLink, [
    PERMISSION_SMART_LINK_VIEW,
    PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT,
    ACLS_EDIT_ACL,
    ACLS_VIEW_ACL
])
