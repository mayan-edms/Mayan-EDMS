from __future__ import unicode_literals

from acls.api import class_permissions
from acls.permissions import ACLS_VIEW_ACL, ACLS_EDIT_ACL
from documents.models import Document
from navigation.api import register_links

from .links import acl_list

register_links(Document, [acl_list], menu_name='form_header')

class_permissions(Document, [
    ACLS_VIEW_ACL,
    ACLS_EDIT_ACL
])
