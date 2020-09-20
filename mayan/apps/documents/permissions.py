from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Documents'), name='documents')

# Document
permission_document_create = namespace.add_permission(
    label=_('Create documents'), name='document_create'
)
permission_document_delete = namespace.add_permission(
    label=_('Delete documents'), name='document_delete'
)
permission_document_edit = namespace.add_permission(
    label=_('Edit documents'), name='document_edit'
)
permission_document_properties_edit = namespace.add_permission(
    label=_('Edit document properties'), name='document_properties_edit'
)
permission_document_print = namespace.add_permission(
    label=_('Print documents'), name='document_print'
)
permission_document_tools = namespace.add_permission(
    label=_('Execute document modifying tools'), name='document_tools'
)
permission_document_view = namespace.add_permission(
    label=_('View documents'), name='document_view'
)

# Document file
permission_document_file_delete = namespace.add_permission(
    label=_('Delete document files'), name='document_file_delete'
)
permission_document_file_download = namespace.add_permission(
    label=_('Download document files'), name='document_file_download'
)
permission_document_file_new = namespace.add_permission(
    label=_('Create new document files'), name='document_file_new'
)
permission_document_file_view = namespace.add_permission(
    label=_('View document files'),
    name='document_file_view'
)
permission_document_file_tools = namespace.add_permission(
    label=_('Execute document file modifying tools'),
    name='document_file_tools'
)

# Document version
permission_document_version_delete = namespace.add_permission(
    label=_('Delete document versions'),
    name='document_version_delete'
)
permission_document_version_view = namespace.add_permission(
    label=_('View document versions'),
    name='document_version_view'
)

# Trashed document
permission_document_restore = namespace.add_permission(
    label=_('Restore trashed document'), name='document_restore'
)
permission_document_trash = namespace.add_permission(
    label=_('Trash documents'), name='document_trash'
)

permission_empty_trash = namespace.add_permission(
    label=_('Empty trash'), name='document_empty_trash'
)

setup_namespace = PermissionNamespace(
    label=_('Document types'), name='documents_types'
)

permission_document_type_create = setup_namespace.add_permission(
    label=_('Create document types'), name='document_type_create'
)
permission_document_type_delete = setup_namespace.add_permission(
    label=_('Delete document types'), name='document_type_delete'
)
permission_document_type_edit = setup_namespace.add_permission(
    label=_('Edit document types'), name='document_type_edit'
)
permission_document_type_view = setup_namespace.add_permission(
    label=_('View document types'), name='document_type_view'
)


