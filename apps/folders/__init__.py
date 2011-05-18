from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_menu, \
    register_multi_item_links
from navigation.api import register_sidebar_template

from folders.models import Folder

folder_list = {'text': _(u'folder list'), 'view': 'folder_list', 'famfam': 'folder_user'}
folder_create = {'text': _('create folder'), 'view': 'folder_create', 'famfam': 'folder_add'}
folder_edit = {'text': _('edit'), 'view': 'folder_edit', 'args': 'object.id', 'famfam': 'folder_edit'}
folder_delete = {'text': _('delete'), 'view': 'folder_delete', 'args': 'object.id', 'famfam': 'folder_delete'}
folder_document_multiple_remove = {'text': _('remove'), 'view': 'folder_document_multiple_remove', 'famfam': 'delete'}

register_multi_item_links(['folder_view'], [folder_document_multiple_remove])

register_links(Folder, [folder_edit, folder_delete])

register_links(['folder_edit', 'folder_delete', 'folder_list', 'folder_create'], [folder_list, folder_create], menu_name='sidebar')

register_menu([
    {'text': _('folders'), 'view': 'folder_list', 'links': [
        folder_list, folder_create
    ], 'famfam': 'folder_user', 'position': 2}])

register_sidebar_template(['document_view', 'document_view_simple'], 'folders_sidebar_template.html')
