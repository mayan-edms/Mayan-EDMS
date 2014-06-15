from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

document_indexing_namespace = PermissionNamespace('document_indexing', _(u'Indexing'))

PERMISSION_DOCUMENT_INDEXING_SETUP = Permission.objects.register(document_indexing_namespace, 'document_index_setup', _(u'Configure document indexes'))
PERMISSION_DOCUMENT_INDEXING_CREATE = Permission.objects.register(document_indexing_namespace, 'document_index_create', _(u'Create new document indexes'))
PERMISSION_DOCUMENT_INDEXING_EDIT = Permission.objects.register(document_indexing_namespace, 'document_index_edit', _(u'Edit document indexes'))
PERMISSION_DOCUMENT_INDEXING_DELETE = Permission.objects.register(document_indexing_namespace, 'document_index_delete', _(u'Delete document indexes'))

PERMISSION_DOCUMENT_INDEXING_VIEW = Permission.objects.register(document_indexing_namespace, 'document_index_view', _(u'View document indexes'))
PERMISSION_DOCUMENT_INDEXING_REBUILD_INDEXES = Permission.objects.register(document_indexing_namespace, 'document_rebuild_indexes', _(u'Rebuild document indexes'))
