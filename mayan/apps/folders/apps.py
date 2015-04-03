from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from common.menus import menu_secondary, menu_object, menu_main
from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_links, register_model_list_columns
from navigation.links import link_spacer
from rest_api.classes import APIEndPoint

from .links import (
    link_folder_list,
    document_folder_list, link_folder_acl_list, folder_add_document,
    folder_add_multiple_documents, link_folder_create, link_folder_delete,
    folder_document_multiple_remove, link_folder_edit, link_folder_view
)
from .models import Folder
from .permissions import (
    PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_REMOVE_DOCUMENT,
    PERMISSION_FOLDER_VIEW
)


class FoldersApp(apps.AppConfig):
    name = 'folders'
    verbose_name = _('Folders')

    def ready(self):
        menu_main.bind_links(links=[link_folder_list])
        menu_secondary.bind_links(links=[link_folder_list, link_folder_create], sources=[Folder, 'folders:folder_list', 'folders:folder_create'])
        menu_object.bind_links(links=[link_folder_view, link_folder_edit, link_folder_acl_list, link_folder_delete], sources=[Folder])

        #register_links(['folders:document_folder_list', 'folders:folder_add_document'], [folder_add_document], menu_name="sidebar")
        #register_links(Document, [document_folder_list], menu_name='form_header')
        #register_links([Document], [folder_add_multiple_documents, folder_document_multiple_remove, link_spacer], menu_name='multi_item_links')

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
