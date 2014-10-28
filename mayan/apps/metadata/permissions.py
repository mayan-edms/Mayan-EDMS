from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import Permission, PermissionNamespace

metadata_namespace = PermissionNamespace('metadata', _(u'Metadata'))
PERMISSION_METADATA_DOCUMENT_EDIT = Permission.objects.register(metadata_namespace, 'metadata_document_edit', _(u'Edit a document\'s metadata'))
PERMISSION_METADATA_DOCUMENT_VIEW = Permission.objects.register(metadata_namespace, 'metadata_document_view', _(u'View metadata from a document'))

metadata_setup_namespace = PermissionNamespace('metadata_setup', _(u'Metadata setup'))
PERMISSION_METADATA_TYPE_EDIT = Permission.objects.register(metadata_setup_namespace, 'metadata_type_edit', _(u'Edit metadata types'))
PERMISSION_METADATA_TYPE_CREATE = Permission.objects.register(metadata_setup_namespace, 'metadata_type_create', _(u'Create new metadata types'))
PERMISSION_METADATA_TYPE_DELETE = Permission.objects.register(metadata_setup_namespace, 'metadata_type_delete', _(u'Delete metadata types'))
PERMISSION_METADATA_TYPE_VIEW = Permission.objects.register(metadata_setup_namespace, 'metadata_type_view', _(u'View metadata types'))
