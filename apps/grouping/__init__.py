from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links

from documents.literals import PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_VIEW

document_group_link = {'text': _(u'group actions'), 'view': 'document_group_view', 'famfam': 'page_go', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_group_back_to_document = {'text': _(u'return to document'), 'view': 'document_view_simple', 'args': 'ref_object.id', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_group_create_sibling = {'text': _(u'upload new document using same metadata'), 'view': 'document_create_sibling', 'args': 'ref_object.id', 'famfam': 'page_copy', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}

register_links(['document_group_view'], [document_group_back_to_document, document_group_create_sibling], menu_name='sidebar')
