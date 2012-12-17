from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (register_links, register_top_menu,
    register_multi_item_links, register_sidebar_template)
from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from acls.api import class_permissions
from acls import ACLS_EDIT_ACL, ACLS_VIEW_ACL

from .models import Folder
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

register_multi_item_links(['folder_view'], [folder_document_multiple_remove])

register_links(Folder, [folder_view, folder_edit, folder_delete, folder_acl_list])

register_links([Folder, 'folder_list', 'folder_create'], [folder_list, folder_create], menu_name='secondary_menu')

register_top_menu(name='folders', link={'text': _('folders'), 'famfam': 'folder_user', 'view': 'folder_list'}, children_views=['folder_list', 'folder_create', 'folder_edit', 'folder_delete', 'folder_view', 'folder_document_multiple_remove'])

register_links(Document, [document_folder_list], menu_name='form_header')

register_sidebar_template(['folder_list'], 'folders_help.html')

register_links(['document_folder_list', 'folder_add_document'], [folder_add_document], menu_name="sidebar")

register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_node_view', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent', 'tag_tagged_item_list'], [folder_add_multiple_documents])

class_permissions(Folder, [
    PERMISSION_FOLDER_EDIT,
    PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_VIEW,
    ACLS_EDIT_ACL,
    ACLS_VIEW_ACL
])

class_permissions(Document, [
    PERMISSION_FOLDER_ADD_DOCUMENT,
    PERMISSION_FOLDER_REMOVE_DOCUMENT,
])
