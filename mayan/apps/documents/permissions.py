from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

document_namespace = PermissionNamespace('documents', _('Documents'))

PERMISSION_DOCUMENT_CREATE = Permission.objects.register(document_namespace, 'document_create', _('Create documents'))
PERMISSION_DOCUMENT_PROPERTIES_EDIT = Permission.objects.register(document_namespace, 'document_properties_edit', _('Edit document properties'))
PERMISSION_DOCUMENT_EDIT = Permission.objects.register(document_namespace, 'document_edit', _('Edit documents'))
PERMISSION_DOCUMENT_VIEW = Permission.objects.register(document_namespace, 'document_view', _('View documents'))
PERMISSION_DOCUMENT_DELETE = Permission.objects.register(document_namespace, 'document_delete', _('Delete documents'))
PERMISSION_DOCUMENT_DOWNLOAD = Permission.objects.register(document_namespace, 'document_download', _('Download documents'))
PERMISSION_DOCUMENT_TRANSFORM = Permission.objects.register(document_namespace, 'document_transform', _('Transform documents'))
PERMISSION_DOCUMENT_TOOLS = Permission.objects.register(document_namespace, 'document_tools', _('Execute document modifying tools'))
PERMISSION_DOCUMENT_VERSION_REVERT = Permission.objects.register(document_namespace, 'document_version_revert', _('Revert documents to a previous version'))
PERMISSION_DOCUMENT_NEW_VERSION = Permission.objects.register(document_namespace, 'document_new_version', _('Create new document versions'))

documents_setup_namespace = PermissionNamespace('documents_setup', _('Documents setup'))

PERMISSION_DOCUMENT_TYPE_VIEW = Permission.objects.register(documents_setup_namespace, 'document_type_view', _('View document types'))
PERMISSION_DOCUMENT_TYPE_EDIT = Permission.objects.register(documents_setup_namespace, 'document_type_edit', _('Edit document types'))
PERMISSION_DOCUMENT_TYPE_DELETE = Permission.objects.register(documents_setup_namespace, 'document_type_delete', _('Delete document types'))
PERMISSION_DOCUMENT_TYPE_CREATE = Permission.objects.register(documents_setup_namespace, 'document_type_create', _('Create document types'))
