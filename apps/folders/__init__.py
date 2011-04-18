from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_model_list_columns, register_multi_item_links
#from main.api import register_diagnostic
from permissions.api import register_permissions

from models import Folder

folder_list = {'text':  _(u'folder list'), 'view': 'folder_list', 'famfam': 'folder'}
folder_create = {'text': _('create folder'), 'view': 'folder_create', 'famfam': 'folder_add'}
folder_edit = {'text': _('edit'), 'view': 'folder_edit', 'args': 'object.id', 'famfam': 'folder_edit'}
folder_delete = {'text': _('delete'), 'view': 'folder_delete', 'args': 'object.id', 'famfam': 'folder_delete'}

#document_create_multiple = {'text': _('upload multiple new documents'), 'view': 'document_create_multiple', 'famfam': 'page_add', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}
#document_create_sibling = {'text': _('upload new document using same metadata'), 'view': 'document_create_sibling', 'args': 'object.id', 'famfam': 'page_copy', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_CREATE]}}
#document_view = {'text': _('details (advanced)'), 'view': 'document_view', 'args': 'object.id', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
#document_view_simple = {'text': _('details (simple)'), 'view': 'document_view_simple', 'args': 'object.id', 'famfam': 'page', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
#document_multiple_delete = {'text': _('delete'), 'view': 'document_multiple_delete', 'famfam': 'page_delete', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_DELETE]}}
#document_edit_metadata = {'text': _('edit metadata'), 'view': 'document_edit_metadata', 'args': 'object.id', 'famfam': 'page_edit', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_METADATA_EDIT]}}
#document_multiple_edit_metadata = {'text': _('edit metadata'), 'view': 'document_multiple_edit_metadata', 'famfam': 'page_edit', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_METADATA_EDIT]}}
#document_preview = {'text': _('preview'), 'class': 'fancybox', 'view': 'document_preview', 'args': 'object.id', 'famfam': 'magnifier', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
#document_download = {'text': _('download'), 'view': 'document_download', 'args': 'object.id', 'famfam': 'page_save', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}}
#document_find_duplicates = {'text': _('find duplicates'), 'view': 'document_find_duplicates', 'args': 'object.id', 'famfam': 'page_refresh', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
#document_find_all_duplicates = {'text': _('find all duplicates'), 'view': 'document_find_all_duplicates', 'famfam': 'page_refresh', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_VIEW]}}
#document_clear_transformations = {'text': _('clear all transformations'), 'view': 'document_clear_transformations', 'args': 'object.id', 'famfam': 'page_paintbrush', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}
#document_multiple_clear_transformations = {'text': _('clear all transformations'), 'view': 'document_multiple_clear_transformations', 'famfam': 'page_paintbrush', 'permissions': {'namespace': 'documents', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}}

#register_links(Document, [document_view_simple, document_view, document_edit, document_edit_metadata, document_delete, document_download, document_find_duplicates, document_clear_transformations], menu_name='sidebar')
#register_links(Document, [document_list_recent, document_list, document_create, document_create_multiple, document_create_sibling], menu_name='sidebar')
#register_multi_item_links(['document_list'], [document_multiple_clear_transformations, document_multiple_edit_metadata, document_multiple_delete])

#####register_links(['folder_list', 'document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_document_with_type', 'upload_multiple_documents_with_type'], [folder_list, folder_create], menu_name='sidebar')

register_links(Folder, [folder_edit, folder_delete])

register_links(['folder_edit', 'folder_delete', 'folder_list', 'folder_create'], [folder_list, folder_create], menu_name='sidebar')


register_menu([
    {'text': _('folders'), 'view': 'folder_list', 'links': [
        folder_list, folder_create
    ], 'famfam': 'folder', 'position': 2}])
