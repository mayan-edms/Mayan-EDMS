from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

metadata_namespace = PermissionNamespace('metadata', _('Metadata'))
PERMISSION_METADATA_DOCUMENT_EDIT = Permission.objects.register(metadata_namespace, 'metadata_document_edit', _('Edit a document\'s metadata'))
PERMISSION_METADATA_DOCUMENT_ADD = Permission.objects.register(metadata_namespace, 'metadata_document_add', _('Add metadata to a document'))
PERMISSION_METADATA_DOCUMENT_REMOVE = Permission.objects.register(metadata_namespace, 'metadata_document_remove', _('Remove metadata from a document'))
PERMISSION_METADATA_DOCUMENT_VIEW = Permission.objects.register(metadata_namespace, 'metadata_document_view', _('View metadata from a document'))

metadata_setup_namespace = PermissionNamespace('metadata_setup', _('Metadata setup'))
PERMISSION_METADATA_TYPE_EDIT = Permission.objects.register(metadata_setup_namespace, 'metadata_type_edit', _('Edit metadata types'))
PERMISSION_METADATA_TYPE_CREATE = Permission.objects.register(metadata_setup_namespace, 'metadata_type_create', _('Create new metadata types'))
PERMISSION_METADATA_TYPE_DELETE = Permission.objects.register(metadata_setup_namespace, 'metadata_type_delete', _('Delete metadata types'))
PERMISSION_METADATA_TYPE_VIEW = Permission.objects.register(metadata_setup_namespace, 'metadata_type_view', _('View metadata types'))
