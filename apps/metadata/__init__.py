from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from permissions.api import register_permission
from documents.models import Document

PERMISSION_METADATA_DOCUMENT_EDIT = {'namespace': 'metadata', 'name': u'metadata_document_edit', 'label': _(u'Edit a document\'s metadata')}
PERMISSION_METADATA_DOCUMENT_ADD = {'namespace': 'metadata', 'name': u'metadata_document_add', 'label': _(u'Add metadata to a document')}
PERMISSION_METADATA_DOCUMENT_REMOVE = {'namespace': 'metadata', 'name': u'metadata_document_remove', 'label': _(u'Remove metadata from a document')}

register_permission(PERMISSION_METADATA_DOCUMENT_EDIT)
register_permission(PERMISSION_METADATA_DOCUMENT_ADD)
register_permission(PERMISSION_METADATA_DOCUMENT_REMOVE)

metadata_edit = {'text': _(u'edit metadata'), 'view': 'metadata_edit', 'args': 'object.id', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_multiple_edit = {'text': _(u'edit metadata'), 'view': 'metadata_multiple_edit', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_add = {'text': _(u'add metadata'), 'view': 'metadata_add', 'args': 'object.id', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_multiple_add = {'text': _(u'add metadata'), 'view': 'metadata_multiple_add', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_remove = {'text': _(u'remove metadata'), 'view': 'metadata_remove', 'args': 'object.id', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}
metadata_multiple_remove = {'text': _(u'remove metadata'), 'view': 'metadata_multiple_remove', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}

register_links(Document, [metadata_add, metadata_edit, metadata_remove])
register_multi_item_links(['document_datagroup_view', 'document_list', 'document_list_recent'], [metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove])
