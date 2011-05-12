from django.utils.translation import ugettext_lazy as _
#from django.core.urlresolvers import reverse
#from django.conf import settings

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from main.api import register_diagnostic, register_tool
from permissions.api import register_permissions
from tags.widgets import get_tags_inline_widget_simple

#from documents.models import Document, DocumentPage, DocumentPageTransformation
#from documents.staging import StagingFile
#from documents.conf.settings import ENABLE_SINGLE_DOCUMENT_UPLOAD
from documents.literals import PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_VIEW
#from documents import document_multiple_clear_transformations

document_group_link = {'text': _(u'group actions'), 'view': 'document_group_view', 'famfam': 'page_go', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_group_back_to_document = {'text': _(u'return to document'), 'view': 'document_view_simple', 'args': 'ref_object.id', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
document_group_create_sibling = {'text': _(u'upload new document using same metadata'), 'view': 'document_create_sibling', 'args': 'ref_object.id', 'famfam': 'page_copy', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}

#register_multi_item_links(['document_group_view'], [document_multiple_clear_transformations, document_multiple_delete])

register_links(['document_group_view'], [document_group_back_to_document, document_group_create_sibling], menu_name='sidebar')
