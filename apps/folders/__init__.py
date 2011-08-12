from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_top_menu, \
    register_multi_item_links, register_sidebar_template
from documents.models import Document
from documents.literals import PERMISSION_DOCUMENT_VIEW

from folders.models import Folder

folder_list = {'text': _(u'folder list'), 'view': 'folder_list', 'famfam': 'folder_user'}
folder_create = {'text': _('create folder'), 'view': 'folder_create', 'famfam': 'folder_add'}
folder_edit = {'text': _('edit'), 'view': 'folder_edit', 'args': 'object.pk', 'famfam': 'folder_edit'}
folder_delete = {'text': _('delete'), 'view': 'folder_delete', 'args': 'object.pk', 'famfam': 'folder_delete'}
folder_document_multiple_remove = {'text': _('remove from folder'), 'view': 'folder_document_multiple_remove', 'args': 'object.pk', 'famfam': 'delete'}
folder_view = {'text': _(u'folder documents'), 'view': 'folder_view', 'args': 'object.pk', 'famfam': 'folder_go'}
folder_add_document = {'text': _('add to a folder'), 'view': 'folder_add_document', 'args': 'object.pk', 'famfam': 'add'}
document_folder_list = {'text': _(u'folders'), 'view': 'document_folder_list', 'args': 'object.pk', 'famfam': 'folder_user', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'children_view_regex': [r'folder']}

register_multi_item_links(['folder_view'], [folder_document_multiple_remove])

register_links(Folder, [folder_view, folder_edit, folder_delete])

register_links(['folder_edit', 'folder_delete', 'folder_list', 'folder_create', 'folder_view', 'folder_document_multiple_remove'], [folder_list, folder_create], menu_name='secondary_menu')

register_top_menu(name='folders', link={'text': _('folders'), 'famfam': 'folder_user', 'view': 'folder_list'}, children_views=['folder_list', 'folder_create', 'folder_edit', 'folder_delete', 'folder_view', 'folder_document_multiple_remove'])

register_links(Document, [document_folder_list], menu_name='form_header')

register_sidebar_template(['folder_list'], 'folders_help.html')

register_links(['document_folder_list', 'folder_add_document'], [folder_add_document], menu_name="sidebar")
