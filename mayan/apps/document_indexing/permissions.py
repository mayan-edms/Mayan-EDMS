from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Indexing'), name='document_indexing')

permission_document_indexing_create = namespace.add_permission(
    label=_('Create new document indexes'), name='document_index_create'
)
permission_document_indexing_edit = namespace.add_permission(
    label=_('Edit document indexes'), name='document_index_edit'
)
permission_document_indexing_delete = namespace.add_permission(
    label=_('Delete document indexes'), name='document_index_delete'
)
permission_document_indexing_instance_view = namespace.add_permission(
    label=_('View document index instances'),
    name='document_index_instance_view'
)
permission_document_indexing_view = namespace.add_permission(
    label=_('View document indexes'), name='document_index_view'
)
permission_document_indexing_rebuild = namespace.add_permission(
    label=_('Rebuild document indexes'), name='document_rebuild_indexes'
)
