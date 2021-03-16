from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Indexing'), name='document_indexing')

permission_index_instance_view = namespace.add_permission(
    label=_('View index instances'), name='document_index_instance_view'
)
permission_index_template_create = namespace.add_permission(
    label=_('Create new index templates'), name='document_index_create'
)
permission_index_template_edit = namespace.add_permission(
    label=_('Edit index templates'), name='document_index_edit'
)
permission_index_template_delete = namespace.add_permission(
    label=_('Delete index templates'), name='document_index_delete'
)
permission_index_template_view = namespace.add_permission(
    label=_('View index templates'), name='document_index_view'
)
permission_index_template_rebuild = namespace.add_permission(
    label=_('Rebuild index templates'), name='document_rebuild_indexes'
)
