from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.links import link_acl_list
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_main, menu_object, menu_secondary,
    menu_sidebar, menu_multi_item
)
from documents.models import Document
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .links import (
    link_folder_list,
    link_document_folder_list, link_folder_add_document,
    link_folder_add_multiple_documents, link_folder_create,
    link_folder_delete, link_folder_document_multiple_remove,
    link_folder_edit, link_folder_view
)
from .models import DocumentFolder, Folder
from .permissions import (
    permission_folder_add_document, permission_folder_delete,
    permission_folder_edit, permission_folder_remove_document,
    permission_folder_view
)


class FoldersApp(MayanAppConfig):
    name = 'folders'
    test = True
    verbose_name = _('Folders')

    def ready(self):
        super(FoldersApp, self).ready()

        APIEndPoint(app=self, version_string='1')

        Document.add_to_class(
            'document_folders',
            lambda document: DocumentFolder.objects.filter(documents=document)
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_folder_add_document,
                permission_folder_remove_document
            )
        )

        ModelPermission.register(
            model=Folder, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_folder_delete, permission_folder_edit,
                permission_folder_view
            )
        )

        SourceColumn(
            source=Folder, label=_('Created'), attribute='datetime_created'
        )
        SourceColumn(source=Folder, label=_('User'), attribute='user')
        SourceColumn(
            source=Folder, label=_('Documents'),
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            )
        )

        menu_facet.bind_links(
            links=(link_document_folder_list,), sources=(Document,)
        )
        menu_main.bind_links(links=(link_folder_list,))
        menu_multi_item.bind_links(
            links=(link_folder_add_multiple_documents,), sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(link_folder_document_multiple_remove,),
            sources=('folders:folder_view',)
        )
        menu_object.bind_links(
            links=(
                link_folder_view,
            ), sources=(DocumentFolder, )
        )
        menu_object.bind_links(
            links=(
                link_folder_view, link_folder_edit, link_acl_list,
                link_folder_delete
            ), sources=(Folder,)
        )
        menu_secondary.bind_links(
            links=(link_folder_list, link_folder_create),
            sources=(Folder, 'folders:folder_list', 'folders:folder_create')
        )
        menu_sidebar.bind_links(
            links=(link_folder_add_document,),
            sources=(
                'folders:document_folder_list', 'folders:folder_add_document'
            )
        )
