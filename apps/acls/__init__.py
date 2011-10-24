from django.utils.translation import ugettext_lazy as _

#from documents.models import Document
from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup

from permissions.api import register_permission, set_namespace_title


ACLS_EDIT_ACL = {'namespace': 'acls', 'name': 'acl_edit', 'label': _(u'Edit ACLs')}
ACLS_VIEW_ACL = {'namespace': 'acls', 'name': 'acl_view', 'label': _(u'View ACLs')}

set_namespace_title('acls', _(u'Access control lists'))
register_permission(ACLS_EDIT_ACL)
register_permission(ACLS_VIEW_ACL)

acl_list = {'text': _(u'ACLs'), 'view': 'acl_list', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}



#register_links(Document, [acl_list], menu_name='form_header')
