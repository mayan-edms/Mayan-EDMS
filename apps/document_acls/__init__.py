from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup
from acls import ACLS_VIEW_ACL

acl_list = {'text': _(u'ACLs'), 'view': 'document_acl_list', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
document_new_holder = {'text': _(u'New holder'), 'view': 'document_new_holder', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}

register_links(Document, [acl_list], menu_name='form_header')

register_links(['document_acl_list', 'document_new_holder'], [document_new_holder], menu_name='sidebar')
