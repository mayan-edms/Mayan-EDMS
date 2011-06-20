from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_top_menu, \
    register_multi_item_links, register_sidebar_template
from navigation.api import register_sidebar_template

from folders.models import Folder

folder_list = {'text': _(u'folder list'), 'view': 'folder_list', 'famfam': 'folder_user'}
folder_create = {'text': _('create folder'), 'view': 'folder_create', 'famfam': 'folder_add'}
folder_edit = {'text': _('edit'), 'view': 'folder_edit', 'args': 'object.id', 'famfam': 'folder_edit'}
folder_delete = {'text': _('delete'), 'view': 'folder_delete', 'args': 'object.id', 'famfam': 'folder_delete'}
folder_document_multiple_remove = {'text': _('remove'), 'view': 'folder_document_multiple_remove', 'famfam': 'delete'}
folder_view = {'text': _(u'folder documents'), 'view': 'folder_view', 'args': 'object.id', 'famfam': 'folder_go'}

register_multi_item_links(['folder_view'], [folder_document_multiple_remove])

register_links(Folder, [folder_view, folder_edit, folder_delete])

register_links(['folder_edit', 'folder_delete', 'folder_list', 'folder_create', 'folder_view'], [folder_list, folder_create], menu_name='secondary_menu')

register_top_menu(name='folders', link={'text': _('folders'), 'famfam': 'folder_user', 'view': 'folder_list'}, children_path_regex=[r'^folders/'])

register_sidebar_template(['document_view_advanced', 'document_view_simple'], 'folders_sidebar_template.html')

register_sidebar_template(['folder_list'], 'folders_help.html')
