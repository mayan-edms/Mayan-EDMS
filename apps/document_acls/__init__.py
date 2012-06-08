from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from navigation.api import bind_links, Link
from acls.permissions import ACLS_VIEW_ACL, ACLS_EDIT_ACL
from acls.api import class_permissions

acl_list = Link(text=_(u'ACLs'), view='document_acl_list', args='object.pk', sprite='lock', permissions=[ACLS_VIEW_ACL])

bind_links([Document], [acl_list], menu_name='form_header')

class_permissions(Document, [
    ACLS_VIEW_ACL,
    ACLS_EDIT_ACL
])
