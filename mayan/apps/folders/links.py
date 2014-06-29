from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from documents.permissions import PERMISSION_DOCUMENT_VIEW

from .permissions import (PERMISSION_FOLDER_CREATE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_REMOVE_DOCUMENT, PERMISSION_FOLDER_VIEW,
    PERMISSION_FOLDER_ADD_DOCUMENT)

folder_list = {'text': _(u'folder list'), 'view': 'folder_list', 'famfam': 'folder_user'}
folder_create = {'text': _('create folder'), 'view': 'folder_create', 'famfam': 'folder_add', 'permissions': [PERMISSION_FOLDER_CREATE]}
folder_edit = {'text': _('edit'), 'view': 'folder_edit', 'args': 'object.pk', 'famfam': 'folder_edit', 'permissions': [PERMISSION_FOLDER_EDIT]}
folder_delete = {'text': _('delete'), 'view': 'folder_delete', 'args': 'object.pk', 'famfam': 'folder_delete', 'permissions': [PERMISSION_FOLDER_DELETE]}
folder_document_multiple_remove = {'text': _('remove from folder'), 'view': 'folder_document_multiple_remove', 'args': 'object.pk', 'famfam': 'folder_delete', 'permissions': [PERMISSION_FOLDER_REMOVE_DOCUMENT]}
folder_view = {'text': _(u'folder documents'), 'view': 'folder_view', 'args': 'object.pk', 'famfam': 'folder_go', 'permissions': [PERMISSION_FOLDER_VIEW]}
folder_add_document = {'text': _('add to a folder'), 'view': 'folder_add_document', 'args': 'object.pk', 'famfam': 'folder_add', 'permissions': [PERMISSION_FOLDER_ADD_DOCUMENT]}
folder_add_multiple_documents = {'text': _('add to folder'), 'view': 'folder_add_multiple_documents', 'famfam': 'folder_add'}
document_folder_list = {'text': _(u'folders'), 'view': 'document_folder_list', 'args': 'object.pk', 'famfam': 'folder_user', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'children_view_regex': [r'folder']}

folder_acl_list = {'text': _(u'ACLs'), 'view': 'folder_acl_list', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
folders_main_menu_link = {'text': _('folders'), 'famfam': 'folder_user', 'view': 'folder_list'}
