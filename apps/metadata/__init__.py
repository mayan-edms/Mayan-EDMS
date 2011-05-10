from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
from main.api import register_diagnostic, register_tool
from permissions.api import register_permissions

from documents.models import Document

PERMISSION_METADATA_DOCUMENT_EDIT = u'metadata_document_edit'
PERMISSION_METADATA_DOCUMENT_ADD = u'metadata_document_add'
PERMISSION_METADATA_DOCUMENT_REMOVE = u'metadata_document_remove'

register_permissions('metadata', [
    {'name': PERMISSION_METADATA_DOCUMENT_EDIT, 'label': _(u'Edit a document\'s metadata')},
    {'name': PERMISSION_METADATA_DOCUMENT_ADD, 'label': _(u'Add metadata to a document')},
    {'name': PERMISSION_METADATA_DOCUMENT_REMOVE, 'label': _(u'Remove metadata from a document')},
])

metadata_edit = {'text': _(u'edit metadata'), 'view': 'metadata_edit', 'args': 'object.id', 'famfam': 'xhtml_go', 'permissions': {'namespace': 'metadata', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}}
metadata_multiple_edit = {'text': _(u'edit metadata'), 'view': 'metadata_multiple_edit', 'famfam': 'xhtml_go', 'permissions': {'namespace': 'metadata', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}}
metadata_add = {'text': _(u'add metadata'), 'view': 'metadata_add', 'args': 'object.id', 'famfam': 'xhtml_add', 'permissions': {'namespace': 'metadata', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}}
metadata_multiple_add = {'text': _(u'add metadata'), 'view': 'metadata_multiple_add', 'famfam': 'xhtml_add', 'permissions': {'namespace': 'metadata', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}}
metadata_remove = {'text': _(u'remove metadata'), 'view': 'metadata_remove', 'args': 'object.id', 'famfam': 'xhtml_delete', 'permissions': {'namespace': 'metadata', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}}
metadata_multiple_remove = {'text': _(u'remove metadata'), 'view': 'metadata_multiple_remove', 'famfam': 'xhtml_delete', 'permissions': {'namespace': 'metadata', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}}

register_links(Document, [metadata_add, metadata_edit, metadata_remove])
register_multi_item_links(['metadatagroup_view', 'document_list', 'document_list_recent'], [metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove])
