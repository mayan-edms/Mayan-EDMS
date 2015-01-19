from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

document_indexing_namespace = PermissionNamespace('document_indexing', _('Indexing'))

PERMISSION_DOCUMENT_INDEXING_SETUP = Permission.objects.register(document_indexing_namespace, 'document_index_setup', _('Configure document indexes'))
PERMISSION_DOCUMENT_INDEXING_CREATE = Permission.objects.register(document_indexing_namespace, 'document_index_create', _('Create new document indexes'))
PERMISSION_DOCUMENT_INDEXING_EDIT = Permission.objects.register(document_indexing_namespace, 'document_index_edit', _('Edit document indexes'))
PERMISSION_DOCUMENT_INDEXING_DELETE = Permission.objects.register(document_indexing_namespace, 'document_index_delete', _('Delete document indexes'))

PERMISSION_DOCUMENT_INDEXING_VIEW = Permission.objects.register(document_indexing_namespace, 'document_index_view', _('View document indexes'))
PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES = Permission.objects.register(document_indexing_namespace, 'document_rebuild_indexes', _('Rebuild document indexes'))
