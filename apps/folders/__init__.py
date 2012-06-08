from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (bind_links, register_top_menu,
    register_multi_item_links, register_sidebar_template, Link)
from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from acls.api import class_permissions
from acls.permissions import ACLS_EDIT_ACL, ACLS_VIEW_ACL

from .models import Folder
from .permissions import (PERMISSION_FOLDER_CREATE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_REMOVE_DOCUMENT, PERMISSION_FOLDER_VIEW,
    PERMISSION_FOLDER_ADD_DOCUMENT)

folder_list = Link(text=_(u'folder list'), view='folder_list', sprite='folder_user')
folder_create = Link(text=_('create folder'), view='folder_create', sprite='folder_add', permissions=[PERMISSION_FOLDER_CREATE])
folder_edit = Link(text=_('edit'), view='folder_edit', args='object.pk', sprite='folder_edit', permissions=[PERMISSION_FOLDER_EDIT])
folder_delete = Link(text=_('delete'), view='folder_delete', args='object.pk', sprite='folder_delete', permissions=[PERMISSION_FOLDER_DELETE])
folder_document_multiple_remove = Link(text=_('remove from folder'), view='folder_document_multiple_remove', args='object.pk', sprite='delete', permissions=[PERMISSION_FOLDER_REMOVE_DOCUMENT])
folder_view = Link(text=_(u'folder documents'), view='folder_view', args='object.pk', sprite='folder_go', permissions=[PERMISSION_FOLDER_VIEW])
folder_add_document = Link(text=_('add to a folder'), view='folder_add_document', args='object.pk', sprite='add', permissions=[PERMISSION_FOLDER_ADD_DOCUMENT])
document_folder_list = Link(text=_(u'folders'), view='document_folder_list', args='object.pk', sprite='folder_user', permissions=[PERMISSION_DOCUMENT_VIEW], children_view_regex=[r'folder'])

folder_acl_list = Link(text=_(u'ACLs'), view='folder_acl_list', args='object.pk', sprite='lock', permissions=[ACLS_VIEW_ACL])

register_multi_item_links(['folder_view'], [folder_document_multiple_remove])

bind_links([Folder], [folder_view, folder_edit, folder_delete, folder_acl_list])

bind_links([Folder, 'folder_list', 'folder_create'], [folder_list, folder_create], menu_name='secondary_menu')

register_top_menu(name='folders', link=Link(text=_('folders'), sprite='folder_user', view='folder_list', children_views=['folder_list', 'folder_create', 'folder_edit', 'folder_delete', 'folder_view', 'folder_document_multiple_remove']))

bind_links([Document], [document_folder_list], menu_name='form_header')

register_sidebar_template(['folder_list'], 'folders_help.html')

bind_links(['document_folder_list', 'folder_add_document'], [folder_add_document], menu_name="sidebar")

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
