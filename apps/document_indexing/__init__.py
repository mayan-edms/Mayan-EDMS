from django.utils.translation import ugettext_lazy as _

from navigation.api import register_menu
from permissions.api import register_permissions
from main.api import register_tool

PERMISSION_DOCUMENT_INDEXING_VIEW = 'document_index_view'
PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES = 'document_rebuild_indexes'

register_permissions('document_indexing', [
    {'name': PERMISSION_DOCUMENT_INDEXING_VIEW, 'label': _(u'View document indexes')},
    {'name': PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES, 'label': _(u'Rebuild document indexes')},
])

index_list = {'text': _(u'index list'), 'view': 'index_instance_list', 'famfam': 'folder_link', 'permissions': {'namespace': 'document_indexing', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW]}}

register_menu([
    {'text': _('indexes'), 'view': 'index_instance_list', 'links': [
    ], 'famfam': 'folder_link', 'position': 2, 'permissions': {'namespace': 'document_indexing', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW]}}])

rebuild_index_instances = {'text': _('rebuild indexes'), 'view': 'rebuild_index_instances', 'famfam': 'folder_link', 'permissions': {'namespace': 'document_indexing', 'permissions': [PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES]}, 'description': _(u'Deletes and creates from scratch all the document indexes.')}

register_tool(rebuild_index_instances, namespace='document_indexing', title=_(u'Indexes'))
