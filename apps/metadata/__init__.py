from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links, \
    register_sidebar_template
from permissions.api import register_permission, set_namespace_title
from documents.models import Document, DocumentType
from documents.literals import PERMISSION_DOCUMENT_TYPE_EDIT
from metadata.models import MetadataType, MetadataSet

PERMISSION_METADATA_DOCUMENT_EDIT = {'namespace': 'metadata', 'name': u'metadata_document_edit', 'label': _(u'Edit a document\'s metadata')}
PERMISSION_METADATA_DOCUMENT_ADD = {'namespace': 'metadata', 'name': u'metadata_document_add', 'label': _(u'Add metadata to a document')}
PERMISSION_METADATA_DOCUMENT_REMOVE = {'namespace': 'metadata', 'name': u'metadata_document_remove', 'label': _(u'Remove metadata from a document')}
PERMISSION_METADATA_DOCUMENT_VIEW = {'namespace': 'metadata', 'name': u'metadata_document_view', 'label': _(u'View metadata from a document')}

PERMISSION_METADATA_TYPE_EDIT = {'namespace': 'metadata_setup', 'name': u'metadata_type_edit', 'label': _(u'Edit metadata types')}
PERMISSION_METADATA_TYPE_CREATE = {'namespace': 'metadata_setup', 'name': u'metadata_type_create', 'label': _(u'Create new metadata types')}
PERMISSION_METADATA_TYPE_DELETE = {'namespace': 'metadata_setup', 'name': u'metadata_type_delete', 'label': _(u'Delete metadata types')}
PERMISSION_METADATA_TYPE_VIEW = {'namespace': 'metadata_setup', 'name': u'metadata_type_view', 'label': _(u'View metadata types')}

PERMISSION_METADATA_SET_EDIT = {'namespace': 'metadata_setup', 'name': u'metadata_set_edit', 'label': _(u'Edit metadata sets')}
PERMISSION_METADATA_SET_CREATE = {'namespace': 'metadata_setup', 'name': u'metadata_set_create', 'label': _(u'Create new metadata sets')}
PERMISSION_METADATA_SET_DELETE = {'namespace': 'metadata_setup', 'name': u'metadata_set_delete', 'label': _(u'Delete metadata sets')}
PERMISSION_METADATA_SET_VIEW = {'namespace': 'metadata_setup', 'name': u'metadata_set_view', 'label': _(u'View metadata sets')}

set_namespace_title('metadata', _(u'Metadata'))
register_permission(PERMISSION_METADATA_DOCUMENT_EDIT)
register_permission(PERMISSION_METADATA_DOCUMENT_ADD)
register_permission(PERMISSION_METADATA_DOCUMENT_REMOVE)
register_permission(PERMISSION_METADATA_DOCUMENT_VIEW)

set_namespace_title('metadata_setup', _(u'Metadata setup'))
register_permission(PERMISSION_METADATA_TYPE_EDIT)
register_permission(PERMISSION_METADATA_TYPE_CREATE)
register_permission(PERMISSION_METADATA_TYPE_DELETE)
register_permission(PERMISSION_METADATA_TYPE_VIEW)

register_permission(PERMISSION_METADATA_SET_EDIT)
register_permission(PERMISSION_METADATA_SET_CREATE)
register_permission(PERMISSION_METADATA_SET_DELETE)
register_permission(PERMISSION_METADATA_SET_VIEW)

metadata_edit = {'text': _(u'edit metadata'), 'view': 'metadata_edit', 'args': 'object.pk', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_view = {'text': _(u'metadata'), 'view': 'metadata_view', 'args': 'object.pk', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT], 'children_view_regex': ['metadata']}
metadata_multiple_edit = {'text': _(u'edit metadata'), 'view': 'metadata_multiple_edit', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_add = {'text': _(u'add metadata'), 'view': 'metadata_add', 'args': 'object.pk', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_multiple_add = {'text': _(u'add metadata'), 'view': 'metadata_multiple_add', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_remove = {'text': _(u'remove metadata'), 'view': 'metadata_remove', 'args': 'object.pk', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}
metadata_multiple_remove = {'text': _(u'remove metadata'), 'view': 'metadata_multiple_remove', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}

setup_metadata_type_list = {'text': _(u'metadata types'), 'view': 'setup_metadata_type_list', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_TYPE_VIEW], 'children_view_regex': ['setup_metadata_type']}
setup_metadata_type_edit = {'text': _(u'edit'), 'view': 'setup_metadata_type_edit', 'args': 'object.pk', 'famfam': 'xhtml', 'permissions': [PERMISSION_METADATA_TYPE_EDIT]}
setup_metadata_type_delete = {'text': _(u'delete'), 'view': 'setup_metadata_type_delete', 'args': 'object.pk', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_TYPE_DELETE]}
setup_metadata_type_create = {'text': _(u'create new'), 'view': 'setup_metadata_type_create', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_TYPE_CREATE]}

setup_metadata_set_list = {'text': _(u'metadata sets'), 'view': 'setup_metadata_set_list', 'famfam': 'table', 'permissions': [PERMISSION_METADATA_SET_VIEW], 'children_view_regex': ['setup_metadata_set']}
setup_metadata_set_edit = {'text': _(u'edit'), 'view': 'setup_metadata_set_edit', 'args': 'object.pk', 'famfam': 'table_edit', 'permissions': [PERMISSION_METADATA_SET_EDIT]}
setup_metadata_set_delete = {'text': _(u'delete'), 'view': 'setup_metadata_set_delete', 'args': 'object.pk', 'famfam': 'table_delete', 'permissions': [PERMISSION_METADATA_SET_DELETE]}
setup_metadata_set_create = {'text': _(u'create new'), 'view': 'setup_metadata_set_create', 'famfam': 'table_add', 'permissions': [PERMISSION_METADATA_SET_CREATE]}

setup_document_type_metadata = {'text': _(u'default metadata'), 'view': 'setup_document_type_metadata', 'args': 'document_type.pk', 'famfam': 'xhtml', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}

#register_links(Document, [metadata_add, metadata_edit, metadata_remove])
register_links(['metadata_add', 'metadata_edit', 'metadata_remove', 'metadata_view'], [metadata_add, metadata_edit, metadata_remove], menu_name='sidebar')
register_links(Document, [metadata_view], menu_name='form_header')  #, metadata_edit, metadata_remove])
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_list', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent'], [metadata_multiple_add, metadata_multiple_edit, metadata_multiple_remove])

register_links(MetadataType, [setup_metadata_type_edit, setup_metadata_type_delete])
register_links(['setup_metadata_type_delete', 'setup_metadata_type_edit', 'setup_metadata_type_list', 'setup_metadata_type_create'], [setup_metadata_type_create], menu_name='sidebar')

register_links(MetadataSet, [setup_metadata_set_edit, setup_metadata_set_delete])
register_links(['setup_metadata_set_delete', 'setup_metadata_set_edit', 'setup_metadata_set_list', 'setup_metadata_set_create'], [setup_metadata_set_create], menu_name='sidebar')

register_links(DocumentType, [setup_document_type_metadata])

metadata_type_setup_views = ['setup_metadata_type_list', 'setup_metadata_type_edit', 'setup_metadata_type_delete', 'setup_metadata_type_create']
metadata_set_setup_views = ['setup_metadata_set_list', 'setup_metadata_set_edit', 'setup_metadata_set_delete', 'setup_metadata_set_create']

register_sidebar_template(['setup_metadata_type_list'], 'metadata_type_help.html')
register_sidebar_template(['setup_metadata_set_list'], 'metadata_set_help.html')
