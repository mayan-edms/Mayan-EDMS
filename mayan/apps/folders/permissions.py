from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

folder_namespace = PermissionNamespace('folders', _('Folders'))

PERMISSION_FOLDER_CREATE = Permission.objects.register(folder_namespace, 'folder_create', _('Create new folders'))
PERMISSION_FOLDER_EDIT = Permission.objects.register(folder_namespace, 'folder_edit', _('Edit new folders'))
PERMISSION_FOLDER_DELETE = Permission.objects.register(folder_namespace, 'folder_delete', _('Delete new folders'))
PERMISSION_FOLDER_REMOVE_DOCUMENT = Permission.objects.register(folder_namespace, 'folder_remove_document', _('Remove documents from folders'))
PERMISSION_FOLDER_VIEW = Permission.objects.register(folder_namespace, 'folder_view', _('View existing folders'))
PERMISSION_FOLDER_ADD_DOCUMENT = Permission.objects.register(folder_namespace, 'folder_add_document', _('Add documents to existing folders'))
