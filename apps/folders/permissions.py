from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

folder_namespace = PermissionNamespace('folders', _(u'Folders'))

PERMISSION_FOLDER_CREATE = Permission.objects.register(folder_namespace, 'folder_create', _(u'Create new folders'))
PERMISSION_FOLDER_EDIT = Permission.objects.register(folder_namespace, 'folder_edit', _(u'Edit new folders'))
PERMISSION_FOLDER_DELETE = Permission.objects.register(folder_namespace, 'folder_delete', _(u'Delete new folders'))
PERMISSION_FOLDER_REMOVE_DOCUMENT = Permission.objects.register(folder_namespace, 'folder_remove_document', _(u'Remove documents from folders'))
PERMISSION_FOLDER_VIEW = Permission.objects.register(folder_namespace, 'folder_view', _(u'View existing folders'))
PERMISSION_FOLDER_ADD_DOCUMENT = Permission.objects.register(folder_namespace, 'folder_add_document', _(u'Add documents to existing folders'))
