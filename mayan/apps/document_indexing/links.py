from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from documents.permissions import PERMISSION_DOCUMENT_VIEW

from .permissions import (
    PERMISSION_DOCUMENT_INDEXING_CREATE, PERMISSION_DOCUMENT_INDEXING_EDIT,
    PERMISSION_DOCUMENT_INDEXING_DELETE,
    PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES,
    PERMISSION_DOCUMENT_INDEXING_SETUP, PERMISSION_DOCUMENT_INDEXING_VIEW
)


def is_not_instance_root_node(context):
    return not context['object'].is_root_node()


def is_not_root_node(context):
    return not context['node'].is_root_node()


index_setup = {'text': _('Indexes'), 'view': 'indexing:index_setup_list', 'icon': 'main/icons/tab.png', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP]}
index_setup_list = {'text': _('Indexes'), 'view': 'indexing:index_setup_list', 'famfam': 'tab', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP]}
index_setup_create = {'text': _('Create index'), 'view': 'indexing:index_setup_create', 'famfam': 'tab_add', 'permissions': [PERMISSION_DOCUMENT_INDEXING_CREATE]}
index_setup_edit = {'text': _('Edit'), 'view': 'indexing:index_setup_edit', 'args': 'index.pk', 'famfam': 'tab_edit', 'permissions': [PERMISSION_DOCUMENT_INDEXING_EDIT]}
index_setup_delete = {'text': _('Delete'), 'view': 'indexing:index_setup_delete', 'args': 'index.pk', 'famfam': 'tab_delete', 'permissions': [PERMISSION_DOCUMENT_INDEXING_DELETE]}
index_setup_view = {'text': _('Tree template'), 'view': 'indexing:index_setup_view', 'args': 'index.pk', 'famfam': 'textfield', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP]}
index_setup_document_types = {'text': _('Document types'), 'view': 'indexing:index_setup_document_types', 'args': 'index.pk', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_INDEXING_EDIT]}

template_node_create = {'text': _('New child node'), 'view': 'indexing:template_node_create', 'args': 'node.pk', 'famfam': 'textfield_add', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP]}
template_node_edit = {'text': _('Edit'), 'view': 'indexing:template_node_edit', 'args': 'node.pk', 'famfam': 'textfield', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP], 'condition': is_not_root_node}
template_node_delete = {'text': _('Delete'), 'view': 'indexing:template_node_delete', 'args': 'node.pk', 'famfam': 'textfield_delete', 'permissions': [PERMISSION_DOCUMENT_INDEXING_SETUP], 'condition': is_not_root_node}

index_list = {'text': _('Index list'), 'view': 'indexing:index_list', 'famfam': 'tab', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW]}

index_parent = {'text': _('Go up one level'), 'view': 'indexing:index_instance_node_view', 'args': 'object.parent.pk', 'famfam': 'arrow_up', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW], 'dont_mark_active': True, 'condition': is_not_instance_root_node}
document_index_list = {'text': _('Indexes'), 'view': 'indexing:document_index_list', 'args': 'object.pk', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW, PERMISSION_DOCUMENT_VIEW]}

document_index_main_menu_link = {'text': _('Indexes'), 'famfam': 'tab', 'view': 'indexing:index_list'}

rebuild_index_instances = {'text': _('Rebuild indexes'), 'view': 'indexing:rebuild_index_instances', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES], 'description': _('Deletes and creates from scratch all the document indexes.')}
