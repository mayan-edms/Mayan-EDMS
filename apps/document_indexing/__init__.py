from django.utils.translation import ugettext_lazy as _

from navigation.api import register_menu
from permissions.api import register_permission, set_namespace_title
from main.api import register_tool

PERMISSION_DOCUMENT_INDEXING_VIEW = {'namespace': 'document_indexing', 'name': 'document_index_view', 'label': _(u'View document indexes')}
PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES = {'namespace': 'document_indexing', 'name': 'document_rebuild_indexes', 'label': _(u'Rebuild document indexes')}

set_namespace_title('document_indexing', _(u'indexing'))
register_permission(PERMISSION_DOCUMENT_INDEXING_VIEW)
register_permission(PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES)

index_list = {'text': _(u'index list'), 'view': 'index_instance_list', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW]}

register_menu([
    {'text': _('indexes'), 'view': 'index_instance_list', 'links': [
    ], 'famfam': 'folder_link', 'position': 2, 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW]}])

rebuild_index_instances = {'text': _('rebuild indexes'), 'view': 'rebuild_index_instances', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES], 'description': _(u'Deletes and creates from scratch all the document indexes.')}

register_tool(rebuild_index_instances, namespace='document_indexing', title=_(u'Indexes'))
