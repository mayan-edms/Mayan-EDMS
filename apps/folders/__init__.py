from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from documents.models import Document
from navigation.api import (bind_links, register_multi_item_links,
    register_sidebar_template)

from .links import (folder_list, folder_create, folder_edit,
    folder_delete, folder_document_multiple_remove, folder_view,
    folder_add_document, document_folder_list, folder_acl_list,
    folder_add_multiple_documents)
from .models import Folder
from .permissions import (PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_REMOVE_DOCUMENT, PERMISSION_FOLDER_VIEW,
    PERMISSION_FOLDER_ADD_DOCUMENT)

register_multi_item_links(['folder_view'], [folder_document_multiple_remove])
bind_links([Folder], [folder_view, folder_edit, folder_delete, folder_acl_list])
bind_links([Folder, 'folder_list', 'folder_create'], [folder_list, folder_create], menu_name='secondary_menu')
bind_links([Document], [document_folder_list], menu_name='form_header')
bind_links(['document_folder_list', 'folder_add_document'], [folder_add_document], menu_name="sidebar")
register_sidebar_template(['folder_list'], 'folders_help.html')
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
