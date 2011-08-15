from django.utils.translation import ugettext_lazy as _

from navigation.api import register_top_menu, register_sidebar_template, \
    register_links
from permissions.api import register_permission, set_namespace_title
from main.api import register_tool
from documents.literals import PERMISSION_DOCUMENT_VIEW
from documents.models import Document

from document_indexing.models import IndexInstance

PERMISSION_DOCUMENT_INDEXING_VIEW = {'namespace': 'document_indexing', 'name': 'document_index_view', 'label': _(u'View document indexes')}
PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES = {'namespace': 'document_indexing', 'name': 'document_rebuild_indexes', 'label': _(u'Rebuild document indexes')}

set_namespace_title('document_indexing', _(u'Indexing'))
register_permission(PERMISSION_DOCUMENT_INDEXING_VIEW)
register_permission(PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES)

index_list = {'text': _(u'index list'), 'view': 'index_instance_list', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW]}
index_parent = {'text': _(u'go up one level'), 'view': 'index_instance_list', 'args': 'object.parent.pk', 'famfam': 'arrow_up', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW], 'dont_mark_active': True}
document_index_list = {'text': _(u'indexes'), 'view': 'document_index_list', 'args': 'object.pk', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_VIEW, PERMISSION_DOCUMENT_VIEW]}

register_top_menu('indexes', link={'text': _('indexes'), 'famfam': 'folder_page', 'view': 'index_instance_list'})

rebuild_index_instances = {'text': _('rebuild indexes'), 'view': 'rebuild_index_instances', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES], 'description': _(u'Deletes and creates from scratch all the document indexes.')}

register_tool(rebuild_index_instances, namespace='document_indexing', title=_(u'Indexes'))

register_sidebar_template(['index_instance_list'], 'indexing_help.html')

register_links(IndexInstance, [index_parent])

register_links(Document, [document_index_list], menu_name='form_header')
