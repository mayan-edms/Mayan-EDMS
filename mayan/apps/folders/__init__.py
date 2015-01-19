from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from common.utils import encapsulate
from documents.models import Document
from navigation.api import (
    register_links, register_model_list_columns, register_top_menu
)
from navigation.links import link_spacer
from rest_api.classes import APIEndPoint

from .links import (
    document_folder_list, folder_acl_list, folder_add_document,
    folder_add_multiple_documents, folder_create, folder_delete,
    folder_document_multiple_remove, folder_edit, folder_list, folder_view,
    folders_main_menu_link
)
from .models import Folder
from .permissions import (
    PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_REMOVE_DOCUMENT,
    PERMISSION_FOLDER_VIEW
)

register_links(Folder, [folder_view, folder_edit, folder_acl_list, folder_delete])
register_links([Folder, 'folders:folder_list', 'folders:folder_create'], [folder_list, folder_create], menu_name='secondary_menu')
register_links(['folders:document_folder_list', 'folders:folder_add_document'], [folder_add_document], menu_name="sidebar")
register_links(Document, [document_folder_list], menu_name='form_header')
register_links([Document], [folder_add_multiple_documents, folder_document_multiple_remove, link_spacer], menu_name='multi_item_links')

register_top_menu(name='folders', link=folders_main_menu_link)

class_permissions(Folder, [
    ACLS_EDIT_ACL, ACLS_VIEW_ACL, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_VIEW
])

class_permissions(Document, [
    PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_REMOVE_DOCUMENT
])

register_model_list_columns(Folder, [
    {'name': _('Created'), 'attribute': 'datetime_created'},
    {'name': _('Documents'), 'attribute': encapsulate(lambda x: x.documents.count())},
])

APIEndPoint('folders')
