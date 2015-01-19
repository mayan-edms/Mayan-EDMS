from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from documents.permissions import PERMISSION_DOCUMENT_VIEW

from .permissions import (
    PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_CREATE,
    PERMISSION_FOLDER_DELETE, PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_VIEW,
    PERMISSION_FOLDER_REMOVE_DOCUMENT
)

folder_list = {'text': _('Folders'), 'view': 'folders:folder_list', 'famfam': 'folder_user'}
folder_create = {'text': _('Create folder'), 'view': 'folders:folder_create', 'famfam': 'folder_add', 'permissions': [PERMISSION_FOLDER_CREATE]}
folder_edit = {'text': _('Edit'), 'view': 'folders:folder_edit', 'args': 'object.pk', 'famfam': 'folder_edit', 'permissions': [PERMISSION_FOLDER_EDIT]}
folder_delete = {'text': _('Delete'), 'view': 'folders:folder_delete', 'args': 'object.pk', 'famfam': 'folder_delete', 'permissions': [PERMISSION_FOLDER_DELETE]}
folder_document_multiple_remove = {'text': _('Remove from folder'), 'view': 'folders:folder_document_multiple_remove', 'args': 'object.pk', 'famfam': 'folder_delete', 'permissions': [PERMISSION_FOLDER_REMOVE_DOCUMENT]}
folder_view = {'text': _('Documents'), 'view': 'folders:folder_view', 'args': 'object.pk', 'famfam': 'page', 'permissions': [PERMISSION_FOLDER_VIEW]}
folder_add_document = {'text': _('Add to a folder'), 'view': 'folders:folder_add_document', 'args': 'object.pk', 'famfam': 'folder_add', 'permissions': [PERMISSION_FOLDER_ADD_DOCUMENT]}
folder_add_multiple_documents = {'text': _('Add to folder'), 'view': 'folders:folder_add_multiple_documents', 'famfam': 'folder_add'}
document_folder_list = {'text': _('Folders'), 'view': 'folders:document_folder_list', 'args': 'object.pk', 'famfam': 'folder_user', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

folder_acl_list = {'text': _('ACLs'), 'view': 'folders:folder_acl_list', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
folders_main_menu_link = {'text': _('Folders'), 'famfam': 'folder_user', 'view': 'folders:folder_list'}
