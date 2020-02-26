from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Metadata'), name='metadata')

permission_metadata_add = namespace.add_permission(
    label=_('Add metadata to a document'), name='metadata_document_add'
)
permission_metadata_edit = namespace.add_permission(
    label=_('Edit a document\'s metadata'), name='metadata_document_edit'
)
permission_metadata_remove = namespace.add_permission(
    label=_('Remove metadata from a document'),
    name='metadata_document_remove'
)
permission_metadata_view = namespace.add_permission(
    label=_('View metadata from a document'), name='metadata_document_view'
)

setup_namespace = PermissionNamespace(
    label=_('Metadata setup'), name='metadata_setup'
)

permission_metadata_type_edit = setup_namespace.add_permission(
    label=_('Edit metadata types'), name='metadata_type_edit'
)
permission_metadata_type_create = setup_namespace.add_permission(
    label=_('Create new metadata types'), name='metadata_type_create'
)
permission_metadata_type_delete = setup_namespace.add_permission(
    label=_('Delete metadata types'), name='metadata_type_delete'
)
permission_metadata_type_view = setup_namespace.add_permission(
    label=_('View metadata types'), name='metadata_type_view'
)
