from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Documents'), name='documents')

permission_document_create = namespace.add_permission(
    label=_('Create documents'), name='document_create'
)
permission_document_delete = namespace.add_permission(
    label=_('Delete documents'), name='document_delete'
)
permission_document_trash = namespace.add_permission(
    label=_('Trash documents'), name='document_trash'
)
permission_document_download = namespace.add_permission(
    label=_('Download documents'), name='document_download'
)
permission_document_edit = namespace.add_permission(
    label=_('Edit documents'), name='document_edit'
)
permission_document_new_version = namespace.add_permission(
    label=_('Create new document versions'), name='document_new_version'
)
permission_document_properties_edit = namespace.add_permission(
    label=_('Edit document properties'), name='document_properties_edit'
)
permission_document_print = namespace.add_permission(
    label=_('Print documents'), name='document_print'
)
permission_document_restore = namespace.add_permission(
    label=_('Restore trashed document'), name='document_restore'
)
permission_document_tools = namespace.add_permission(
    label=_('Execute document modifying tools'), name='document_tools'
)
permission_document_version_revert = namespace.add_permission(
    label=_('Revert documents to a previous version'),
    name='document_version_revert'
)
permission_document_version_view = namespace.add_permission(
    label=_('View documents\' versions list'),
    name='document_version_view'
)
permission_document_view = namespace.add_permission(
    label=_('View documents'), name='document_view'
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
