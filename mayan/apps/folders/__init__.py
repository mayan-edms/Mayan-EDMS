from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL
from common.utils import encapsulate
from documents.models import Document
from navigation.api import (register_links, register_model_list_columns,
                            register_multi_item_links, register_top_menu)
from rest_api.classes import APIEndPoint

from .links import (document_folder_list, folder_acl_list,
                    folder_add_document, folder_add_multiple_documents,
                    folder_create, folder_delete,
                    folder_document_multiple_remove, folder_edit, folder_list,
                    folder_view, folders_main_menu_link)
from .models import Folder
from .permissions import (PERMISSION_FOLDER_ADD_DOCUMENT,
                          PERMISSION_FOLDER_DELETE, PERMISSION_FOLDER_EDIT,
                          PERMISSION_FOLDER_REMOVE_DOCUMENT,
                          PERMISSION_FOLDER_VIEW)
from .urls import api_urls


def document_folders(self):
    return Folder.objects.filter(folderdocument__document=self)


register_links(Document, [document_folder_list], menu_name='form_header')
register_links(Folder, [folder_view, folder_edit, folder_delete, folder_acl_list])
register_links([Folder, 'folders:folder_list', 'folders:folder_create'], [folder_list, folder_create], menu_name='secondary_menu')
register_links(['folders:document_folder_list', 'folders:folder_add_document'], [folder_add_document], menu_name="sidebar")

register_multi_item_links(['documents:document_find_duplicates', 'folders:folder_view', 'indexes:index_instance_node_view', 'documents:document_type_document_list', 'search:search', 'search:results', 'indexing:document_group_view', 'documents:document_list', 'documents:document_list_recent', 'tags:tag_tagged_item_list'], [folder_add_multiple_documents])
register_multi_item_links(['folders:folder_view'], [folder_document_multiple_remove])

register_top_menu(name='folders', link=folders_main_menu_link, children_views=['folders:folder_list', 'folders:folder_create', 'folders:folder_edit', 'folders:folder_delete', 'folders:folder_view', 'folders:folder_document_multiple_remove'])

class_permissions(Folder, [ACLS_EDIT_ACL, ACLS_VIEW_ACL,
                           PERMISSION_FOLDER_DELETE, PERMISSION_FOLDER_EDIT,
                           PERMISSION_FOLDER_VIEW])

class_permissions(Document, [PERMISSION_FOLDER_ADD_DOCUMENT,
                             PERMISSION_FOLDER_REMOVE_DOCUMENT])

register_model_list_columns(Folder, [
    {'name': _(u'Created'), 'attribute': 'datetime_created'},
    {'name': _(u'Documents'), 'attribute': encapsulate(lambda x: x.documents.count())},
])

Document.add_to_class('folders', property(document_folders))

endpoint = APIEndPoint('folders')
endpoint.register_urls(api_urls)
endpoint.add_endpoint('folder-list', _(u'Returns a list of all the folders.'))
