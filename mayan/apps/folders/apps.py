from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from common import (
    MayanAppConfig, menu_facet, menu_main, menu_object, menu_secondary,
    menu_sidebar, menu_multi_item
)
from common.utils import encapsulate
from documents.models import Document
from navigation.api import register_model_list_columns
from navigation import CombinedSource
from rest_api.classes import APIEndPoint

from .links import (
    link_folder_list,
    link_document_folder_list, link_folder_acl_list, link_folder_add_document,
    link_folder_add_multiple_documents, link_folder_create,
    link_folder_delete, link_folder_document_multiple_remove,
    link_folder_edit, link_folder_view
)
from .models import Folder
from .permissions import (
    PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_REMOVE_DOCUMENT,
    PERMISSION_FOLDER_VIEW
)


class FoldersApp(MayanAppConfig):
    name = 'folders'
    verbose_name = _('Folders')

    def ready(self):
        super(FoldersApp, self).ready()

        APIEndPoint('folders')

        class_permissions(Document, [
            PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_REMOVE_DOCUMENT
        ])

        class_permissions(Folder, [
            ACLS_EDIT_ACL, ACLS_VIEW_ACL, PERMISSION_FOLDER_DELETE,
            PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_VIEW
        ])

        menu_facet.bind_links(links=[link_document_folder_list], sources=[Document])
        menu_main.bind_links(links=[link_folder_list])
        menu_multi_item.bind_links(links=[link_folder_add_multiple_documents], sources=[Document])
        menu_multi_item.bind_links(links=[link_folder_document_multiple_remove], sources=[CombinedSource(obj=Document, view='folders:folder_view')])
        menu_object.bind_links(links=[link_folder_view, link_folder_edit, link_folder_acl_list, link_folder_delete], sources=[Folder])
        menu_secondary.bind_links(links=[link_folder_list, link_folder_create], sources=[Folder, 'folders:folder_list', 'folders:folder_create'])
        menu_sidebar.bind_links(links=[link_folder_add_document], sources=['folders:document_folder_list', 'folders:folder_add_document'])

        register_model_list_columns(Folder, [
            {'name': _('Created'), 'attribute': 'datetime_created'},
            {'name': _('Documents'), 'attribute': encapsulate(lambda x: x.documents.count())},
        ])
